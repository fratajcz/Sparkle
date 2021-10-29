#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Software: 	Sparkle (Platform for evaluating empirical algorithms/solvers)
'''

import sys
import os
import argparse
from pathlib import Path

from sparkle_help import sparkle_logging as sl
from sparkle_help import sparkle_settings
from sparkle_help import sparkle_global_help as sgh
from sparkle_help.reporting_scenario import ReportingScenario
from sparkle_help import argparse_custom as ac
from sparkle_help.sparkle_settings import SettingState, processMonitoring
from sparkle_help import sparkle_run_parallel_portfolio_help as srpp
from sparkle_help import sparkle_file_help as sfh
from sparkle_help.sparkle_settings import PerformanceMeasure


if __name__ == r'__main__':
    # Initialise settings
    global settings
    sgh.settings = sparkle_settings.Settings()

    # Initialise latest scenario
    global latest_scenario
    sgh.latest_scenario = ReportingScenario()

    # Log command call
    sl.log_command(sys.argv)

    # Define command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance-paths', default=sgh.instance_list, metavar='N',
                        nargs="+", type=str, action=ac.SetByUser,
                        help='Specify the instance_path(s) on which the portfolio will '
                             'run. This can be a space-separated list of instances '
                             'contain instance sets and/or singular instances. For '
                             'example --instance-paths Instances/PTN/Ptn-7824-b01.cnf '
                             'Instances/PTN2/')
    parser.add_argument('--portfolio-name',
                        default=sgh.latest_scenario.get_parallel_portfolio_path(),
                        type=str, action=ac.SetByUser,
                        help='Specify the name of the portfolio. If the portfolio is not'
                             ' in the standard folder, use its full path, the default '
                             'location is Sparkle_Parallel_Portfolio/. If the option is '
                             'not specified, the latest constructed portfolio will be '
                             'selected.')
    parser.add_argument('--process-monitoring', choices=processMonitoring.__members__,
                        default=sgh.settings.get_parallel_portfolio_process_monitoring(),
                        action=ac.SetByUser,
                        help='Specify whether the monitoring of the portfolio should '
                             'cancel all solvers within a portfolio once a solver '
                             'finishes (realistic). Or allow all solvers within a '
                             'portfolio to get an equal chance to have the shortest '
                             'running time on an instance(extended). The default option '
                             'is realistic.')
    parser.add_argument('--performance-measure', choices=PerformanceMeasure.__members__,
                        default=sgh.settings.get_general_performance_measure(),
                        action=ac.SetByUser,
                        help='the performance measure, e.g. runtime (for decision '
                             'algorithms) or qualty_absolute (for optimisation '
                             'algorithms)')
    parser.add_argument("--cutoff-time",
                        default=sgh.settings.get_general_target_cutoff_time(), type=int,
                        action=ac.SetByUser,
                        help='The duration the portfolio will run before the solvers '
                             'within the portfolio will be stopped')
    parser.add_argument('--settings-file', type=Path,
                        default=sgh.settings.DEFAULT_settings_path, action=ac.SetByUser,
                        help='specify the settings file to use instead of the default')

    # Process command line arguments
    args = parser.parse_args()

    # Do first, so other command line options can override settings from the file
    if ac.set_by_user(args, 'settings_file'):
        sgh.settings.read_settings_ini(args.settings_file, SettingState.CMD_LINE)

    if ac.set_by_user(args, 'portfolio_name'):

        if(os.path.isdir(args.portfolio_name)):
            portfolio_path = args.portfolio_name
        else:
            portfolio_path = Path('Sparkle_Parallel_Portfolio/' + args.portfolio_name)

            if(not os.path.isdir(portfolio_path)):
                sys.exit("c Portfolio not found, aborting the process")
    else:
        portfolio_path = args.portfolio_name

    if ac.set_by_user(args, 'instance_paths'):
        instance_paths = []

        for instance in args.instance_paths:
            if(os.path.isdir(instance)):
                print(f'c Added {str(len(os.listdir(instance)))} instance(s) from '
                      f'directory {str(instance)}')
                for item in os.listdir(instance):
                    item_with_dir = str(instance) + str(item)
                    instance_paths.append(str(item_with_dir))
            elif(os.path.isfile(instance)):
                print('c Added instance ' + str(instance))
                instance_paths.append(str(instance))
            else:
                instance_with_dir = 'Instances/' + instance
                if(os.path.isdir(instance_with_dir)):
                    print(f'c Added {str(len(os.listdir(instance_with_dir)))} '
                          f'instance(s) from directory {str(instance)}')
                    for item in os.listdir(instance_with_dir):
                        item_with_dir = 'Instances/' + str(instance) + '/' + str(item)
                        instance_paths.append(str(item_with_dir))
    else:
        if(args.instance_paths is None):
            sys.exit("c Instances not found, aborting the process")
        instance_paths = args.instance_paths
        if(os.path.isfile(sgh.used_instance_list_file)):
            temp = [i for i in instance_paths
                    if i not in sfh.get_used_instance_list_from_file('Instances/')]
            instance_paths = temp
        if(len(instance_paths) == 0):
            sys.exit("c No unused instances found, aborting the process")

    if ac.set_by_user(args, 'cutoff_time'):
        sgh.settings.set_general_target_cutoff_time(args.cutoff_time,
                                                    SettingState.CMD_LINE)

    if ac.set_by_user(args, 'process_monitoring'):
        sgh.settings.set_parallel_portfolio_process_monitoring(args.process_monitoring,
                                                               SettingState.CMD_LINE)

    if ac.set_by_user(args, 'performance_measure'):
        sgh.settings.set_general_performance_measure(
            PerformanceMeasure.from_str(args.performance_measure), SettingState.CMD_LINE)

    print('c Sparkle parallel portfolio is running ...')
    # instance_paths = list of paths to all instances
    # portfolio_path = Path to the portfolio containing the solvers
    succes = srpp.run_parallel_portfolio(instance_paths, portfolio_path)

    if succes:
        sgh.latest_scenario.set_parallel_portfolio_instance_list(instance_paths)
        print('c Running Sparkle parallel portfolio is done!')

        # Write used settings to file
        sgh.settings.write_used_settings()
    else:
        print('c An unexpected error occurred, please check your input an try again.')
