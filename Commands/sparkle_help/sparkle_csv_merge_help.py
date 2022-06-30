#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import fcntl

try:
    from sparkle_help import sparkle_global_help
    from sparkle_help import sparkle_file_help as sfh
    from sparkle_help import sparkle_feature_data_csv_help as sfdcsv
    from sparkle_help import sparkle_performance_data_csv_help as spdcsv
except ImportError:
    import sparkle_global_help
    import sparkle_file_help as sfh
    import sparkle_feature_data_csv_help as sfdcsv
    import sparkle_performance_data_csv_help as spdcsv


def feature_data_csv_merge():
    try:
        feature_data_csv = sfdcsv.Sparkle_Feature_Data_CSV(
            sparkle_global_help.feature_data_csv_path)
        tmp_feature_data_csv_directory = 'Feature_Data/Tmp/'
        csv_list = sfh.get_list_all_csv_filename(tmp_feature_data_csv_directory)
    except Exception:
        return

    for i in range(0, len(csv_list)):
        csv_name = csv_list[i]
        csv_path = tmp_feature_data_csv_directory + csv_name

        try:
            tmp_feature_data_csv = sfdcsv.Sparkle_Feature_Data_CSV(csv_path)
            feature_data_csv.combine(tmp_feature_data_csv)
            feature_data_csv.update_csv()
            os.system('rm -f ' + csv_path)
        except Exception:
            continue
    return


def performance_data_csv_merge():
    try:
        performance_data_csv = spdcsv.Sparkle_Performance_Data_CSV(
            sparkle_global_help.performance_data_csv_path)
        tmp_performance_data_result_directory = 'Performance_Data/Tmp/'
        result_list = sfh.get_list_all_result_filename(
            tmp_performance_data_result_directory)
    except Exception:
        return

    wrong_solver_list = []

    for i in range(0, len(result_list)):
        result_name = result_list[i]
        result_path = tmp_performance_data_result_directory + result_name

        try:
            fin = open(result_path, 'r+')
            fcntl.flock(fin.fileno(), fcntl.LOCK_EX)
            instance_path = fin.readline().strip()
            if not instance_path:
                continue
            solver_path = fin.readline().strip()
            if not solver_path:
                continue
            runtime_str = fin.readline().strip()
            if not runtime_str:
                continue
            runtime = float(runtime_str)

            performance_data_csv.set_value(instance_path, solver_path, runtime)
            fin.close()
            performance_data_csv.update_csv()
            os.system('rm -f ' + result_path)
        except Exception:
            continue

    for i in range(0, len(wrong_solver_list)):
        wrong_solver_path = wrong_solver_list[i]
        performance_data_csv.delete_column(wrong_solver_path)
        performance_data_csv.update_csv()
        sparkle_global_help.solver_list.remove(wrong_solver_path)
        sparkle_global_help.solver_nickname_mapping.pop(wrong_solver_path)
        sfh.write_solver_list()
        sfh.write_solver_nickname_mapping()

    return


if __name__ == '__main__':
    feature_data_csv_merge()
    performance_data_csv_merge()
else:
    feature_data_csv_merge()
    performance_data_csv_merge()
