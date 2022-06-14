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
import fcntl
from pathlib import Path
from typing import List

try:
	from sparkle_help import sparkle_global_help as sgh
	from sparkle_help import sparkle_basic_help as sbh
	from sparkle_help import sparkle_file_help as sfh
	from sparkle_help import sparkle_performance_data_csv_help as spdcsv
	from sparkle_help import sparkle_job_help as sjh
	from sparkle_help.sparkle_settings import PerformanceMeasure
	from sparkle_help.sparkle_settings import SolutionVerifier
except ImportError:
	import sparkle_global_help as sgh
	import sparkle_basic_help as sbh
	import sparkle_file_help as sfh
	import sparkle_performance_data_csv_help as spdcsv
	import sparkle_job_help as sjh
	from sparkle_settings import PerformanceMeasure
	from sparkle_settings import SolutionVerifier

import functools
print = functools.partial(print, flush=True)


def get_solver_call_from_wrapper(solver_wrapper_path: str, instance_path: str) -> str:
	cmd_solver_call = ''

	cutoff_time_str = str(sgh.settings.get_general_target_cutoff_time())
	seed_str = str(sgh.get_seed())
	cmd_get_solver_call = solver_wrapper_path + ' --print-command \"' + instance_path + '\" --seed ' + seed_str + ' --cutoff-time ' + cutoff_time_str
	solver_call_rawresult = os.popen(cmd_get_solver_call)
	solver_call_result = solver_call_rawresult.readlines()[0].strip()

	if len(solver_call_result) > 0:
		cmd_solver_call = solver_call_result
	else:
		# TODO: Add instructions for the user that might fix the issue?
		print('c ERROR: Failed to get valid solver call command from wrapper at \'' + solver_wrapper_path + '\' stopping execution!')
		sys.exit()

	return cmd_solver_call


def run_solver_on_instance(solver_path: str, solver_wrapper_path: str,
							instance_path: str, raw_result_path: str,
							runsolver_values_path: str, custom_cutoff: int = None):
	"""Get the appropriate command line call and run the solver on the given instance."""
	if not Path(solver_wrapper_path).is_file():
		print(f'c ERROR: Wrapper named \'{solver_wrapper_path}\' not found, stopping '
			'execution!')
		sys.exit()

	# Get the solver call command from the wrapper
	cmd_solver_call = get_solver_call_from_wrapper(solver_wrapper_path, instance_path)

	run_solver_on_instance_with_cmd(Path(solver_path), cmd_solver_call,
									Path(raw_result_path),
									Path(runsolver_values_path), custom_cutoff)

	return


def run_solver_on_instance_with_cmd(solver_path: Path, cmd_solver_call: str,
									raw_result_path: Path, runsolver_values_path: Path,
									custom_cutoff: int = None,
									is_configured: bool = False) -> Path:
	"""Run the solver on the given instance, with a given command line call."""
	if custom_cutoff is None:
		cutoff_time_str = str(sgh.settings.get_general_target_cutoff_time())
	else:
		cutoff_time_str = str(custom_cutoff)

	# Prepare runsolver call
	runsolver_path = sgh.runsolver_path
	runsolver_option = '--timestamp --use-pty'
	cutoff_time_each_run_option = f'--cpu-limit {cutoff_time_str}'
	runsolver_values_log = f'-v {str(runsolver_values_path)}'
	runsolver_watch_data_path = str(runsolver_values_path).replace('val', 'log')
	runsolver_watch_data_path_option = f'-w {runsolver_watch_data_path}'
	raw_result_path_option = f'-o {str(raw_result_path)}'

	# For configured solvers change the directory to accommodate sparkle_smac_wrapper
	original_path = os.getcwd()

	if is_configured:
		# Change paths to accommodate configured execution directory
		runsolver_path = f'../../{sgh.runsolver_path}'
		runsolver_values_log = f'-v ../../{str(runsolver_values_path)}'
		runsolver_values_path = '../../' / runsolver_values_path
		runsolver_watch_data_path = str(runsolver_values_path).replace('val', 'log')
		runsolver_watch_data_path_option = f'-w {runsolver_watch_data_path}'
		raw_result_path_option = f'-o ../../{str(raw_result_path)}'

		# Copy to execution directory
		exec_path = str(raw_result_path).replace('.rawres', '_exec_dir/')
		Path(exec_path).mkdir(parents=True)
		cmd_copy_solver = f'cp -r {str(solver_path)}/* {exec_path}'
		os.system(cmd_copy_solver)

		# Change to execution directory
		cmd_cd = f'cd {exec_path}'

		# Return to original directory
		cmd_cd_back = f'cd {original_path}'

	# Finalise command
	command_line_run_solver = (f'{runsolver_path} {runsolver_option} '
		f'{cutoff_time_each_run_option} {runsolver_watch_data_path_option} '
		f'{runsolver_values_log} {raw_result_path_option} {str(solver_path)}/'
		f'{cmd_solver_call}')

	if is_configured:
		command_line_run_solver = (f'{cmd_cd} ; {runsolver_path} {runsolver_option} '
			f'{cutoff_time_each_run_option} {runsolver_watch_data_path_option} '
			f'{runsolver_values_log} {raw_result_path_option} ./{cmd_solver_call} ; '
			f'{cmd_cd_back}')

	# Execute command
	try:
		os.system(command_line_run_solver)
	except:
		print('WARNING: Solver execution seems to have failed!')
		print(f'The used command was: {command_line_run_solver}')

		# TODO: Why create an empty file if the command fails?
		if not raw_result_path.exists():
			sfh.create_new_empty_file(str(raw_result_path))
	else:
		# Clean up on success
		if is_configured:
			# Move .rawres file from tmp/ directory in the execution directory
			# to raw_result_path + '_solver'
			tmp_raw_res = f'{exec_path}tmp/'
			tmp_paths = list(Path(tmp_raw_res).glob('*.rawres'))
			raw_result_solver_path = str(raw_result_path).replace('.rawres', '.rawres_solver')

			# Only one result should exist
			if len(tmp_paths) < 1:
				print(f'WARNING: Raw result not found in {tmp_raw_res}, assuming '
					'timeout...')
				sfh.create_new_empty_file(raw_result_solver_path)
			else:
				raw_result_solver_src_path, *rest = tmp_paths
				raw_result_solver_src_path.rename(Path(raw_result_solver_path))
			# Remove execution directory (should contain nothing of interest on succes
			# after moving the .rawres file)
			sfh.rmtree(Path(exec_path))
			# Check .rawres_solver output
			check_solver_output_for_errors(Path(raw_result_solver_path))

		sfh.rmfile(Path(runsolver_watch_data_path))

	# Check for known errors/issues
	check_solver_output_for_errors(raw_result_path)

	if is_configured:
		return raw_result_solver_path
	else:
		return raw_result_path


def check_solver_output_for_errors(raw_result_path: Path):
	error_lines = [ \
		# /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found:
		"libstdc++.so.6: version `GLIBCXX",
		# For e.g. invalid solver path:
		"No such file or directory"
		]

	# Find lines containing an error
	with raw_result_path.open('r') as infile:
		for current_line in infile:
			for error in error_lines:
				if error in current_line:
					print('WARNING: Possible error deteced in', raw_result_path,
						'involving:', error)

	return


def run_solver_on_instance_and_process_results(solver_path: str, instance_path: str, custom_cutoff: int = None) -> (float, float, float, List[float], str, str):
	# Prepare paths
	# TODO: Fix result path for multi-file instances (only a single file is part of the result path)
	raw_result_path = sgh.sparkle_tmp_path + sfh.get_last_level_directory_name(solver_path) + '_' + sfh.get_last_level_directory_name(instance_path) + '_' + sbh.get_time_pid_random_string() + '.rawres'
	runsolver_values_path = raw_result_path.replace('.rawres', '.val')
	solver_wrapper_path = solver_path + '/' + sgh.sparkle_run_default_wrapper

	# Run
	run_solver_on_instance(solver_path, solver_wrapper_path, instance_path, raw_result_path, runsolver_values_path, custom_cutoff)

	# Process results
	cpu_time, wc_time, quality, status = process_results(raw_result_path, solver_wrapper_path, runsolver_values_path)
	cpu_time_penalised, status = handle_timeouts(cpu_time, status, custom_cutoff)
	status = verify(instance_path, raw_result_path, solver_path, status)

	return cpu_time, wc_time, cpu_time_penalised, quality, status, raw_result_path


def running_solvers(performance_data_csv_path, mode):
	cutoff_time_str = str(sgh.settings.get_general_target_cutoff_time())
	performance_measure = sgh.settings.get_general_performance_measure()
	performance_data_csv = spdcsv.Sparkle_Performance_Data_CSV(performance_data_csv_path)
	if mode == 1: list_performance_computation_job = performance_data_csv.get_list_remaining_performance_computation_job()
	elif mode == 2: list_performance_computation_job = performance_data_csv.get_list_recompute_performance_computation_job()
	else:
		print('c Running solvers mode error!')
		print('c Do not run solvers')
		sys.exit()

	print('c The cutoff time per algorithm run to solve an instance is set to ' + cutoff_time_str + ' seconds')

	total_job_num = sjh.get_num_of_total_job_from_list(list_performance_computation_job)
	current_job_num = 1
	print('c The total number of jobs to run is: ' + str(total_job_num))

	# If there are no jobs, stop
	if total_job_num < 1:
		return
	# If there are jobs update performance data ID
	else:
		update_performance_data_id()

	for i in range(0, len(list_performance_computation_job)):
		instance_path = list_performance_computation_job[i][0]
		solver_list = list_performance_computation_job[i][1]
		len_solver_list = len(solver_list)
		for j in range(0, len_solver_list):
			solver_path = solver_list[j]

			print('c')
			# TODO: Fix printing of multi-file instance 'path' (only one file name is printed)
			print('c Solver ' + sfh.get_last_level_directory_name(solver_path) + ' running on instance ' + sfh.get_last_level_directory_name(instance_path) + ' ...')

			cpu_time, wc_time, cpu_time_penalised, quality, status, raw_result_path = run_solver_on_instance_and_process_results(solver_path, instance_path)

			if status == 'CRASHED':
				print('c Warning: Solver ' + solver_path + ' appears to have crashed on instance ' + instance_path + ' for details see the solver log file at ' + raw_result_path)

			# Handle timeouts
			penalised_str = ''
			if performance_measure == PerformanceMeasure.RUNTIME and (status == 'TIMEOUT' or status == 'UNKNOWN'):
				penalised_str = ' (penalised)'

			# If status == 'WRONG' after verification remove solver
			# TODO: Check whether things break when a solver is removed which still has instances left in the job list
			if status == 'WRONG':
				remove_faulty_solver(solver_path, instance_path)
				current_job_num += 1

				continue # Skip to the next job

			# Update performance CSV
			if performance_measure == PerformanceMeasure.QUALITY_ABSOLUTE:
				# TODO: Handle the multi-objective case for quality
				performance_data_csv.set_value(instance_path, solver_path, quality[0])
				print('c Running Result: Status: ' + status + ', Quality' + penalised_str + ': ' + str(quality[0]))
			else:
				performance_data_csv.set_value(instance_path, solver_path, cpu_time_penalised)
				print('c Running Result: Status ' + status + ', Runtime' + penalised_str + ': ' + str(cpu_time_penalised))

			print(r'c Executing Progress: ' + str(current_job_num) + ' out of ' + str(total_job_num))
			current_job_num += 1

	performance_data_csv.update_csv()
	print('c Performance data file ' + performance_data_csv_path + ' has been updated!')

	return


def handle_timeouts(runtime: float, status: str, custom_cutoff: int = None) -> (float, str):
	if custom_cutoff is None:
		cutoff_time = sgh.settings.get_general_target_cutoff_time()
	else:
		cutoff_time = custom_cutoff

	if runtime > cutoff_time and status != 'CRASHED':
		status = 'TIMEOUT' # Overwrites possible user status, unless it is 'CRASHED'
	if status == 'TIMEOUT' or status == 'UNKNOWN':
		runtime_penalised = sgh.settings.get_penalised_time(cutoff_time)
	else:
		runtime_penalised = runtime

	return runtime_penalised, status


def verify(instance_path, raw_result_path, solver_path, status):
	verifier = sgh.settings.get_general_solution_verifier()

	# Use verifier if one is given and the solver did not time out
	if verifier == SolutionVerifier.SAT and status != 'TIMEOUT' and status != 'UNKNOWN':
		status = sat_verify(instance_path, raw_result_path, solver_path)

	return status


def process_results(raw_result_path: str, solver_wrapper_path: str, runsolver_values_path: str) -> (float, float, List[float], str):
	# By default runtime comes from runsolver, may be overwritten by user wrapper
	cpu_time, wc_time = get_runtime_from_runsolver(runsolver_values_path)

	# Get results from the wrapper
	cmd_get_results_from_wrapper = solver_wrapper_path + ' --print-output ' + raw_result_path
	results = os.popen(cmd_get_results_from_wrapper)
	result_lines = results.readlines()

	if len(result_lines) <= 0:
		# TODO: Add instructions for the user that might fix the issue?
		print('c ERROR: Failed to get output from wrapper at \'' + solver_wrapper_path + '\' stopping execution!')
		sys.exit()

	# Check if Sparkle should use it's own parser
	first_line = result_lines[0]
	first_line_parts = first_line.strip().split()

	if len(first_line_parts) == 4 and first_line_parts[0].lower() == 'use' and first_line_parts[1].lower() == 'sparkle':
		if first_line_parts[2].lower() == 'sat':
			quality = [] # Not defined for SAT
			status = sparkle_sat_parser(raw_result_path, cpu_time) # TODO: Handle wc_time when user can choose which to use
		else:
			parser_list = 'SAT'
			print('c ERROR: Wrapper at \'' + solver_wrapper_path + '\' requested Sparkle to use an internal parser that does not exist\nc Possible internal parsers: ' + parser_list + '\nc If your problem domain is not in the list, please parse the output in the wrapper.\nc Stopping execution!')
			sys.exit()
	else:
		# Read output
		quality = []
		status = 'UNKNOWN'
		for line in result_lines:
			parts = line.strip().split()
			# Skip empty lines
			if len(parts) <= 0:
				continue
			# Handle lines that are too short
			if len(parts) <= 1:
				print('c Warning: The line \'' + line.strip() + '\' contains no result information or is not formatted correctly: <quality/status/runtime> VALUE')
			if parts[0].lower() == 'quality':
				quality = get_quality_from_wrapper(parts)
			elif parts[0].lower() == 'status':
				status = get_status_from_wrapper(parts[1])
			elif parts[0].lower() == 'runtime':
				cpu_time = get_runtime_from_wrapper(parts[1])
				wc_time = cpu_time
			# TODO: Handle unknown keywords?

	return cpu_time, wc_time, quality, status


# quality -- comma separated list of quality measurements; [required when one or more quality objectives are used, optional otherwise]
def get_quality_from_wrapper(result_list: List[str]) -> List[float]:
	quality = []
	start_index = 1 # 0 is the keyword 'quality'

	for i in range(start_index, len(result_list)):
		quality.append(float(result_list[i]))
	
	return quality


# status [optional, SUCCESS assumed]
# In: List of words
# Out: String
def get_status_from_wrapper(result: str) -> str:
	status_list = '<SUCCESS/TIMEOUT/CRASHED/SAT/UNSAT/WRONG/UNKNOWN>'
	status = 'SUCCESS'

	if result.upper() == 'SUCCESS':
		status = 'SUCCESS'
	elif result.upper() == 'TIMEOUT':
		status = 'TIMEOUT'
	elif result.upper() == 'CRASHED':
		status = 'CRASHED'
	elif result.upper() == 'SAT':
		status = 'SAT'
	elif result.upper() == 'UNSAT':
		status = 'UNSAT'
	elif result.upper() == 'WRONG':
		status = 'WRONG'
	elif result.upper() == 'UNKNOWN':
		status = 'UNKNOWN'
	else:
		print('c ERROR: Invalid status \'' + result_list[1] + '\' given, possible statuses are: ' + status_list + '\nc Stopping execution!')
		sys.exit()

	return status


# runtime -- in seconds, will overwrite Sparkle's own measurement (through runsolver) if given [optional]
def get_runtime_from_wrapper(result: str) -> float:
	runtime = float(result)

	return runtime


# Read runtime in CPU and WC time from runsolver values file
def get_runtime_from_runsolver(runsolver_values_path: str) -> (float, float):
	cpu_time = float(-1)
	wc_time = float(-1)

	infile = open(runsolver_values_path, 'r+')
	fcntl.flock(infile.fileno(), fcntl.LOCK_EX)

	while True:
		line = infile.readline().strip()
		if not line:
			break
		words = line.split('=')
		# Read wallclock time from a line of the form 'WCTIME=0.110449'
		if len(words) == 2 and words[0] == 'WCTIME':
			wc_time = float(words[1])
		# Read CPU time from a line of the form 'CPUTIME=0.110449'
		elif len(words) == 2 and words[0] == 'CPUTIME':
			cpu_time = float(words[1])
			break # order is fixed, CPU is the last thing we want to read, so break from the loop

	infile.close()

	return cpu_time, wc_time


def sparkle_sat_parser(raw_result_path: str, runtime: float) -> str:
	if runtime > sgh.settings.get_general_target_cutoff_time():
		status = 'TIMEOUT'
	else: 
		status = sat_get_result_status(raw_result_path)

	return status


# In: Path to solver, path to instance it failed on
# Out: N/A
def remove_faulty_solver(solver_path, instance_path):
	wrong_solver_list.append(solver_path)
	print(r'c Warning: Solver ' + sfh.get_last_level_directory_name(solver_path) + r' reports the wrong answer on instance ' + sfh.get_last_level_directory_name(instance_path) + r'!')
	print(r'c Warning: Solver ' + sfh.get_last_level_directory_name(solver_path) + r' will be removed!')

	performance_data_csv.delete_column(solver_path)
	sgh.solver_list.remove(solver_path)
	sgh.solver_nickname_mapping.pop(solver_path)
	sfh.write_solver_list()
	sfh.write_solver_nickname_mapping()

	print(r'c Solver ' + sfh.get_last_level_directory_name(solver_path) + r' is a wrong solver')
	print(r'c Solver ' + sfh.get_last_level_directory_name(solver_path) + ' running on instance ' + sfh.get_last_level_directory_name(instance_path) + ' ignored!')
	print(r'c')

	return


def sat_verify(instance_path: str, raw_result_path: str, solver_path: str) -> str:
	status = sat_judge_correctness_raw_result(instance_path, raw_result_path)

	if status != 'SAT' and status != 'UNSAT' and status != 'WRONG':
		status = 'UNKNOWN'
		print('c Warning: Verification result was UNKNOWN for solver ' + sfh.get_last_level_directory_name(solver_path) + ' on instance ' + sfh.get_last_level_directory_name(instance_path) + '!')

	# TODO: Make removal conditional on a success status (SAT or UNSAT)
	#command_line = r'rm -f ' + raw_result_path
	#os.system(command_line)

	return status


def sat_get_result_status(raw_result_path: str) -> str:
	# If no result is reported in the result file something went wrong or the solver timed out
	status = 'UNKNOWN'

	infile = open(raw_result_path, 'r+')
	fcntl.flock(infile.fileno(), fcntl.LOCK_EX)

	while True:
		line = infile.readline().strip()
		if not line:
			break
		words = line.split()
		if len(words) == 3 and words[1] == 's':
			if words[2] == 'SATISFIABLE':
				status = 'SAT'
			elif words[2] == 'UNSATISFIABLE':
				status = 'UNSAT'
			else:
				# Something is wrong or the solver timed out
				print('c Warning: Unknown SAT result \'' + words[2] + '\'')
				status = 'UNKNOWN'
			break

	infile.close()

	return status


def sat_get_verify_string(tmp_verify_result_path):
	#4 return values: 'SAT', 'UNSAT', 'WRONG', 'UNKNOWN'
	ret = 'UNKNOWN'
	fin = open(tmp_verify_result_path, 'r+')
	fcntl.flock(fin.fileno(), fcntl.LOCK_EX)
	while True:
		myline = fin.readline()
		myline = myline.strip()
		if not myline: break
		if myline == r'Solution verified.':
			myline2 = fin.readline()
			myline2 = fin.readline().strip()
			if myline2 == r'11':
				ret = r'SAT'
				break
		elif myline == r'Solver reported unsatisfiable. I guess it must be right!':
			myline2 = fin.readline()
			myline2 = fin.readline().strip()
			if myline2 == r'10':
				ret = r'UNSAT'
				break
		elif myline == r'Wrong solution.':
			myline2 = fin.readline()
			myline2 = fin.readline().strip()
			if myline2 == r'0':
				ret = 'WRONG'
				break
		else:
			continue	
	fin.close()
	return ret


def sat_judge_correctness_raw_result(instance_path, raw_result_path):
	SAT_verifier_path = sgh.SAT_verifier_path
	tmp_verify_result_path = r'Tmp/'+ sfh.get_last_level_directory_name(SAT_verifier_path) + r'_' + sfh.get_last_level_directory_name(raw_result_path) + r'_' + sbh.get_time_pid_random_string() + r'.vryres'
	# TODO: Log output file
	command_line = SAT_verifier_path + r' ' + instance_path + r' ' + raw_result_path + r' > ' + tmp_verify_result_path
	print('c Run SAT verifier')
	os.system(command_line)
	print('c SAT verifier done')

	ret = sat_get_verify_string(tmp_verify_result_path)

	# TODO: Log output file removal
	command_line = 'rm -f ' + tmp_verify_result_path
	os.system(command_line)
	return ret


def update_performance_data_id():
	# Get current pd_id
	pd_id = get_performance_data_id()

	# Increment pd_id
	pd_id = pd_id + 1

	# Write new pd_id
	pd_id_path = sgh.performance_data_id_path

	with open(pd_id_path, 'w') as pd_id_file:
		pd_id_file.write(str(pd_id))

	return


def get_performance_data_id() -> int:
	pd_id = -1
	pd_id_path = sgh.performance_data_id_path

	try:
		with open(pd_id_path, 'r') as pd_id_file:
			pd_id = int(pd_id_file.readline())
	except FileNotFoundError:
		pd_id = 0

	return pd_id

