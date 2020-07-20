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
import argparse
from sparkle_help import sparkle_record_help
from sparkle_help import sparkle_csv_merge_help

if __name__ == r'__main__':
	# Define command line arguments
	parser = argparse.ArgumentParser()

	# Process command line arguments
	args = parser.parse_args()

	print(r'c Cleaning temporary files ...')
	command_line = r'rm -rf Commands/sparkle_help/*.pyc'
	os.system(command_line)
	command_line = r'rm -rf Tmp/*'
	os.system(command_line)
	command_line = r'rm -rf Tmp/SBATCH_Extractor_Jobs/*'
	os.system(command_line)
	command_line = r'rm -rf Tmp/SBATCH_Solver_Jobs/*'
	os.system(command_line)
	command_line = r'rm -rf Tmp/SBATCH_Portfolio_Jobs/*'
	os.system(command_line)
	command_line = r'rm -rf Tmp/SBATCH_Report_Jobs/*'
	os.system(command_line)
	command_line = r'rm -rf Feature_Data/Tmp/*'
	os.system(command_line)
	command_line = r'rm -rf Performance_Data/Tmp/*'
	os.system(command_line)
	command_line = r'rm -rf Log/*'
	os.system(command_line)
	command_line = r'rm -f slurm-*'
	os.system(command_line)
	print(r'c Temporary files cleaned!')

