#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2023 - 2024, Bustillos Federico, Gualpa Sebastian, Cabral Juan,
#                            Paz Dante, Ruiz Andres, Correa Carlos
# License: MIT
# Full Text: https://github.com/FeD7791/voidFinderProject/blob/dev/LICENSE.txt
# All rights reserved.

"""Cloud with voids builder utility."""

# =============================================================================
# IMPORTS
# =============================================================================

import grispy as gsp

import numpy as np

# =============================================================================
# FUNCTIONS
# =============================================================================


def _dens_gen(*, seed=2, center, rad, n_points):
    """
    Generate random points uniformly distributed within a spherical volume.

    Parameters
    ----------
    seed : int, optional
        Seed for the random number generator. Default is 2.
    center : array_like, shape (3,)
        The x, y, z coordinates of the center of the spherical volume.
    rad : float
        The radius of the spherical volume within which the points will be
        generated.
    n_points : int
        The number of random points to generate.

    Returns
    -------
    xyz : ndarray, shape (3, n_points)
        An array of shape (3, n_points) where each column represents the
        x, y, z coordinates of a generated point.

    Notes
    -----
    The generated points are uniformly distributed in a spherical shell with
    the specified radius and centered at the provided coordinates.

    """
    # generate_random_tracers_on_spherical_volume
    rng = np.random.default_rng(seed=seed)

    theta = rng.uniform(0, 2 * np.pi, size=(n_points, 1))

    phi = rng.uniform(0, np.pi, size=(n_points, 1))
    radii = rng.uniform(0, rad, size=(n_points, 1))
    x = np.ravel(center[0] + radii * np.sin(theta) * np.cos(phi))
    y = np.ravel(center[1] + radii * np.sin(theta) * np.sin(phi))
    z = np.ravel(center[2] + radii * np.cos(theta))
    xyz = np.column_stack((x, y, z))
    return xyz


def build_cloud(
    *,
    seed=2,
    lmin=0,
    lmax=1000,
    n_points=100**3,
):
    """
    Builds a cloud of n_points , where: lmin < x,y,z < lmax.

    Parameters
    ----------
        seed: int
            Seed for random number generator.
        lmin: float
            Low limit of random generated points.
        lmax: float
            Max limit of random generated points.
        n_points: int
            Number of points to be generated

    Returns
    -------
        cloud: array
            Array of n_points with x,y,z coordinates between lmin and lmax

    """
    rng = np.random.default_rng(seed=seed)
    # Create point cloud xyz
    cloud = rng.uniform(lmin, lmax, size=(n_points, 3))
    return cloud


def add_mass_to_cloud(*, cloud, seed=2, log_mass_min=10, log_mass_max=12):
    """
    Adds log of mass to a cloud of tracers.

    Parameters
    ----------
    cloud : array
        Array of xyz positions of tracers
    seed : int
        Seed for random number generator
    log_mass_min : float
        Minimun log sun mass.
    log_mass_max : float
        Maximun log sun mass.

    Returns
    -------
    cloud :
        Updated cloud with log mass.
    """
    rng = np.random.default_rng(seed=seed)
    # Generate mass for each tracers
    log_mass = np.ravel(
        rng.uniform(log_mass_min, log_mass_max, size=(len(cloud), 1))
    )
    cloud = np.vstack([cloud.T, log_mass]).T
    return cloud


def build_spherical_void(
    delta, centers: np.ndarray, radii: float, cloud, seed=2
):
    """
    Takes a cloud of tracers and removes tracers inside an spherical shell \
    around each void center so that each void has a desired density \
    density contrast.

    Parameters
    ----------
        delta: float
            Integrated density contrast of the void. -1 < delta < 0
        centers: array
            Array of x,y,z positions of void centers.
        radii: float
            Radius of void. (All void have same radius)
        cloud: array
            Collection of tracers, each with positions x,y,z that constitu-
            te the universe (Box)

    Returns
    -------
        cloud_with_voids : array
            Collection of tracers of cloud input, minus some tracers around
            each void so that these have the desired density contrast.
    """
    # Preserve max, min values of cloud
    max_cloud, min_cloud = np.max(cloud), np.min(cloud)
    # Set random seed
    rng = np.random.default_rng(seed=seed)

    # Calculate right number of tracers so the void gets at the desired
    # density
    tracers = find_tracers_in_spherical_region(
        cloud=cloud, centers=centers, radii=radii, sorted=True
    )
    add_remove = _tracers_to_remove_calculator(
        cloud=cloud, delta=delta, radii=radii, tracers=tracers
    )

    to_remove = np.array([], dtype=int)
    for m, cent, idx in zip(add_remove, [c for c in centers], tracers):
        if m > 0:
            tracers_ = rng.uniform(
                cent - radii * np.cos(np.pi / 4),
                cent + radii * np.cos(np.pi / 4),
                size=(m, 3),
            )
            cloud = np.vstack((cloud, tracers_))
        if m < 0:
            # Remove elements after otherwise this causes errors
            to_remove = np.concatenate((to_remove, idx[:-m]), dtype=int)

    # Now remove the desired elements.
    cloud = np.delete(cloud, to_remove, axis=0)

    cloud = np.where(cloud < min_cloud, cloud + (max_cloud - min_cloud), cloud)
    cloud = np.where(cloud > max_cloud, cloud - (max_cloud - min_cloud), cloud)
    tracers = find_tracers_in_spherical_region(
        cloud=cloud, centers=centers, radii=radii
    )

    return cloud


def find_tracers_in_spherical_region(cloud, centers, radii, **kwargs):
    """
    Find tracers (points) within spherical regions defined by given centers \
    and radii.

    This function uses the `GriSPy` library to set periodic boundaries for a
    3D grid and then finds the nearest neighbors (tracers) for each center
    point, where the distance between the tracers and centers is bounded by the
    specified radii. The function returns the indices of the tracers found
    within the spherical regions.

    Parameters
    ----------
    cloud : array_like, shape (N, 3)
        The 3D coordinates of points in the cloud. The shape should be (N, 3)
        where N is the number of points in the cloud, and each point has x, y,
        and z coordinates.

    centers : array_like, shape (M, 3)
        The 3D coordinates of the centers of the spherical regions where the
        tracers will be searched for. The shape should be (M, 3), where M is
        the number of spherical regions.

    radii : array_like, shape (M,)
        The radii of the spherical regions. The shape should be (M,) where M
        is the number of spherical regions, with each radius corresponding to
        the region centered at the respective entry in `centers`.

    **kwargs : keyword arguments, optional
        Additional keyword arguments passed to the `bubble_neighbors` method
        of the `GriSPy` object, such as distance metrics or other options
        related to neighbor search.

    Returns
    -------
    index : array_like, shape (M, K)
        The indices of the points in `cloud` that lie within each of the
        spherical regions defined by the centers and radii. The shape of the
        returned array is (M, K), where M is the number of centers, and K is
        the number of neighbors found within each region.

    Notes
    -----
    The `GriSPy` object uses the minimum and maximum values of the `cloud`
    points to define the periodicity of the grid, ensuring that the spherical
    regions are checked in a periodic manner across the grid.

    The periodic boundaries are set in all three dimensions (x, y, and z).

    This method assumes that the `cloud` points and `centers` are provided in
    3D space and that the distance calculation will be done in Euclidean space.
    """
    grid = gsp.GriSPy(cloud)
    # Set periodicity
    periodic = {
        0: (np.round(np.min(cloud), 0), np.round(np.max(cloud), 0)),
        1: (np.round(np.min(cloud), 0), np.round(np.max(cloud), 0)),
        2: (np.round(np.min(cloud), 0), np.round(np.max(cloud), 0)),
    }
    grid.set_periodicity(periodic, inplace=True)

    # Find nearest neighbors
    dist, index = grid.bubble_neighbors(
        centers, distance_upper_bound=radii, **kwargs
    )

    return index


def _tracers_to_remove_calculator(*, cloud, delta, radii, tracers):
    cloud_volume = round(np.max(cloud) - np.min(cloud)) ** 3
    cloud_density = len(cloud) / cloud_volume
    density_voids = (1 + delta) * cloud_density
    n_tracers = int(round(density_voids * (4 / 3) * np.pi * (radii**3), 0))
    n_tinv = list(map(len, tracers))
    return n_tracers - np.array(n_tinv)


def build_spherical_overdensity(delta, centers, radii, cloud):
    """
    Build a new point cloud by adding tracers to regions of specified centers \
    with a desired overdensity.

    Parameters
    ----------
    delta : float
        The overdensity factor to apply to the mean density of the cloud.
    centers : array_like, shape (n_centers, 3)
        An array of shape (n_centers, 3) containing the x, y, z coordinates
        of the centers where overdensity should be applied.
    radii : array_like, shape (n_centers,)
        An array of shape (n_centers,) specifying the radii of the spherical
        regions around each center where tracers will be added.
    cloud : array_like, shape (n_points, 3)
        The initial point cloud represented as an array of shape (n_points, 3),
        where each row corresponds to the x, y, z coordinates of a point.

    Returns
    -------
    cloud_with_overdensities : ndarray, shape (n_points + n_added_points, 3)
        A new array containing the original points in `cloud` along with
        additional tracers added to achieve the specified overdensity in
        the defined spherical regions.

    Notes
    -----
    This function assumes a periodic boundary condition for the point cloud
    and uses the Grispy library to find neighboring points within the given
    radii.

    """
    rho_med = len(cloud) / (np.max(cloud)) ** 3
    rho = (1 + delta) * rho_med
    # Get number of tracers that should be in void so that the overdensity is
    # reached for a certain radii (Rounded to closest integer)
    n_ideal_tracers_in_void = np.round(((4 / 3) * np.pi * radii**3) * rho, 0)

    # Get number of tracers in void using Grispy
    periodic = {
        0: (np.min(cloud), np.max(cloud)),
        1: (np.min(cloud), np.max(cloud)),
        2: (np.min(cloud), np.max(cloud)),
    }
    grid = gsp.GriSPy(cloud)
    grid.set_periodicity(periodic, inplace=True)
    dist_, indx = grid.bubble_neighbors(centers, distance_upper_bound=radii)
    n_actual_tracers_in_void = np.array(list(map(len, indx)))

    # Calculate number of tracers that should be added
    add_n = n_ideal_tracers_in_void - n_actual_tracers_in_void
    # If negative number of pints are provided then switch them to zero
    add_n = np.where(add_n < 0, 0, add_n)
    # Calculate tracers xyz positions
    new_tracers = [
        _dens_gen(center=e[0], rad=radii, n_points=int(e[1]))
        for e in zip(centers, add_n)
    ]
    new_tracers.append(cloud)
    # Add tracers to cloud
    cloud_with_overdensities = np.concatenate(new_tracers)
    return cloud_with_overdensities
