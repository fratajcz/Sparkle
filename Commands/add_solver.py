#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Software: 	Sparkle (Platform for evaluating empirical algorithms/solvers)

Authors: 	Chuan Luo, chuanluosaber@gmail.com
			Holger H. Hoos, hh@liacs.nl

Contact: 	Chuan Luo, chuanluosaber@gmail.com
'''

import os
import sys
import argparse
from pathlib import Path

from sparkle_help import sparkle_file_help as sfh
from sparkle_help import sparkle_global_help as sgh
from sparkle_help import sparkle_performance_data_csv_help as spdcsv
from sparkle_help import sparkle_run_solvers_help as srs
from sparkle_help import sparkle_run_solvers_parallel_help as srsp
from sparkle_help import sparkle_job_parallel_help
from sparkle_help import sparkle_add_configured_solver_help as sacsh
from sparkle_help import argparse_custom as ac
from sparkle_help import sparkle_logging as sl
from sparkle_help import sparkle_settings
from sparkle_help.sparkle_command_help import CommandName


if __name__ == r'__main__':
	# Initialise settings
	global settings
	sgh.settings = sparkle_settings.Settings()

	# Log command call
	sl.log_command(sys.argv)

	# Define command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('solver_path', metavar='solver-path', type=str, help='path to the solver')
	parser.add_argument('--deterministic', required=True, type=int, choices=range(0, 2), help='indicate whether the solver is deterministic or not')
	parser.add_argument('--run-solver-later', action='store_true', help='do not immediately run the newly added solver')
	parser.add_argument('--nickname', type=str, help='set a nickname for the solver')
	parser.add_argument('--parallel', action='store_true', help='run the solver on multiple instances in parallel')
	# TODO choose a less confusing argument name
	parser.add_argument('--solver-instances', default=1, type=int, action=ac.SetByUser, help='if a solver is NOT deterministic this argument can be used to add multiple instances of the solver')

	# Process command line arguments
	args = parser.parse_args()
	solver_source = args.solver_path
	if not os.path.exists(solver_source):
		print(r'c Solver path ' + "\'" + solver_source + "\'" + r' does not exist!')
		sys.exit()

	deterministic = str(args.deterministic)
	my_flag_run_solver_later = args.run_solver_later
	nickname_str = args.nickname
	my_flag_parallel = args.parallel
	if ac.set_by_user(args, 'solver_instances'):
		solver_instances = args.solver_instances
		if solver_instances < 1: solver_instances = 1
	
	# Start add solver
	last_level_directory = r''
	last_level_directory = sfh.get_last_level_directory_name(solver_source)

	solver_diretory = r'Solvers/' + last_level_directory
	if not os.path.exists(solver_diretory):
		Path(solver_diretory).mkdir(parents=True, exist_ok=True)
	else:
		print(r'c Solver ' + sfh.get_last_level_directory_name(solver_diretory) + r' already exists!')
		if deterministic == 0:
			print(r'c adding ' + solver_instances + r' solver instance(s)!')
			sfh.change_solver_instances_from_solver_list(solver_diretory,solver_instances,True)
			sys.exit() 
		else:
			print(r'c Do not add solver ' + sfh.get_last_level_directory_name(solver_diretory))
			sys.exit()

	os.system(r'cp -r ' + solver_source + r'/* ' + solver_diretory)

	performance_data_csv = spdcsv.Sparkle_Performance_Data_CSV(sgh.performance_data_csv_path)
	performance_data_csv.add_column(solver_diretory)
	performance_data_csv.update_csv()

	sgh.solver_list.append(solver_diretory)
	sfh.add_new_solver_into_file(solver_diretory, deterministic, solver_instances)
	
	if sacsh.check_adding_solver_contain_pcs_file(solver_diretory):
		print('c pcs file detected, this is a configurable solver')

	print('c Adding solver ' + sfh.get_last_level_directory_name(solver_diretory) + ' done!')

	if os.path.exists(sgh.sparkle_portfolio_selector_path):
		command_line = r'rm -f ' + sgh.sparkle_portfolio_selector_path
		os.system(command_line)
		print('c Removing Sparkle portfolio selector ' + sgh.sparkle_portfolio_selector_path + ' done!')
	
	if os.path.exists(sgh.sparkle_report_path):
		command_line = r'rm -f ' + sgh.sparkle_report_path
		os.system(command_line)
		print('c Removing Sparkle report ' + sgh.sparkle_report_path + ' done!')
	
	if nickname_str is not None:
		sgh.solver_nickname_mapping[nickname_str] = solver_diretory
		sfh.add_new_solver_nickname_into_file(nickname_str, solver_diretory)
		pass

	if not my_flag_run_solver_later:
		if not my_flag_parallel:
			print('c Start running solvers ...')
			srs.running_solvers(sgh.performance_data_csv_path, 1)
			print('c Performance data file ' + sgh.performance_data_csv_path + ' has been updated!')
			print('c Running solvers done!')
		else:
			num_job_in_parallel = sgh.settings.get_slurm_number_of_runs_in_parallel()
			run_solvers_parallel_jobid = srsp.running_solvers_parallel(sgh.performance_data_csv_path, num_job_in_parallel, 1)
			print('c Running solvers in parallel ...')
			dependency_jobid_list = []
			if run_solvers_parallel_jobid:
				dependency_jobid_list.append(run_solvers_parallel_jobid)
			job_script = 'Commands/construct_sparkle_portfolio_selector.py'
			run_job_parallel_jobid = sparkle_job_parallel_help.running_job_parallel(job_script, dependency_jobid_list, CommandName.CONSTRUCT_SPARKLE_PORTFOLIO_SELECTOR)
		
			if run_job_parallel_jobid:
				dependency_jobid_list.append(run_job_parallel_jobid)
			job_script = 'Commands/generate_report.py'
			run_job_parallel_jobid = sparkle_job_parallel_help.running_job_parallel(job_script, dependency_jobid_list, CommandName.GENERATE_REPORT)

	# Write used settings to file
	sgh.settings.write_used_settings()

