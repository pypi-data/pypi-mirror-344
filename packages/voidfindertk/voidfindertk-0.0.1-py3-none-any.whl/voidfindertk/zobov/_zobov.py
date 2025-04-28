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

"""Module that holds functions and methods that are used to run the ZOBOV \
python wrapper methods in a coherent step by step."""

# =============================================================================
# IMPORTS
# =============================================================================

import datetime as dt
import os
import pathlib
import shutil
import tempfile

import attr

import numpy as np

import pandas as pd

from . import _zb_postprocessing
from . import _zb_wrapper as _wrap
from ..core import VoidFinderABC
from ..settings import SETTINGS

# =============================================================================
# HELPER CLASSES
# =============================================================================


@attr.define(frozen=True)
class Names:
    """
    Holds Names to suffix inputs for files created using ZOBOV.

    Parameters
    ----------
        OUTPUT_VOZINIT : str
        Suffix of the name used as vozinit input.
    """

    OUTPUT_VOZINIT = "output_vozinit"
    OUTPUT_JOZOV_VOIDS = "output_txt"
    PARTICLES_IN_ZONES = "part_vs_zone"
    ZONES_IN_VOID = "zones_vs_voids"


@attr.define(frozen=True)
class _Files:
    """
    Names of the Box parsed to raw files.

    These files are parsed and saved with the same names (see write_input
    module in _wrapper).

    Attributes
    ----------
    TRACERS_RAW : str
        Name of the raw file for tracers.
    TRACERS_TXT : str
        Name of the ASCII text file for tracers.
    PARTICLES_VS_ZONES_RAW : str
        Name of the raw file for particles in zones.
    PARTICLES_VS_ZONES_ASCII : str
        Name of the ASCII text file for particles in zones.
    OUTPUT_JOZOV_VOIDS_DAT : str
        Name of the raw file for output from JOZOV regarding voids.
    ZONES_VS_VOID_RAW : str
        Name of the raw file for zones in voids.
    ZONES_VS_VOID_ASCII : str
        Name of the ASCII text file for zones in voids.
    """

    TRACERS_RAW = "tracers_zobov.raw"
    TRACERS_TXT = "tracers_zobov.txt"
    PARTICLES_VS_ZONES_RAW = f"{Names.PARTICLES_IN_ZONES}.dat"
    PARTICLES_VS_ZONES_ASCII = f"{Names.PARTICLES_IN_ZONES}_ascii.txt"
    OUTPUT_JOZOV_VOIDS_DAT = f"{Names.OUTPUT_JOZOV_VOIDS}.dat"
    ZONES_VS_VOID_RAW = f"{Names.ZONES_IN_VOID}.dat"
    ZONES_VS_VOID_ASCII = f"{Names.ZONES_IN_VOID}_ascii.txt"


@attr.define(frozen=True)
class _ExecutableNames:
    ZOBOV_LOADER_BIN = "zobov_loader.so"
    TRACERS_IN_ZONES_BIN = "tracers_in_zones.so"
    ZONES_IN_VOIDS_BIN = "zones_in_void.so"


@attr.define(frozen=True)
class _Paths:
    """
    Class that holds paths of reference to the current file and ZOBOV's\
    source directory.

    Attributes
    ----------
    ZOBOV : pathlib.Path
        Path to the src folder of ZOBOV.
    """

    CURRENT_FILE_PATH = executable_path = pathlib.Path(
        os.path.abspath(__file__)
    ).parent
    ZOBOV = pathlib.Path(SETTINGS.zobov_path)
    SO_PATHS = ZOBOV / "src"


# =============================================================================
# FINDER
# =============================================================================


@attr.define
class ZobovVF(VoidFinderABC):
    """
    ZobovVF class for running ZOBOV Void Finder.

    This class provides methods to preprocess data and execute the ZOBOV
    Void Finder algorithm on a given data box.

    Parameters
    ----------
    buffer_size : float, optional
        Buffer size for ZOBOV (default is 0.08). The buffer size sets the size
        in units such that the box size of the data cube is 1, of the buffer
        around each sub-box when calculating the Voronoi diagram.
    box_size : int, optional
        Range of positions of particles in each dimension (default is 500).
    number_of_divisions : int, optional
        Number of divisions in each dimension of the box (default is 2).
    density_threshold : float (0< density_threshold <1), optional
        Limits the growth in density of a Void in density_threshold*mean,
        where mean is the mean density of the box. A value of 0.2 is
        equivalent to a density contrast of -0.8.
        (default is 0.2)
    zobov_path : str or None, optional
        Path to ZOBOV executable (default is None, uses internal path).
    workdir : str or None, optional
        Temporary working directory path (default is None, creates a new temp
        directory).
    workdir_clean : bool, optional
        Whether to clean up the working directory on deletion (default is
        False).
    dtype : numpy.dtype, optional
        Data type used for computations (default is np.float32).
    center_method : str {"barycentre", "core_particle"}, default="barycentre".
        Selects the kind of center to be asociated to the final output. If
        barycentre is selected, (x,y,z) coordinates of centers will be
        asociated to centers gotten from the weighted sum of the volumes of
        voronoi cells asociated to a void. If core_particle is selected then
        the centers (x,y,z) coordinates will be asociated to the positions of
        the core particles in the watershed density algorythm.


    Methods
    -------
    preprocess(box)
        Placeholder method for data preprocessing.
    model_find(box)
        Executes the ZOBOV Void Finder algorithm on the provided    Box
        object.
        This step follows these steps:
            1. Build the input data from the input box. This step will parse
            the box data to a raw file that the next step needs
            2. Run ZOBOV's vozinit executable using the input params and the
            tracers input file build in the last step. As the process ends
            an script file will be created (see run_vozinit).
            3. In this step the mentioned script will be run. It will result
            in the output of volume and adjacency files (see run_voztie).
            4. This step will run ZOBOV's jozov executable (see run_jozov)
            This step will result in the output of three files:
                - part_vs_zone.dat : Raw File containing the particles inside
                zones (see run_jozov)
                - zones_vsvoids.dat : Raw File containing the zones inside
                voids (see run_jozov)
                - output_txt.dat : Ascii File containing the voids properties
                (see run_jozov)
            5. This step will create the object Voids that contains the voids
            foud by the method and their properties.

    Notes
    -----
    The ZOBOV Void Finder is executed in several steps including VOZINIT,
    VOZSTEP, and JOZOV.
    """

    _buffer_size = attr.field(default=0.08, alias="buffer_size")
    _box_size = attr.field(default=500, alias="box_size")
    _number_of_divisions = attr.field(default=2, alias="number_of_divisions")
    _density_threshold = attr.field(default=0.2, alias="density_threshold")
    _zobov_path = attr.field(default=None, alias="zobov_path")
    _workdir = attr.field(default=None, alias="workdir")
    _workdir_clean = attr.field(default=False, alias="workdir_clean")
    _dtype = attr.field(default=np.float32, alias="dtype")
    _center_method = attr.field(default="barycentre", alias="center_method")

    def __attrs_post_init__(self):
        """Post init Method."""
        if self._zobov_path is None:
            self._zobov_path = _Paths.ZOBOV

        # Create a workdir path to run ZOBOV
        self._workdir = pathlib.Path(
            tempfile.mkdtemp(prefix=f"vftk_{type(self).__name__}_")
            if self._workdir is None
            else pathlib.Path(os.path.abspath(self._workdir))
        )

        if self._center_method not in ["barycentre", "core_particle"]:
            raise ValueError("This is not a valid center_method")

    # PROPERTIES ==============================================================
    @property
    def buffer_size(self):
        """Return the buffer size for the ZOBOV void finder."""
        return self._buffer_size

    @property
    def box_size(self):
        """Return the size of the box for particle positions."""
        return self._box_size

    @property
    def number_of_divisions(self):
        """Return the number of divisions in each dimension of the box."""
        return self._number_of_divisions

    @property
    def ensity_threshold(self):
        """Return the density threshold for void growth."""
        return self._density_threshold

    @property
    def zobov_path(self):
        """Return the path to the ZOBOV executable."""
        return self._zobov_path

    @property
    def workdir(self):
        """Return the temporary working directory path."""
        return self._workdir

    @property
    def workdir_clean(self):
        """Return whether to clean up the working directory on deletion."""
        return self._workdir_clean

    @property
    def dtype(self):
        """Return the data type used for computations."""
        return self._dtype

    @property
    def center_method(self):
        """Return the centre calculation method."""
        return self._center_method

    # INTERNAL ================================================================

    def _create_run_work_dir(self):
        """
        Create a temporary directory for the current run.

        This method will create a temporal directory inside the working
        directory of the ZobovVF class workdir.

        Returns
        -------
        pathlib.Path
            Path of the working directory for the current run.
        """
        timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
        run_work_dir = pathlib.Path(
            tempfile.mkdtemp(suffix=timestamp, dir=self.workdir)
        )
        return run_work_dir

    def __del__(self):
        """
        Clean up temporary resources when the object is deleted.

        Destructor that cleans up the temporary working directory
        if workdir_clean is True.
        """
        if self._workdir_clean:
            shutil.rmtree(self._workdir)

    def preprocess(self, box):
        """
        Preprocess the data contained in the Box object.

        Placeholder method for data preprocessing.

        Parameters
        ----------
        box : object
            Box object containing data to be preprocessed.

        Returns
        -------
        object
            Preprocessed data.
        """
        return box

    def model_find(self, box):
        """
        Execute the ZOBOV Void Finder algorithm on the provided Box object.

        The execution of ZOBOV involves: write box data into raw files, run
        VOZINIT ---> run VOZSTEP ---> run JOZOV.For a detailed explanation of
        each step see: _wrapper.

        Parameters
        ----------
        box : object
            Box object containing the data box to be analyzed.
        """
        # Retrieve box from Box object
        box = box

        # create the sandbox
        run_work_dir = self._create_run_work_dir()

        # the tracers files
        tracers_raw_file_path = run_work_dir / _Files.TRACERS_RAW
        tracers_txt_file_path = run_work_dir / _Files.TRACERS_TXT

        # write the box in the files

        _wrap.write_input(
            box=box,
            path_executable=_Paths.CURRENT_FILE_PATH
            / _ExecutableNames.ZOBOV_LOADER_BIN,
            raw_file_path=tracers_raw_file_path,
            txt_file_path=tracers_txt_file_path,
        )

        # VOZINIT =============================================================

        _wrap.run_vozinit(
            vozinit_dir_path=pathlib.Path(self._zobov_path) / "src",
            input_file_path=tracers_raw_file_path,
            buffer_size=self.buffer_size,
            box_size=self.box_size,
            number_of_divisions=self.number_of_divisions,
            executable_name=Names.OUTPUT_VOZINIT,
            work_dir_path=run_work_dir,
        )

        # VOZSTEP =============================================================
        # This step is mandatory if VOZINIT was run before

        _wrap.run_voz_step(
            preprocess_dir_path=run_work_dir,
            executable_name=Names.OUTPUT_VOZINIT,
            work_dir_path=run_work_dir,
            voz_executables_path=pathlib.Path(self._zobov_path) / "src",
        )

        # JOZOV ===============================================================
        _wrap.run_jozov(
            jozov_dir_path=pathlib.Path(self._zobov_path) / "src",
            executable_name=Names.OUTPUT_VOZINIT,
            output_name_particles_in_zones=Names.PARTICLES_IN_ZONES,
            output_name_zones_in_void=Names.ZONES_IN_VOID,
            output_name_text_file=Names.OUTPUT_JOZOV_VOIDS,
            density_threshold=self._density_threshold,
            work_dir_path=run_work_dir,
        )
        return {
            "run_work_dir": run_work_dir,
            "box": box,
        }

    def build_voids(self, model_find_parameters):
        """
        Build the final Voids object using specified model parameters.

        This method is used to build the final object Voids (see Voids class
        in this module). Each step will specify a mandatory attribute or
        method of the Voids class.

        Parameters
        ----------
        model_find_parameters : dict
            The dictionary holds some relevant properties from the
            model_find method (see model_find method within this class).
            These properties are needed to run this module:
            - run_work_dir: Directory path where the current run is
            performed.
            - box: Box object (see Box in box module) with the tracers
            information.

        Returns
        -------
        tuple
            A tuple containing:
            - tracers_in_voids: List of particles in each void.
            - centers: Coordinates of the centers of the voids.
            - extra: Dictionary with additional properties about the voids.
        """
        # Center Method:
        center_method = self._center_method
        # Get current working directory
        run_work_dir = model_find_parameters["run_work_dir"]
        # Get box
        box = model_find_parameters["box"]
        # Get properties as dataframe
        df = pd.read_csv(
            run_work_dir / _Files.OUTPUT_JOZOV_VOIDS_DAT,
            delim_whitespace=True,
            header=1,
        )
        # Process 1:
        # a) Parse tracers in zones raw file in the work directory
        _zb_postprocessing.parse_tracers_in_zones_output(
            executable_path=_Paths.CURRENT_FILE_PATH
            / _ExecutableNames.TRACERS_IN_ZONES_BIN,
            input_file_path=run_work_dir / _Files.PARTICLES_VS_ZONES_RAW,
            output_file_path=run_work_dir / _Files.PARTICLES_VS_ZONES_ASCII,
        )
        # b) Parse zones in voids raw file in the work directory
        _zb_postprocessing.parse_zones_in_void_output(
            executable_path=_Paths.CURRENT_FILE_PATH
            / _ExecutableNames.ZONES_IN_VOIDS_BIN,
            input_file_path=run_work_dir / _Files.ZONES_VS_VOID_RAW,
            output_file_path=run_work_dir / _Files.ZONES_VS_VOID_ASCII,
        )
        # Process 2:
        # a) Get Tracers in voids
        # tinv stands for tracers in voids
        prop_df, tracers_in_voids = _zb_postprocessing.get_tracers_in_voids(
            properties_dataframe=df,
            tracers_in_zones_path=(
                run_work_dir / _Files.PARTICLES_VS_ZONES_ASCII
            ),
            zones_in_void_path=run_work_dir / _Files.ZONES_VS_VOID_ASCII,
        )

        # c) Create extra
        extra = {
            "zobov_path": self._zobov_path,
            "properties": prop_df,
            "files_directory_path": run_work_dir,
        }

        # d) Get centers
        if center_method == "barycentre":
            barycentre = _zb_postprocessing.get_center_method("barycentre")
            centers = barycentre(
                tracers_volumes_file_path=(
                    run_work_dir / f"vol{Names.OUTPUT_VOZINIT}.dat"
                ),
                tracers_in_voids=tracers_in_voids,
                box=box,
            )
        elif center_method == "core_particle":
            core_particle = _zb_postprocessing.get_center_method(
                "core_particle"
            )
            centers = core_particle(properties_df=prop_df, box=box)

        return tuple(tracers_in_voids), centers, extra
