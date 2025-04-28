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

"""Wrapper functions for the ZOBOV void finder."""

# =============================================================================
# IMPORTS
# =============================================================================
import ctypes
import os
import shutil

import numpy as np

import sh


def _move_inputs(src, dst_dir):
    """Move input files to the destination directory if necessary.

    Parameters
    ----------
    src : str
        Path to the source file.
    dst_dir : str
        Path to the destination directory.

    Returns
    -------
    str
        Path to the moved or original file.

    Notes
    -----
    This function checks if the source file is already in the destination
    directory. If so, it returns the source path unchanged. Otherwise, it
    copies the file to the specified destination.
    """
    src_dir = os.path.dirname(src)
    if src_dir == dst_dir:
        return src
    return shutil.copy2(src, dst_dir)


# =============================================================================
# VOZ INIT
# =============================================================================


def run_vozinit(
    *,
    vozinit_dir_path,
    input_file_path,
    buffer_size,
    box_size,
    number_of_divisions,
    executable_name,
    work_dir_path,
):
    """
    Run the vozinit command of the ZOBOV void finder.

    This function initializes the vozinit process, which provides insights
    into the partitioning of a simulation, checks guard point sufficiency,
    and generates a script for the subsequent "voz" step.

    As a result of the vozinit process, a script file is created. This
    script is used to run voz1b1 on each sub-box and then the voztie
    executable.

    Parameters
    ----------
    vozinit_dir_path : str
        Path to the directory containing the vozinit executable.
    input_file_path : str
        Path to the tracers input file.
    buffer_size : float
        Size of the buffer, in units such that the box size of the data
        cube is 1.
    box_size : float
        The range of positions of particles in each dimension.
    number_of_divisions : int
        Number of divisions (default 2). Must be at least 2; determines
        the number of partitions in each dimension.
    executable_name : str
        Suffix label for the output files.
    work_dir_path : str
        Path to the working directory.

    Returns
    -------
    str
        Output of the vozinit process.

    Notes
    -----
    This function leverages the `sh` module to execute the vozinit
    command in the specified working directory and returns the output.

    """
    vozinit = sh.Command("vozinit", search_paths=[vozinit_dir_path])

    params = (
        input_file_path,
        buffer_size,
        box_size,
        number_of_divisions,
        executable_name,
    )

    args = [str(param) for param in params]

    vozinit(
        *args,
        _cwd=work_dir_path,
        _out=lambda line: print(line, end=""),
        _err_to_out=True,
    )


# =============================================================================
# VOZ STEP : VOZ1B1 + VOZTIE
# =============================================================================


def run_voz_step(
    *,
    preprocess_dir_path,
    executable_name,
    work_dir_path,
    voz_executables_path,
):
    """
    Runs vozinit executable.

    Use this method only if vozinit was executed before. The executable
    created by vozinit has the suffix provided in the vozinit step and the
    prefix "src". This script runs voz1b1 using the different slices of the
    box obtained from the vozinit step, where the Voronoi tessellation is
    performed in each subcube division of the dataset. The script then runs
    voztie to tie the subdivision boxes together.

    To perform this task, voz1b1 and voztie executables are needed in the
    working directory.

    Parameters
    ----------
    preprocess_dir_path : str
        Path to the directory containing the vozinit executable.
    executable_name : str
        Suffix of the executable file.
    work_dir_path : str
        Path to the working directory.
    voz_executables_path : str
        Path of the voz - 1b1 / tie (voz1b1/voztie) executables.

    Returns
    -------
    str
        Output of the voz1b1 and voztie executions.

    Notes
    -----
    This function relies on moving the necessary files to run the
    src-executable and executing it in the specified working directory.

    """
    # Moving necesary files to run the src-executable
    _move_inputs(voz_executables_path / "voz1b1", work_dir_path)
    _move_inputs(voz_executables_path / "voztie", work_dir_path)

    full_executable_name = preprocess_dir_path / f"scr{executable_name}"
    preprocess = sh.Command(str(full_executable_name))

    preprocess(
        _cwd=work_dir_path,
        _out=lambda line: print(line, end=""),
        _err_to_out=True,
    )


# =============================================================================
# VOZ 1b1
# =============================================================================


def run_voz1b1(
    *,
    input_file_path,
    buffer_size,
    box_size,
    executable_name,
    number_of_divisions,
    binary_division,
    voz1b1_dir_path,
    work_dir_path,
):
    """
    Runs the VOZ1B1 executable with specified parameters.

    This program (VOZ one-by-one) calculates the Voronoi diagram on one
    sub-box of the data cube. Ideally, one would not have to use the input
    parameters, since they would be set in the vozinit script file, but one
    argument might have to be changed if a guard point is encountered while
    diagramming one of the sub-boxes. Only the sub-box(es) encountering
    guard particles need be rediagrammed.

    The output of voz1b1 is a file containing the Voronoi adjacencies and
    volumes of particles in the sub-box: part.%s.%02d.%02d.%02d, where %s
    is the "suffix," and the %02d's are the three two-digit labels
    identifying the sub-box.

    Parameters
    ----------
    input_file_path : str
        Path to the input file.
    buffer_size : int
        Sets the size, in units such that the box size of the data cube is 1.
    box_size : int
        Max value of the tracers in each x, y, z coordinates.
    executable_name : str
        Suffix of the created executable.
    number_of_divisions : int
        The number of partitions in each dimension; must be at least 2
        (giving 8 sub-boxes).
    binary_division : tuple
        Tuple of 3 integers representing binary divisions.
    voz1b1_dir_path : str
        Path to the voz1b1 executable directory.
    work_dir_path : str
        Path to the working directory.

    Returns
    -------
    str
        Output of the voz1b1 run.
    """
    voz1b1 = sh.Command("voz1b1", search_paths=[voz1b1_dir_path])

    params = [
        input_file_path,
        buffer_size,
        box_size,
        executable_name,
        number_of_divisions,
        binary_division[0],
        binary_division[1],
        binary_division[2],
    ]

    args = [str(param) for param in params]

    voz1b1(
        *args,
        _cwd=work_dir_path,
        _out=lambda line: print(line, end=""),
        _err_to_out=True,
    )


# =============================================================================
# VOZ TIE
# =============================================================================


def run_voztie(
    *,
    number_of_divisions,
    executable_name,
    voztie_dir_path,
    work_dir_path,
):
    """Run the VOZTIE executable with specified parameters.

    This program ties the sub-boxes together, returning single adjacency
    (adj%s.dat, where %s is the "suffix,") and volume (vol%s.dat) files
    for the whole datacube. The volume file is formatted simply in C
    (not Fortran77) format: it consists of a 4-byte integer containing the
    number of particles, followed by an array of 4-byte floats containing
    each particle volume. The adjacency file is formatted in a more
    complicated manner to reduce its size from the doubly linked list used
    within the code.

    This program (JOin ZOnes to form Voids) first finds "zones" (one for
    each density minimum) and then links them together in the manner
    described in the paper.

    Parameters
    ----------
    number_of_divisions : int
        Number of divisions, min: 2.
    executable_name : str
        Suffix of the executable.
    voztie_dir_path : str
        Path to the VOZTIE directory.
    work_dir_path : str
        Path to the working directory.

    Returns
    -------
    str
        Output of the sh voztie run.
    """
    voztie = sh.Command("voztie", search_paths=[voztie_dir_path])

    params = [
        number_of_divisions,
        executable_name,
    ]
    args = [str(param) for param in params]
    voztie(
        *args,
        _cwd=work_dir_path,
        _out=lambda line: print(line, end=""),
        _err_to_out=True,
    )


def run_jozov(
    *,
    jozov_dir_path,
    executable_name,
    output_name_particles_in_zones,
    output_name_zones_in_void,
    output_name_text_file,
    density_threshold,
    work_dir_path,
):
    """Run the JOZOV executable to link zones and form voids.

    This program (JOin ZOnes to form Voids) first finds "zones"
    (one for each density minimum) and then links them together.
    The density threshold is an optional parameter, which can limit
    the growth of voids into high-density regions.

    There are 3 outputs of jozov: a zone membership file which
    contains the particles in each zone; a void membership file
    containing the zones in each void, and a text file. For the
    format of the first two files, please see the code. Here is an
    example text file. The results may not be typical, because the
    simulation they come from has very low mass resolution.

    Parameters
    ----------
    jozov_dir_path : str
        Path to the directory containing the jozov executable.
    executable_name : str
        Corpus name of the executable files with suffix adj/vol.
        These are the adjacency and volume input files of the run.
    output_name_particles_in_zones : str
        Name of the output file containing particles vs zones.
    output_name_zones_in_void : str
        Name of the output file containing zones vs voids.
    output_name_text_file : str
        Name of the main parameters output text file.
    density_threshold : float
        Density threshold (0 for no threshold).
    work_dir_path : str
        Path to the working directory.

    Returns
    -------
    str
        Output of the jozov run.
    """
    jozov = sh.Command("jozov", search_paths=[jozov_dir_path])

    args = (
        f"adj{executable_name}.dat",
        f"vol{executable_name}.dat",
        f"{output_name_particles_in_zones}.dat",
        f"{output_name_zones_in_void}.dat",
        f"{output_name_text_file}.dat",
        f"{density_threshold}",
    )
    jozov(
        *args,
        _cwd=work_dir_path,
        _out=lambda line: print(line, end=""),
        _err_to_out=True,
    )


def write_input(*, box, path_executable, raw_file_path, txt_file_path):
    """
    Generate input files for the ZOBOV void finder from the Box object.

    Create the position file used in the ZOBOV void finder from the input
    Box object of tracers.

    This function generates a position file containing the positions of
    all particles. By default, this is a Fortran 77-formatted file,
    structured as follows:

    open(unit=1, file=outname, form='unformatted')
    write(1) num_particles
    write(1) (x(i),i=1,num_particles)
    write(1) (y(i),i=1,num_particles)
    write(1) (z(i),i=1,num_particles)
    close(1)

    The module will create two files:
        "tracers_zobov.raw": Contains the parsed raw contents of the Box
        object and is used to run the ZOBOV finder.
        "tracers_zobov.txt": Contains the same data in ASCII format for
        better readability.

    Parameters
    ----------
    box : object
        Input box object containing x, y, z, vx, vy, vz, and m.
    path_executable : str
        Path to the executable file.
    raw_file_path : str
        Path to the raw file output directory.
    txt_file_path : str
        Path to the text file output directory.

    Returns
    -------
    None
    """
    # Create input binary files for Zobov finder

    # Declare library path
    clibrary = ctypes.CDLL(str(path_executable), mode=ctypes.RTLD_GLOBAL)

    # Create Input Pointers for x,y,z
    arr_pointer = 3 * [
        np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags=["CONTIGUOUS"])
    ]

    # Declare Input Pointers type
    clibrary.c_binary_writter.argtypes = arr_pointer + [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]

    # Fill Input
    clibrary.c_binary_writter(
        box.arr_.x,
        box.arr_.y,
        box.arr_.z,
        # box.vx,
        # box.vy,
        # box.vz,
        # box.m,
        len(box),
        str(raw_file_path).encode("utf-8"),
        str(txt_file_path).encode("utf-8"),
    )
