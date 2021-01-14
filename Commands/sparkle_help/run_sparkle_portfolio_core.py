#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Software: 	Sparkle (Platform for evaluating empirical algorithms/solvers)

Authors: 	Chuan Luo, chuanluosaber@gmail.com
			Holger H. Hoos, hh@liacs.nl

Contact: 	Chuan Luo, chuanluosaber@gmail.com
'''

import argparse
from pathlib import Path
from pathlib import PurePath

try:
	from sparkle_help import sparkle_global_help as sgh
	from sparkle_help import sparkle_settings
	from sparkle_help import sparkle_run_portfolio_selector_help as srpsh
except ImportError:
	import sparkle_global_help as sgh
	import sparkle_settings
	import sparkle_run_portfolio_selector_help as srpsh


if __name__ == r'__main__':
	# Initialise settings
	global settings
	settings_dir = Path('Settings')
	file_path_latest = PurePath(settings_dir / 'latest.ini')
	sgh.settings = sparkle_settings.Settings(file_path_latest)

	# Define command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--instance', required=True, type=str, help='path to instance to run on')
	parser.add_argument('--performance-data-csv', required=True, type=str, help='path to performance data csv')
	args = parser.parse_args()

	# Process command line arguments
	instance_path = args.instance
	performance_data_csv_path = args.performance_data_csv

	# Run portfolio selector
	srpsh.call_sparkle_portfolio_selector_solve_instance(instance_path, performance_data_csv_path)

