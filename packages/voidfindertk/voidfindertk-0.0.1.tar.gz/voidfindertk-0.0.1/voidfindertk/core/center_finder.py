#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 - 2024, Bustillos Federico, Gualpa Sebastian, Cabral Juan,
#                            Paz Dante, Ruiz Andres, Correa Carlos
# License: MIT
# Full Text: https://github.com/FeD7791/voidFinderProject/blob/dev/LICENSE.txt
# All rights reserved.


# =============================================================================
# DOCS
# =============================================================================

"""Module to perform center calculatios based on tracers."""

# =============================================================================
# IMPORTS
# =============================================================================

from joblib import Parallel, delayed, parallel_backend

import numpy as np

from voidfindertk.utils.box_to_grid import get_grispy_grid_from_box

# =============================================================================
# FUNCTIONS
# =============================================================================


def _get_xyz_tracers_from_indx(*, box, tracers_idx):
    """Find the (x,y,z) coordinates of tracer based on an index and the Box.

    Parameters
    ----------
        box : Box
            Object with tracer properties.

        tracers_idx : list
            Iterable with the indexes of the tracers
    """
    centers = np.column_stack((box.arr_.x, box.arr_.y, box.arr_.z))
    return [centers[idx] for idx in tracers_idx]


def _single_center_search(*, tracers, box_size, threshold, n_neighbors, grid):
    """
    Estimate the density-weighted center of a region based on tracer positions.

    This function calculates the density around each tracer by computing the
    distance to its `n_neighbors` nearest neighbors, and then estimates a
    center using a density-weighted average of the tracer positions. It also
    applies a boundary correction if tracers are close to the box edges.

    Parameters
    ----------
    tracers : ndarray of shape (N, 3)
        Coordinates of tracer particles in 3D space.

    box_size : float
        The size of the (assumed cubic) simulation box.

    threshold : float
        Threshold used for determining proximity to the box boundaries. Tracers
        beyond `threshold * box_size` are wrapped around for continuity.

    n_neighbors : int
        Number of nearest neighbors to consider for local density estimation.

    grid : object
        A spatial indexing structure with a `nearest_neighbors(centres, n)`
        method that returns distances and indices of nearest neighbors for
        given centres.

    Returns
    -------
    center : ndarray of shape (3,)
        The density-weighted center coordinates, wrapped within the bounds of
        the box.

    Notes
    -----
    - This function assumes periodic boundary conditions and performs a simple
      correction for tracers near the box boundary.
    - The density is estimated using the volume enclosed by the distance to
      the farthest of the `n_neighbors` for each tracer.
    """
    # Calculate the distances to n_neighbors to each of the tracers in the
    # array. n = n_neighbors+1 since first distance is to the center itself.

    distances_, nn = grid.nearest_neighbors(centres=tracers, n=n_neighbors + 1)
    # Get the fartest distance and make it as radius. This is an array of
    # fartest radius to each tracer in the void

    radius = np.array(list(map(np.max, distances_)))

    # Using that radius calculate as density.
    density = 1 / (n_neighbors / ((4 / 3) * np.pi * radius**3))

    # Compute bin width
    bin_width = np.abs(box_size - threshold * box_size)

    counts = np.histogram(
        np.ravel(tracers),
        bins=np.arange(0, box_size + bin_width, bin_width),
    )[0]

    if (counts[0] > 0) & (counts[-1] > 0):
        # We shift the tracers near superior border
        tracers_ = np.where(
            tracers > threshold * box_size,  # Condition
            tracers - box_size,  # If condition condition fullfilled
            tracers,  # Else
        )
    else:
        tracers_ = tracers

    center = np.sum((tracers_.T * density).T, axis=0) / np.sum(density)

    return np.mod(center, box_size)


def center_calculator(
    *, box, tracers_in_voids, n_neighbors, threshold, n_jobs, batch_size
):
    """Calculate the center of mass for multiple voids in parallel.

    This function computes the center of mass for each void region defined by
    tracers, using a density-weighted approach and accounting for periodic
    boundary conditions. The calculation is performed in parallel batches for
    efficiency.

    Parameters
    ----------
    box : Box
        Simulation box object containing tracer positions and size information.
        Must have `arr_.x`, `arr_.y`, `arr_.z` attributes and `size()` method.

    tracers_in_voids : list of lists
        List where each element contains the indices of tracers belonging to
        a single void region.

    n_neighbors : int
        Number of nearest neighbors to consider for local density estimation.

    threshold : float
        Fraction of box size used to determine periodic boundary handling.
        Tracers beyond `threshold * box_size` are shifted.

    n_jobs : int
        Number of parallel jobs to use for computation.

    batch_size : int
        Number of voids to process in each parallel batch. Voids are grouped
        by similar tracer count for efficiency.

    Returns
    -------
    numpy.ndarray
        Array of shape (n_voids, 3) containing the (x,y,z) coordinates of each
        void center, ordered to match the input `tracers_in_voids`.

    Notes
    -----
    The center calculation:
    1. Estimates local density using the distance to the nth nearest neighbor
    2. Handles periodic boundaries by shifting tracers near box edges
    3. Computes a density-weighted center of mass
    4. Applies periodic boundary conditions to the final center position

    The computation is performed in parallel batches of voids with similar
    tracer counts for optimal performance.
    """
    # Build grispy grid from Box
    grid = get_grispy_grid_from_box(box=box, N_cells=64)
    # Get (x,y,z) positions from tracers in each void.
    # We get a list of positions of tracers for each void
    tinv = _get_xyz_tracers_from_indx(box=box, tracers_idx=tracers_in_voids)

    # Sort by increasing number of tracers
    n_tracers = np.array(list(map(len, tinv)))

    tinv_sorted = [tinv[i] for i in np.argsort(n_tracers)]

    # Build batches of objects with similar number of tracers.

    centers_ = []
    batches = [
        tinv_sorted[i : i + batch_size]
        for i in np.arange(0, len(tinv), batch_size)
    ]

    with parallel_backend("threading"):
        for idx, batch in enumerate(batches):
            c_ = Parallel(n_jobs=n_jobs)(
                delayed(_single_center_search)(
                    tracers=tracers,
                    box_size=box.size(),
                    threshold=threshold,
                    n_neighbors=n_neighbors,
                    grid=grid,  # shared memory
                )
                for tracers in batch
            )
            centers_ = centers_ + list(c_)
            print(f"batch {idx + 1}/{len(batches)} compleated")
    # Sort back the result to the original order
    return np.array(centers_)[np.argsort(np.argsort(n_tracers))]
