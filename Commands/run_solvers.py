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
import run_solvers_parallel as rsp
from sparkle_help import sparkle_basic_help
from sparkle_help import sparkle_record_help as srh
from sparkle_help import sparkle_file_help as sfh
from sparkle_help import sparkle_global_help
from sparkle_help import sparkle_performance_data_csv_help as spdcsv
from sparkle_help import sparkle_run_solvers_help as srs
from sparkle_help import sparkle_run_solvers_parallel_help as srsp
from sparkle_help import sparkle_csv_merge_help
from sparkle_help import sparkle_experiments_related_help
from sparkle_help import sparkle_job_parallel_help
from sparkle_help import sparkle_logging as sl


if __name__ == r'__main__':
	# Log command call
	sl.log_command(sys.argv)

	print('c Start running solvers ...')

	my_flag_recompute = False
	my_flag_parallel = False

	len_argv = len(sys.argv)
	i = 1
	while i<len_argv:
		if sys.argv[i] == r'--recompute':
			my_flag_recompute = True
		elif sys.argv[i] == r'--parallel':
			my_flag_parallel = True
		i += 1

	if not srh.detect_current_sparkle_platform_exists():
		print('c No Sparkle platform found; please first run the initialise command')
		exit()

	if not my_flag_parallel:
		if my_flag_recompute:
			performance_data_csv = spdcsv.Sparkle_Performance_Data_CSV(sparkle_global_help.performance_data_csv_path)
			performance_data_csv.clean_csv()
			srs.running_solvers(sparkle_global_help.performance_data_csv_path, 2)
		else:
			srs.running_solvers(sparkle_global_help.performance_data_csv_path, 1)
	
		print('c Performance data file ' + sparkle_global_help.performance_data_csv_path + ' has been updated!')
		print('c Running solvers done!')
	else:
		# Call the parallel version of this command
		rsp.run_solvers_parallel(my_flag_recompute)

