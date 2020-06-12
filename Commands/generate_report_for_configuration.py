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
from sparkle_help import sparkle_global_help
from sparkle_help import sparkle_system_status_help
from sparkle_help import sparkle_csv_merge_help
from sparkle_help import sparkle_run_status_help
from sparkle_help import sparkle_generate_report_help
from sparkle_help import sparkle_generate_report_for_test_help
from sparkle_help import sparkle_configure_solver_help as scsh
from sparkle_help import sparkle_file_help as sfh
from sparkle_help import sparkle_generate_report_for_configuration_help as sgrfch

if __name__ == r'__main__':
	solver = ''
	instance_set = ''
	
	flag_solver = False
	flag_instance_set_train = False
	flag_instance_set_test = False
	
	len_argv = len(sys.argv)
	i = 1
	while i<len_argv:
		if sys.argv[i] == '--solver':
			i += 1
			solver = sys.argv[i]
			flag_solver = True
		elif sys.argv[i] == '--instance-set-train':
			i += 1
			instance_set_train = sys.argv[i]
			flag_instance_set_train = True
		elif sys.argv[i] == '--instance-set-test':
			i += 1
			instance_set_test = sys.argv[i]
			flag_instance_set_test = True
		else:
			print('c Argument Error!')
			print('c Usage: %s --solver <solver> [--instance-set-train <instance-set-train> [--instance-set-test <instance-set-test>]]' % sys.argv[0])
			sys.exit(-1)
		i += 1
	
	if not (flag_solver):
		print('c Argument Error!')
		print('c Usage: %s --solver <solver> [--instance-set-train <instance-set-train>] [--instance-set-test <instance-set-test>]' % sys.argv[0])
		sys.exit(-1)
	
	solver_name = sfh.get_last_level_directory_name(solver)

	# If no instance set(s) is/are given, try to retrieve them from the last run of test_configured_solver_and_default_solver
	if not flag_instance_set_train and not flag_instance_set_test:
		instance_set_train, instance_set_test, flag_instance_set_train, flag_instance_set_test = sgrfch.get_most_recent_test_run(solver_name)
	# If only the testing set is given return an error
	elif not flag_instance_set_train and flag_instance_set_test:
		print('c Argument Error! Only a testing set was provided, please also provide a training set')
		print('c Usage: %s --solver <solver> [--instance-set-train <instance-set-train>] [--instance-set-test <instance-set-test>]' % sys.argv[0])
		sys.exit(-1)

	# Generate a report depending on which instance sets are provided
	if (flag_instance_set_train and flag_instance_set_test):
		instance_set_train_name = sfh.get_last_level_directory_name(instance_set_train)
		instance_set_test_name = sfh.get_last_level_directory_name(instance_set_test)
		sgrfch.check_results_exist(solver_name, instance_set_train_name, instance_set_test_name)
		sgrfch.generate_report_for_configuration(solver_name, instance_set_train_name, instance_set_test_name)
	elif flag_instance_set_train:
		instance_set_train_name = sfh.get_last_level_directory_name(instance_set_train)
		sgrfch.check_results_exist(solver_name, instance_set_train_name)
		sgrfch.generate_report_for_configuration_train(solver_name, instance_set_train_name)
	else:
		print('c Error: No results from test_configured_solver_and_default_solver found that can be used in the report!')
		sys.exit(-1)

