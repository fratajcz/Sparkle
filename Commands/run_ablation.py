#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Software: 	Sparkle (Platform for evaluating empirical algorithms/solvers)

Authors: 	Chuan Luo, chuanluosaber@gmail.com
			Holger H. Hoos, hh@liacs.nl
            Jeroen Rook, j.g.rook@umail.leidenuniv.nl

Contact: 	Chuan Luo, chuanluosaber@gmail.com
'''

#TODO: Read settingsfile
#TODO: Dedicated ablations settings file or copy from settings?
#TODO: Check for conflicts between settings (slurm vs ablation, smac vs ablation)
#TODO: SLURM and ABLATION run over multiple nodes (-n64 -c1 for example)
#TODO: Move log files to dedicated directories
#TODO: Handle tmp files

import argparse
import os
from sparkle_help import sparkle_file_help as sfh
from sparkle_help import sparkle_run_ablation_help as sah
from sparkle_help import sparkle_global_help as sgh
from sparkle_help import sparkle_configure_solver_help as scsh
from sparkle_help import sparkle_add_train_instances_help as satih
from sparkle_help import sparkle_slurm_help as ssh


if __name__ == r'__main__':
	#Load solver and test instances
    parser = argparse.ArgumentParser()
    parser.add_argument('--solver', required=False, type=str, help='path to solver')
    parser.add_argument('--instance-set-train', required=False, type=str, help='path to training instance set')
    parser.add_argument('--instance-set-test', required=False, type=str, help='path to testing instance set')
    parser.add_argument('--ablation-settings-help', required=False, dest="ablation_settings_help", action="store_true", help='prints a list of setting that can be used for the ablation analysis')
    parser.set_defaults(ablation_settings_help=False)
    args = parser.parse_args()

    if(args.ablation_settings_help):
        sah.print_ablation_help()
        exit()

    solver = args.solver
    instance_set_train = args.instance_set_train
    instance_set_test = args.instance_set_test

    solver_name = sfh.get_last_level_directory_name(solver)
    instance_set_train_name = sfh.get_last_level_directory_name(instance_set_train)
    instance_set_test_name = None
    if instance_set_test is not None:
        instance_set_test_name = sfh.get_last_level_directory_name(instance_set_test)
    print(solver_name, instance_set_train_name, instance_set_test_name)

    #DEVELOP: REMOVE SCENARIO
    ablation_scenario_dir = sah.get_ablation_scenario_directory(solver_name, instance_set_train_name, instance_set_test_name)
    os.system("rm -rf {}".format(ablation_scenario_dir))

    #Prepare ablation scenario directory
    ablation_scenario_dir = sah.prepare_ablation_scenario(solver_name, instance_set_train_name, instance_set_test_name)
    print(ablation_scenario_dir)

    #Instances
    sah.create_instance_file(instance_set_train, ablation_scenario_dir, "train")
    sah.create_instance_file(instance_set_test, ablation_scenario_dir, "test")

    #Configurations
    sah.create_configuration_file(solver_name, instance_set_train_name, instance_set_test_name)
    #Add instances

    #Submit ablation run
    #TODO: Move to help
    sbatch_script_path = sah.generate_slurm_script(solver_name, instance_set_train_name, instance_set_test_name)
    jobid =ssh.submit_sbatch_script(sbatch_script_path, "./")
    print("Launched sbatch with jobid {}".format(jobid))