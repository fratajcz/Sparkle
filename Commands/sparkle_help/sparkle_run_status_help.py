#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Helper functions to communicate run statuses of various commands."""

from pathlib import Path

from Commands.sparkle_help import sparkle_global_help as sgh
from Commands.sparkle_help import sparkle_job_help as sjh
from Commands.sparkle_help import sparkle_file_help as sfh
from Commands.Structures.status_info import (SolverRunStatusInfo, StatusInfoType,
                                             ConfigureSolverStatusInfo,
                                             ConstructParallelPortfolioStatusInfo,
                                             ConstructPortfolioSelectorStatusInfo,
                                             GenerateReportStatusInfo)
from Commands.sparkle_help.sparkle_command_help import CommandName


def get_jobs_for_command(jobs: list[dict[str, str, str]], command: str) \
        -> list[dict[str, str, str]]:
    """Filter jobs by a command.

    Args:
      jobs: List of jobs
      command: The command to filter for

    Returns:
      Jobs that belong to the given command.
    """
    return [x for x in jobs if x["command"] == command]


def get_running_jobs_for_command(command: CommandName) -> str:
    """Print all the running jobs.

    Args:
        command: name of the command to search for.

    Returns:
        string with job ids.
    """
    sjh.cleanup_active_jobs()
    jobs = sjh.read_active_jobs()

    command_jobs = get_jobs_for_command(jobs, command.name)
    command_jobs_ids = " ".join([x["job_id"] for x in command_jobs])

    return command_jobs_ids


def print_running_solver_jobs() -> None:
    """Print a list of currently active run solver job."""
    command = CommandName.RUN_SOLVERS
    command_jobs_ids = get_running_jobs_for_command(command)
    tmp_directory = f"{sgh.sparkle_tmp_path}/{StatusInfoType.SOLVER_RUN}/"
    list_all_statusinfo_filename = sfh.get_list_all_statusinfo_filename(tmp_directory)
    if len(command_jobs_ids) > 0:
        print(f"The command {command} is running "
              f"with job IDs {command_jobs_ids}")
        if len(list_all_statusinfo_filename) > 0:
            print("Running solver jobs:")
            for statusinfo_filename in list_all_statusinfo_filename:
                statusinfo_filepath = Path(
                    tmp_directory
                    + sfh.get_last_level_directory_name(statusinfo_filename))
                status_info = SolverRunStatusInfo.from_file(statusinfo_filepath)
                print(f"Start Time: {status_info.get_start_time()}")
                print(f"Solver: {status_info.get_solver()}")
                print(f"Instance: {status_info.get_instance()}")
                print()
    else:
        print("No running solver jobs")


def print_running_configuration_jobs() -> None:
    """Print a list of currently active run solver job."""
    command = CommandName.CONFIGURE_SOLVER
    command_jobs_ids = get_running_jobs_for_command(command)
    tmp_directory = f"{sgh.sparkle_tmp_path}/{StatusInfoType.CONFIGURE_SOLVER}/"
    list_all_statusinfo_filename = sfh.get_list_all_statusinfo_filename(tmp_directory)
    if len(command_jobs_ids) > 0:
        print(f"The command {command} is running "
              f"with job IDs {command_jobs_ids}")
        if len(list_all_statusinfo_filename) > 0:
            print("Running configuration jobs:")
            for statusinfo_filename in list_all_statusinfo_filename:
                statusinfo_filepath = Path(
                    tmp_directory
                    + sfh.get_last_level_directory_name(statusinfo_filename))
                status_info = ConfigureSolverStatusInfo.from_file(statusinfo_filepath)
                print(f"Start Time: {status_info.get_start_time()}")
                print(f"Solver: {status_info.get_solver()}")
                print(f"Instance set test: {status_info.get_instance_set_test()}")
                print(f"Instance set train: {status_info.get_instance_set_train()}")
                print()
    else:
        print("No running configuration jobs")


def print_running_parallel_portfolio_construction_jobs() -> None:
    """Print a list of currently active pap construction jobs."""
    command = CommandName.CONSTRUCT_SPARKLE_PARALLEL_PORTFOLIO
    command_jobs_ids = get_running_jobs_for_command(command)
    tmp_directory = (f"{sgh.sparkle_tmp_path}/"
                     f"{StatusInfoType.CONSTRUCT_PARALLEL_PORTFOLIO}/")
    list_all_statusinfo_filename = sfh.get_list_all_statusinfo_filename(tmp_directory)
    if len(command_jobs_ids) > 0:
        print(f"The command {command} is running "
              f"with job IDs {command_jobs_ids}")
        if len(list_all_statusinfo_filename) > 0:
            print("Running parallel portfolio construction jobs:")
            for statusinfo_filename in list_all_statusinfo_filename:
                statusinfo_filepath = Path(
                    tmp_directory
                    + sfh.get_last_level_directory_name(statusinfo_filename))
                status_info = (ConstructParallelPortfolioStatusInfo
                               .from_file(statusinfo_filepath))
                print(f"Start Time: {status_info.get_start_time()}")
                print(f"Portfolio Name: {status_info.get_portfolio_name()}")
                print(f"Solver List: {str(status_info.get_list_of_solvers())}")
                print()
    else:
        print("No running parallel portfolio construction jobs")


def print_running_portfolio_selector_construction_jobs() -> None:
    """Print a list of currently active ps construction jobs."""
    command = CommandName.CONSTRUCT_SPARKLE_PORTFOLIO_SELECTOR
    command_jobs_ids = get_running_jobs_for_command(command)
    tmp_directory = (f"{sgh.sparkle_tmp_path}/"
                     f"{StatusInfoType.CONSTRUCT_PORTFOLIO_SELECTOR}/")
    list_all_statusinfo_filename = sfh.get_list_all_statusinfo_filename(tmp_directory)
    if len(command_jobs_ids) > 0:
        print(f"The command {command} is running "
              f"with job IDs {command_jobs_ids}")
        if len(list_all_statusinfo_filename) > 0:
            print("Running portfolio selector construction jobs:")
            for statusinfo_filename in list_all_statusinfo_filename:
                statusinfo_filepath = Path(
                    tmp_directory
                    + sfh.get_last_level_directory_name(statusinfo_filename))
                status_info = (ConstructPortfolioSelectorStatusInfo
                               .from_file(statusinfo_filepath))
                print(f"Start Time: {status_info.get_start_time()}")
                print(f"Algorithm Selector: {status_info.get_algorithm_selector_path()}")
                print(f"Feature data csv: "
                      f"{str(status_info.get_feature_data_csv_path())}")
                print(f"Performance data csv: "
                      f"{str(status_info.get_performance_data_csv_path())}")
                print()
    else:
        print("No running portfolio selector construction jobs")


def print_running_generate_report_jobs() -> None:
    """Print a list of currently active generate report jobs."""
    tmp_directory = (f"{sgh.sparkle_tmp_path}/"
                     f"{StatusInfoType.GENERATE_REPORT}/")
    list_all_statusinfo_filename = sfh.get_list_all_statusinfo_filename(tmp_directory)
    if len(list_all_statusinfo_filename) > 0:
        print("Running generate report jobs:")
        for statusinfo_filename in list_all_statusinfo_filename:
            statusinfo_filepath = Path(
                tmp_directory
                + sfh.get_last_level_directory_name(statusinfo_filename))
            status_info = (GenerateReportStatusInfo
                           .from_file(statusinfo_filepath))
            print(f"Start Time: {status_info.get_start_time()}")
            print(f"Report Type: {status_info.get_report_type()}")
            print()
    else:
        print("No running generate report jobs")
