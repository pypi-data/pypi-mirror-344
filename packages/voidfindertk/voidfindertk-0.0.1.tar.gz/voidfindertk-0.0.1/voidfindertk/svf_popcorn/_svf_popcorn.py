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


"""Module that holds functions and methods that are used to run SVF Popcorn \
void finder."""


# =============================================================================
# IMPORTS
# =============================================================================


import os
import pathlib
import shutil
import tempfile

import attr

import numpy as np

from . import _svf_pc_postprocessing, _svf_pc_wrapper
from ..core import VoidFinderABC
from ..settings import SETTINGS
from ..utils import make_workdir


class Paths:
    """
    A class to store paths used in the Popcorn void finder.

    Attributes
    ----------
    SVF : pathlib.Path
        Path to the source folder of the Popcorn void finder.
    CONFFILE : pathlib.Path
        Path to the configuration folder within the SVF directory.
    """

    # Path to the src folder of Popcorn.
    SVF = pathlib.Path(SETTINGS.popcorn_path)
    # Path to the configuration File of Popcorn.
    CONFFILE = SVF / "configuration"


class FileNames:
    """
    A class to hold the file names used in the Popcorn void finder project.

    Attributes
    ----------
    CONFIG : str
        Name of the configuration file.
    TRSFILE : str
        Name of the tracer file.
    SPHFILE : str
        Name of the spherical voids catalogue file.
    POPFILE : str
        Name of the popcorn voids catalogue file.
    RAWPOPFILE : str
        Name of the raw popcorn voids file before cleaning.
    PAIRSFILE : str
        Name of the file containing pairs of touching popcorn voids.
    """

    CONFIG = "vars.conf"
    TRSFILE = "trsfile.dat"
    SPHFILE = "sphfile.dat"
    POPFILE = "popfile.dat"
    RAWPOPFILE = "rawpopfile.dat"
    PAIRSFILE = "pairsfile.dat"


@attr.define
class SVFPopCorn(VoidFinderABC):
    """PopCornVF class for void finding and analysis.

    Attributes
    ----------
    auxfiles : str
        Flag indicating the use of auxiliary files.
    boxsize : float
        Length of the box in the same units as the tracer input file.
    densth : float
        Density threshold for void identification.
    minradius : int
        Minimum radius of a sphere in input units.
    maxradius : int
        Maximum radius of a sphere in input units.
    svf_path : pathlib.Path
        Path to the source directory of the SVF.
    cores : str or None
        MPI flags for parallel computation.
    workdir : pathlib.Path
        Path to the working directory.
    workdir_clean : bool
        Flag to clean the working directory on deletion.

    Notes
    -----
    MASSMIN popcorns parameter in vars.conf file is always set to when using
    this interface. This way all the masses in the input file are considered.
    In order to constrain the mass of the input please use the box method:
    box.mass_cutoff(mass_threshold=<threshold>).
    """

    _auxfiles = attr.field(default="true", alias="auxfiles")  # AUXILIARY FILES
    # INPUT PARAMETERS
    _boxsize = attr.field(default=1000.0, alias="boxsize")
    _densth = attr.field(default=-0.9, alias="densth")
    _minradius = attr.field(default=5, alias="minradius")
    _maxradius = attr.field(default=100, alias="maxradius")
    # Path to Source folder
    _svf_path = attr.field(
        default=None, alias="svf_path"
    )  # Path to source directory of SVF
    # mpi flags:
    _cores = attr.field(default=None, alias="cores")
    # Path to working directory
    _workdir = attr.field(default=None, alias="workdir")
    # Whether to clean or not the working directory
    _workdir_clean = attr.field(default=False, alias="workdir_clean")

    # Set path to extra files
    def __attrs_post_init__(self):
        """Post inicialization method."""
        # svf_path
        if self._svf_path is None:
            self._svf_path = Paths.SVF

        # Set workdir path
        self._workdir = pathlib.Path(
            tempfile.mkdtemp(prefix=f"svf_{type(self).__name__}_")
            if self._workdir is None
            else pathlib.Path(os.path.abspath(self._workdir))
        )

    # PROPERTIES ==============================================================

    @property
    def auxfiles(self):
        """Returns the flag for auxiliary files."""
        return self._auxfiles

    @property
    def boxsize(self):
        """Returns the length of the box."""
        return self._boxsize

    @property
    def densth(self):
        """Returns the density threshold."""
        return self._densth

    @property
    def minradius(self):
        """Returns the minimum radius for void detection."""
        return self._minradius

    @property
    def maxradius(self):
        """Returns the maximum radius for void detection."""
        return self._maxradius

    @property
    def svf_path(self):
        """Returns the path to the SVF directory."""
        return self._svf_path

    @property
    def cores(self):
        """Returns the MPI flags."""
        return self._cores

    @property
    def workdir(self):
        """Returns the working directory path."""
        return self._workdir

    @property
    def workdir_clean(self):
        """Returns the flag for cleaning the working directory."""
        return self._workdir_clean

    # INTERNAL ================================================================
    # Directory Creator
    def _create_run_work_dir(self):
        """
        Creates and returns a temporary working directory.

        Returns
        -------
        pathlib.Path
            The path to the created working directory.
        """
        run_workdir = make_workdir.create_run_work_dir(
            workdir_path=self._workdir
        )
        return run_workdir

    # Directory Cleaner
    def __del__(self):
        """
        Workdir Cleaner.

        Destructor that cleans up the temporary working directory
        if workdir_clean is True.
        """
        if self._workdir_clean:
            shutil.rmtree(self._workdir)

    def preprocess(self, box):
        """
        Placeholder for preprocessing the box object.

        Parameters
        ----------
        box : Object
            The box object to preprocess.

        Returns
        -------
        Object
            The processed box object.
        """
        return box

    def model_find(self, box):
        """
        Performs Void Finding with PopCorn Void Finder.

        Runs the POPCORN void finder by creating the input file and the
        vars.conf parameter file and then running the binary using command line
        instructions.

        Parameters
        ----------
            box : Object
                Box object that holds the tracer properties.

        Returns
        -------
            Dictionary with two parameters:
                - run_work_dir : path to the working directory.
                - box : Box Object.

        Notes
        -----
        To run the POPCORN void finder, an input tracer and a configuration
        file are needed. The input tracer file is built using the Box Object.
        The configuration file is built using the parameters of the class.
        """
        # create the sandbox
        run_work_dir = self._create_run_work_dir()

        # Create config file on Workdir
        _svf_pc_wrapper.config_file_maker(
            # Files
            trsfile=str(run_work_dir / FileNames.TRSFILE),
            filefmt="ASCII",
            num_file=str(1),
            sphfile=str(run_work_dir / FileNames.SPHFILE),
            popfile=str(run_work_dir / FileNames.POPFILE),
            auxfiles=str(self._auxfiles),
            rawpopfile=str(run_work_dir / FileNames.RAWPOPFILE),
            pairsfile=str(run_work_dir / FileNames.PAIRSFILE),
            # Parameters
            boxsize=str(self._boxsize),
            densth=str(self._densth),
            minradius=str(self._minradius),
            maxradius=str(self._maxradius),
            massmin=str(0),
            eps=str(1e-5),
            path=str(run_work_dir / FileNames.CONFIG),  # Workdir path
        )

        # Generate dataset file from box
        _svf_pc_wrapper.popcorn_svf_input_data_builder(
            box=box, file_path=str(run_work_dir / FileNames.TRSFILE)
        )  # Save File to workdir
        # Run Void Finder
        _svf_pc_wrapper.spherical_popcorn_void_finder(
            cores=self._cores,
            bin_path=Paths.SVF,
            conf_file_path=run_work_dir / FileNames.CONFIG,
            work_dir_path=run_work_dir,
        )
        return {"run_work_dir": run_work_dir, "box": box}

    def build_voids(self, model_find_parameters):
        """
        Postprocess outputs from PopCorn Void Finder output files.

        Postprocesses the outputs of the POPCORN (spherical) void finder to get
        the list of tracers inside each void (if any) and properties found by
        this method.

        Parameters
        ----------
            model_find_parameters : Dict
                Parameters obtained from the model_find step.

        Returns
        -------
            tracers_in_voids : tuple
                List of indexes of tracers (relative to the Box object index)
                inside each void.

            centers : numpy 2D array
                (x, y, z) coordinates of each center for each void.

            extra : Dict
                Dictionary with extra parameters, varying from properties to
                directory paths.
        """
        # Retrieve box from box object
        box = model_find_parameters["box"]
        # Get current working directory
        run_work_dir = pathlib.Path(model_find_parameters["run_work_dir"])
        # Get void Properties
        properties = _svf_pc_postprocessing.get_void_properties(
            popcorn_output_file_path=str(run_work_dir / FileNames.SPHFILE)
        )
        # Get tracers in void
        tracers_in_voids = _svf_pc_postprocessing.get_tracers_in_voids(
            box=box,
            popcorn_output_file_path=str(run_work_dir / FileNames.SPHFILE),
        )
        # Get centers coordinates
        centers = np.array(properties[["x", "y", "z"]])

        # Build extra
        extra = {
            "radius": np.array(properties["r"]),
            "properties": properties,
            "files_directory_path": run_work_dir,
        }
        return tuple(tracers_in_voids), centers, extra
