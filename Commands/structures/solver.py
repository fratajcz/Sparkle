#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Class to handle a solver and its directories."""

from __future__ import annotations
import sys
import fcntl
import ast
from pathlib import Path


class Solver:
    """Class to handle a solver and its directories."""
    solver_dir = Path("Solvers/")
    solver_list_path = Path("Reference_Lists/") / "sparkle_solver_list.txt"

    def __init__(self: Solver, solver_directory: Path) -> None:
        """Initialize solver.

        Args:
            solver_directory: Directory of the solver.
        """
        self.directory = solver_directory
        self.name = solver_directory.name

    def get_pcs_file(self: Solver) -> Path:
        """Get path of the parameter file.

        Returns:
            Path to the parameter file.
        """
        file_count = 0
        file_name = ""
        for file_path in self.directory.iterdir():
            file_extension = "".join(file_path.suffixes)

            if file_extension == ".pcs":
                file_name = file_path.name
                file_count += 1

        if file_count != 1:
            print("None or multiple .pcs files found. Solver "
                  "is not valid for configuration.")
            sys.exit(-1)

        return self.directory / file_name

    # TODO: This information should be stored in the solver as an attribute too.
    # That will allow us to at least skip this method.
    def is_deterministic(self: Solver) -> str:
        """Return a string indicating whether a given solver is deterministic or not.

        Returns:
            A string containing 0 or 1 indicating whether solver is deterministic.
        """
        deterministic = ""
        target_solver_path = "Solvers/" + self.name
        for solver in Solver.get_solver_list():
            solver_line = solver.strip().split()
            if (solver_line[0] == target_solver_path):
                deterministic = solver_line[1]
                break

        return deterministic

    @staticmethod
    def get_solver_by_name(name: str) -> Solver:
        """Attempt to resolve the solver object by name.

        Args:
            name: The name of the solver

        Returns:
            A Solver object if found, None otherwise
        """
        if (Solver.solver_dir / name).exists():
            return Solver(Solver.solver_dir / name)
        return None

    @staticmethod
    def get_solver_list() -> list[str]:
        """Get solver list from file."""
        if Solver.solver_list_path.exists():
            with Solver.solver_list_path.open("r+") as fo:
                fcntl.flock(fo.fileno(), fcntl.LOCK_EX)
                return ast.literal_eval(fo.read())
        return []
