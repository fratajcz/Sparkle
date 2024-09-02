#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Sparkle command to execute a parallel algorithm portfolio."""

import sys
import argparse
import random
import time
import shutil
import csv
import itertools
from pathlib import Path, PurePath

import runrunner as rrr
from runrunner.base import Runner
from runrunner.slurm import Status

from sparkle.CLI.help.reporting_scenario import Scenario
from sparkle.CLI.help import logging as sl
from sparkle.CLI.help import global_variables as gv
from sparkle.platform import CommandName, COMMAND_DEPENDENCIES
from sparkle.CLI.initialise import check_for_initialise
from sparkle.CLI.help import argparse_custom as ac
from sparkle.CLI.help.nicknames import resolve_object_name
from sparkle.types.objective import PerformanceMeasure
from sparkle.platform.settings_objects import Settings, SettingState
from sparkle.solver import Solver
from sparkle.instance import instance_set, InstanceSet
from sparkle.types import SolverStatus


def run_parallel_portfolio(instances_set: InstanceSet,
                           portfolio_path: Path,
                           solvers: list[Solver],
                           run_on: Runner = Runner.SLURM) -> None:
    """Run the parallel algorithm portfolio.

    Args:
        instances_set: Set of instances to run on.
        portfolio_path: Path to the parallel portfolio.
        solvers: List of solvers to run on the instances.
        run_on: Currently only supports Slurm.
    """
    num_solvers, num_instances = len(solvers), len(instances_set._instance_paths)
    seeds_per_solver = gv.settings().get_parallel_portfolio_number_of_seeds_per_solver()
    num_jobs = num_solvers * num_instances * seeds_per_solver
    parallel_jobs = min(gv.settings().get_number_of_jobs_in_parallel(), num_jobs)
    if parallel_jobs > num_jobs:
        print("WARNING: Not all jobs will be started at the same time due to the "
              "limitation of number of Slurm jobs that can be run in parallel. Check"
              " your Sparkle Slurm Settings.")
    print(f"Sparkle parallel portfolio is running {seeds_per_solver} seed(s) per solver "
          f"on {num_solvers} solvers for {num_instances} instances ...")
    cmd_list = []
    cutoff = gv.settings().get_general_target_cutoff_time()
    objectives = gv.settings().get_general_sparkle_objectives()
    # Create a command for each instance-solver-seed combination
    for instance, solver in itertools.product(instances_set._instance_paths, solvers):
        for _ in range(seeds_per_solver):
            seed = int(random.getrandbits(32))
            solver_call_list = solver.build_cmd(
                instance.absolute(),
                objectives=objectives,
                seed=seed,
                cutoff_time=cutoff)
            cmd_list.append((" ".join(solver_call_list)).replace("'", '"'))
    # Jobs are added in to the runrunner object in the same order they are provided
    sbatch_options = gv.settings().get_slurm_extra_options(as_args=True)
    run = rrr.add_to_queue(
        runner=run_on,
        cmd=cmd_list,
        name=CommandName.RUN_PARALLEL_PORTFOLIO,
        parallel_jobs=parallel_jobs,
        path=portfolio_path,
        base_dir=sl.caller_log_dir,
        srun_options=["-N1", "-n1"] + sbatch_options,
        sbatch_options=sbatch_options
    )
    check_interval = gv.settings().get_parallel_portfolio_check_interval()
    instances_done = [False] * num_instances
    # We record the 'best' of all seed results per solver-instance
    job_output_dict = {instance_name: {solver.name: {"cpu_time": float(sys.maxsize),
                                                     "wc_time": float(sys.maxsize),
                                                     "status": SolverStatus.UNKNOWN}
                                       for solver in solvers}
                       for instance_name in instances_set._instance_names}
    n_instance_jobs = num_solvers * seeds_per_solver
    while not all(instances_done):
        time.sleep(check_interval)
        job_status_list = [r.status for r in run.jobs]
        job_status_completed = [status == Status.COMPLETED for status in job_status_list]
        # The jobs are sorted by instance
        for i, instance in enumerate(instances_set._instance_paths):
            if instances_done[i]:
                continue
            instance_job_slice = slice(i * n_instance_jobs, (i + 1) * n_instance_jobs)
            if any(job_status_completed[instance_job_slice]):
                instances_done[i] = True
                # Kill all running jobs for this instance
                solver_kills = [0] * num_solvers
                for job_index in range(i * n_instance_jobs, (i + 1) * n_instance_jobs):
                    if not job_status_completed[job_index]:
                        run.jobs[job_index].kill()
                        solver_index = int(
                            (job_index % n_instance_jobs) / seeds_per_solver)
                        solver_kills[solver_index] += 1
                for solver_index in range(num_solvers):
                    # All seeds of a solver were killed on instance, set state to killed
                    if solver_kills[solver_index] == seeds_per_solver:
                        solver_name = solvers[solver_index].name
                        job_output_dict[instance.name][solver_name]["status"] =\
                            SolverStatus.KILLED

    # Now iterate over runsolver logs to get runtime, get the lowest value per seed
    for index, cmd in enumerate(cmd_list):
        runsolver_configuration = cmd.split(" ")[:11]
        solver_output = Solver.parse_solver_output(run.jobs[i].stdout,
                                                   runsolver_configuration,
                                                   portfolio_path)
        solver_index = int((index % n_instance_jobs) / seeds_per_solver)
        solver_name = solvers[solver_index].name
        instance_name = instances_set._instance_names[int(index / n_instance_jobs)]
        if "cpu_time" not in solver_output:
            cpu_time, wc_time = -1.0, -1.0
        else:
            cpu_time, wc_time = solver_output["cpu_time"], solver_output["wc_time"]
        if cpu_time < job_output_dict[instance_name][solver_name]["cpu_time"]:
            job_output_dict[instance_name][solver_name]["cpu_time"] = cpu_time
            job_output_dict[instance_name][solver_name]["wc_time"] = wc_time
            if (job_output_dict[instance_name][solver_name]["status"]
                    != SolverStatus.KILLED):
                job_output_dict[instance_name][solver_name]["status"] =\
                    solver_output["status"]

    # Fix the CPU/WC time for non existent logs to instance min time + check_interval
    for instance in job_output_dict.keys():
        no_log_solvers = []
        min_time = cutoff
        for solver in job_output_dict[instance].keys():
            if job_output_dict[instance][solver]["cpu_time"] == -1.0:
                no_log_solvers.append(solver)
            elif job_output_dict[instance][solver]["cpu_time"] < min_time:
                min_time = job_output_dict[instance][solver]["cpu_time"]
        for solver in no_log_solvers:
            job_output_dict[instance][solver]["cpu_time"] = min_time + check_interval
            job_output_dict[instance][solver]["wc_time"] = min_time + check_interval

    for index, instance_name in enumerate(instances_set._instance_names):
        index_str = f"[{index + 1}/{num_instances}] "
        instance_output = job_output_dict[instance_name]
        if all([instance_output[k]["status"] == SolverStatus.TIMEOUT
                for k in instance_output.keys()]):
            print(f"\n{index_str}{instance_name} was not solved within the cutoff-time.")
            continue
        print(f"\n{index_str}{instance_name} yielded the following Solver results:")
        for sindex in range(index * num_solvers, (index + 1) * num_solvers):
            solver_name = solvers[sindex % num_solvers].name
            job_info = job_output_dict[instance_name][solver_name]
            print(f"\t- {solver_name} ended with status {job_info['status']} in "
                  f"{job_info['cpu_time']}s CPU-Time ({job_info['wc_time']}s WC-Time)")

    # Write the results to a CSV
    csv_path = portfolio_path / "results.csv"
    with csv_path.open("w") as out:
        writer = csv.writer(out)
        for instance_name in job_output_dict.keys():
            for solver_name in job_output_dict[instance_name].keys():
                job_o = job_output_dict[instance_name][solver_name]
                writer.writerow((instance_name, solver_name,
                                 job_o["status"], job_o["cpu_time"], job_o["wc_time"]))


def parser_function() -> argparse.ArgumentParser:
    """Define the command line arguments.

    Returns:
        parser: The parser with the parsed command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(*ac.InstancePath.names,
                        **ac.InstancePath.kwargs)
    parser.add_argument(*ac.NicknamePortfolioArgument.names,
                        **ac.NicknamePortfolioArgument.kwargs)
    parser.add_argument(*ac.SolversArgument.names,
                        **ac.SolversArgument.kwargs)
    parser.add_argument(*ac.PerformanceMeasureSimpleArgument.names,
                        **ac.PerformanceMeasureSimpleArgument.kwargs)
    parser.add_argument(*ac.CutOffTimeArgument.names,
                        **ac.CutOffTimeArgument.kwargs)
    parser.add_argument(*ac.SolverSeedsArgument.names,
                        **ac.SolverSeedsArgument.kwargs)
    parser.add_argument(*ac.RunOnArgument.names,
                        **ac.RunOnArgument.kwargs)
    parser.add_argument(*ac.SettingsFileArgument.names,
                        **ac.SettingsFileArgument.kwargs)
    return parser


if __name__ == "__main__":
    # Log command call
    sl.log_command(sys.argv)

    # Define command line arguments
    parser = parser_function()

    # Process command line arguments
    args = parser.parse_args()
    if args.solvers is not None:
        solver_paths = [resolve_object_name("".join(s),
                                            target_dir=gv.settings().DEFAULT_solver_dir)
                        for s in args.solvers]
        if None in solver_paths:
            print("Some solvers not recognised! Check solver names:")
            for i, name in enumerate(solver_paths):
                if solver_paths[i] is None:
                    print(f'\t- "{solver_paths[i]}" ')
            sys.exit(-1)
        solvers = [Solver(p) for p in solver_paths]
    else:
        solvers = [Solver(p) for p in
                   gv.settings().DEFAULT_solver_dir.iterdir() if p.is_dir()]

    check_for_initialise(COMMAND_DEPENDENCIES[CommandName.RUN_PARALLEL_PORTFOLIO])

    # Compare current settings to latest.ini
    prev_settings = Settings(PurePath("Settings/latest.ini"))
    Settings.check_settings_changes(gv.settings(), prev_settings)

    # Do first, so other command line options can override settings from the file
    if args.settings_file is not None:
        gv.settings().read_settings_ini(args.settings_file, SettingState.CMD_LINE)

    portfolio_path = args.portfolio_name

    if args.run_on is not None:
        gv.settings().set_run_on(
            args.run_on.value, SettingState.CMD_LINE)
    run_on = gv.settings().get_run_on()

    if args.solver_seeds is not None:
        gv.settings().set_parallel_portfolio_number_of_seeds_per_solver(
            args.solver_seeds, SettingState.CMD_LINE)

    if run_on == Runner.LOCAL:
        print("Parallel Portfolio is not fully supported yet for Local runs. Exiting.")
        sys.exit(-1)

    # Retrieve instance set
    data_set = resolve_object_name(
        args.instance_path,
        gv.file_storage_data_mapping[gv.instances_nickname_path],
        gv.settings().DEFAULT_instance_dir,
        instance_set)
    print(f"Running on {data_set.size} instance(s)...")

    if args.cutoff_time is not None:
        gv.settings().set_general_target_cutoff_time(args.cutoff_time,
                                                     SettingState.CMD_LINE)

    if args.performance_measure is not None:
        gv.settings().set_general_sparkle_objectives(
            args.performance_measure, SettingState.CMD_LINE)
    if gv.settings().get_general_sparkle_objectives()[0].PerformanceMeasure\
            is not PerformanceMeasure.RUNTIME:
        print("ERROR: Parallel Portfolio is currently only relevant for "
              f"{PerformanceMeasure.RUNTIME} measurement. In all other cases, "
              "use validation")
        sys.exit(-1)

    if args.portfolio_name is not None:  # Use a nickname
        portfolio_path = gv.settings().DEFAULT_parallel_portfolio_output_raw /\
            args.portfolio_name
    else:  # Generate a timestamped nickname
        timestamp = time.strftime("%Y-%m-%d-%H:%M:%S", time.gmtime(time.time()))
        randintstamp = int(random.getrandbits(32))
        portfolio_path = gv.settings().DEFAULT_parallel_portfolio_output_raw /\
            f"{timestamp}_{randintstamp}"
    if portfolio_path.exists():
        print(f"[WARNING] Portfolio path {portfolio_path} already exists! "
              "Overwrite? [y/n] ", end="")
        user_input = input()
        if user_input != "y":
            sys.exit()
        shutil.rmtree(portfolio_path)
    portfolio_path.mkdir(parents=True)
    run_parallel_portfolio(data_set, portfolio_path, solvers, run_on=run_on)

    # Update latest scenario
    gv.latest_scenario().set_parallel_portfolio_path(portfolio_path)
    gv.latest_scenario().set_latest_scenario(Scenario.PARALLEL_PORTFOLIO)
    gv.latest_scenario().set_parallel_portfolio_instance_path(args.instance_path)
    # Write used scenario to file
    gv.latest_scenario().write_scenario_ini()
    # Write used settings to file
    gv.settings().write_used_settings()
    print("Running Sparkle parallel portfolio is done!")
