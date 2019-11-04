#!/usr/bin/env python2.7
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
from sparkle_help import sparkle_basic_help
from sparkle_help import sparkle_record_help
from sparkle_help import sparkle_file_help as sfh
from sparkle_help import sparkle_global_help
from sparkle_help import sparkle_performance_data_csv_help as spdcsv
from sparkle_help import sparkle_run_solvers_help as srs
from sparkle_help import sparkle_run_solvers_parallel_help as srsp
from sparkle_help import sparkle_csv_merge_help
from sparkle_help import sparkle_experiments_related_help
from sparkle_help import sparkle_job_parallel_help
from sparkle_help import sparkle_configure_solver_help as scsh
from sparkle_help import sparkle_add_train_instances_help as satih


if __name__ == r'__main__':
	solver = ''
	instance_set = ''
	
	flag_solver = False
	flag_instance_set = False
	
	len_argv = len(sys.argv)
	i = 1
	while i<len_argv:
		if sys.argv[i] == r'-solver':
			i += 1
			solver = sys.argv[i]
			flag_solver = True
		elif sys.argv[i] == r'-instances-train':
			i += 1
			instance_set = sys.argv[i]
			flag_instance_set = True
		else:
			print('c Argument Error!')
			print('c Usage: %s -solver <solver> -instances-train <instances-train>' % sys.argv[0])
			sys.exit(-1)
		i += 1
	
	if not (flag_solver and flag_instance_set):
		print('c Argument Error!')
		print('c Usage: %s -solver <solver> -instances_train <instances_train>' % sys.argv[0])
		sys.exit(-1)
	
	solver_name = sfh.get_last_level_directory_name(solver)
	instance_set_name = sfh.get_last_level_directory_name(instance_set)
	#print(solver_name, instance_set_name)

	# Copy instances to smac directory
	instances_directory = r'Instances/' + instance_set_name
	list_cnf_path = satih.get_list_cnf_path(instances_directory)
	cnf_dir_prefix = instances_directory
	smac_cnf_dir_prefix = sparkle_global_help.smac_dir + r'/' + 'example_scenarios/' + r'instances/' + sfh.get_last_level_directory_name(instances_directory)
	satih.copy_instances_to_smac(list_cnf_path, cnf_dir_prefix, smac_cnf_dir_prefix, r'train')

	scsh.handle_file_instance_train(solver_name, instance_set_name)
	scsh.create_file_scenario(solver_name, instance_set_name)
	smac_configure_sbatch_script_name = scsh.create_smac_configure_sbatch_script(solver_name, instance_set_name)
	scsh.submit_smac_configure_sbatch_script(smac_configure_sbatch_script_name)

	# Write most recent run to file
	last_configuration_file_path = sparkle_global_help.smac_dir + '/example_scenarios/' + solver_name + '/' + sparkle_global_help.sparkle_last_configuration_file_name

	fout = open(last_configuration_file_path, 'w+')
	fout.write('solver ' + str(solver) + '\n')
	fout.write('train ' + str(instance_set) + '\n')
	fout.close()

