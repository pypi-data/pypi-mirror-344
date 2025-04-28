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

"""Installation Helper."""

# =============================================================================
# IMPORTS
# =============================================================================


import os
import pathlib

import sh

from ..settings import SETTINGS


# =============================================================================
# FUNCTIONS
# =============================================================================


def cbl_installation_assistant():
    """
    Assist with the installation of the CBL cleaner method by compiling \
    the shared object.

    This function checks for the existence of the 'libcleaner.so' shared
    object file in the core directory. If not found, it attempts to compile
    and install it using the system's 'make' command with custom settings from
    the global SETTINGS object.

    Notes
    -----
        The MAKEFILE should be located in the core dir of voidfindertk
        alongside the cleaner.cpp module.
    """
    # Path to the voidfindertk directory.
    vftk_path = pathlib.Path(os.path.abspath(__file__)).parent.parent
    # Path to the core directory.
    core_path = vftk_path / "core"
    # Build make command.
    make = sh.Command("make")
    # Attempt to find the .so file if it is missing.
    if not (core_path / "libcleaner.so").is_file():
        print("No libcleaner.so shared object found:\n")
        print("Attempting Installation...")

        # Runs makefile
        make(
            "dirLib=" + SETTINGS.cbl_path,
            _cwd=core_path,
            _out=lambda line: print(line, end=""),
            _err_to_out=True,
        )
