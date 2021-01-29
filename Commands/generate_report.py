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

from sparkle_help import sparkle_global_help as sgh
from sparkle_help import sparkle_generate_report_help as sgrh
from sparkle_help import sparkle_file_help as sfh
from sparkle_help import sparkle_logging as sl
from sparkle_help import sparkle_settings
from sparkle_help.sparkle_settings import PerformanceMeasure
from sparkle_help.sparkle_settings import SettingState
from sparkle_help import argparse_custom as ac


def generate_task_run_status():
	key_str = 'generate_report'
	task_run_status_path = r'Tmp/SBATCH_Report_Jobs/' + key_str + r'.statusinfo'
	status_info_str = 'Status: Running\n'
	sfh.write_string_to_file(task_run_status_path, status_info_str)
	return


def delete_task_run_status():
	key_str = 'generate_report'
	task_run_status_path = r'Tmp/SBATCH_Report_Jobs/' + key_str + r'.statusinfo'
	os.system(r'rm -rf ' + task_run_status_path)
	return


if __name__ == r'__main__':
	# Initialise settings
	global settings
	sgh.settings = sparkle_settings.Settings()

	# Log command call
	sl.log_command(sys.argv)

	# Define command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--test-case-directory', type=str, default=None, help='Path to test case directory of an instance set')
	parser.add_argument('--performance-measure', choices=PerformanceMeasure.__members__, default=sgh.settings.DEFAULT_general_performance_measure, action=ac.SetByUser, help='the performance measure, e.g. runtime')
	parser.add_argument('--settings-file', type=Path, default=sgh.settings.DEFAULT_settings_path, action=ac.SetByUser, help='specify the settings file to use in case you want to use one other than the default')

	# Process command line arguments
	args = parser.parse_args()
	test_case_directory = args.test_case_directory

	if ac.set_by_user(args, 'settings_file'): sgh.settings.read_settings_ini(args.settings_file, SettingState.CMD_LINE) # Do first, so other command line options can override settings from the file
	if ac.set_by_user(args, 'performance_measure'): sgh.settings.set_general_performance_measure(PerformanceMeasure.from_str(args.performance_measure), SettingState.CMD_LINE)

	## Reporting for algorithm selection
	if sgh.settings.get_general_performance_measure() == PerformanceMeasure.QUALITY_ABSOLUTE:
		print('ERROR: The generate_report command is not yet implemented for the QUALITY_ABSOLUTE performance measure! (functionality coming soon)')
		sys.exit()

	if not os.path.isfile(sgh.sparkle_portfolio_selector_path):
		print(r'c Before generating Sparkle report, please first construct Sparkle portfolio selector!')
		print(r'c Do not generate Sparkle report. Exit!')
		sys.exit()
	
	print(r'c Generating report ...')
	generate_task_run_status()

	if test_case_directory == None:
		sgrh.generate_report()
	else:
		sgrh.generate_report(test_case_directory)

	delete_task_run_status()
	print(r'c Report generated ...')

	# Write used settings to file
	sgh.settings.write_used_settings()

