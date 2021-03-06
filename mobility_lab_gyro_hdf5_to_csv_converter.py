import os
import json
import traceback
from copy import deepcopy

import h5py
import csv
import numpy as np
import tkinter as tk
from tkinter import filedialog


def get_hd5_files():
    root = tk.Tk()
    root.withdraw()
    dir_path = filedialog.askdirectory(title="Select Folder with h5 files")

    hd5_files = list()
    if dir_path:
        for file in os.listdir(dir_path):
            if file.endswith(".hd5") or file.endswith(".h5") or file.endswith(".hdf5"):
                hd5_files.append(os.path.join(dir_path, file))
    else:
        print("User Canceled")
    return hd5_files, dir_path


def get_config_file(file_dir):
    for file in os.listdir(file_dir):
        if "config" in file:
            return file
    return None


def get_config_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Json Config file")
    return file_path


def parse_config_file(file):
    with open(file) as f:
        file_dict = json.load(f)
    return file_dict


def parse_hd5_files(hd5_files, result_data_dict):
    for file in hd5_files:
        try:
            with h5py.File(file, "r") as f:
                # print(f['Measures']['Duration'])
                # print(list(f['Measures']['Duration']))
                # print(list(f['Annotations']))
                # print(f['Processed']['13746']['Orientation'])
                # print(list(f['Sensors']['13746']['Accelerometer']))
                # print(f['Sensors']['13746']['Barometer'])
                # print(f['Sensors']['13746']['Configuration']['Config'])
                # print(f['Sensors']['13746']['Configuration']['Config Strings'])
                # print(f['Sensors']['13746']['Configuration']['Misc'])
                # print(f['Sensors']['13746']['Gyroscope'])
                # print(f['Sensors']['13746']['Magnetometer'])
                # print(f['Sensors']['13746']['Metrics']['Events'])
                # print(f['Sensors']['13746']['Metrics']['Mesh'])
                # print(f['Sensors']['13746']['Metrics']['States'])
                # print(f['Sensors']['13746']['Temperature'])
                # print(f['Sensors']['13746']['Time'])
                # print(f['Processed']['13864']['Orientation'])
                # print(f['Sensors']['13864']['Accelerometer'])
                # print(f['Sensors']['13864']['Barometer'])
                # print(f['Sensors']['13864']['Configuration']['Config'])
                # print(f['Sensors']['13864']['Configuration']['Config Strings'])
                # print(f['Sensors']['13864']['Configuration']['Misc'])
                # print(f['Sensors']['13864']['Gyroscope'])
                # print(f['Sensors']['13864']['Magnetometer'])
                # print(f['Sensors']['13864']['Metrics']['Events'])
                # print(f['Sensors']['13864']['Metrics']['Mesh'])
                # print(f['Sensors']['13864']['Metrics']['States'])
                # print(f['Sensors']['13864']['Temperature'])
                # print(f['Sensors']['13864']['Time'])

                file_dict = {'sternum': dict(), 'sacrum': dict()}
                file_dict['sternum']['accelerometer'] = list(f['Sensors']['13746']['Accelerometer'])
                file_dict['sternum']['gyroscope'] = list(f['Sensors']['13746']['Gyroscope'])
                file_dict['sternum']['given_time'] = list(f['Sensors']['13746']['Time'])
                file_dict['sacrum']['accelerometer'] = list(f['Sensors']['13864']['Accelerometer'])
                file_dict['sacrum']['gyroscope'] = list(f['Sensors']['13864']['Gyroscope'])
                file_dict['sacrum']['given_time'] = list(f['Sensors']['13864']['Time'])

                temp_dict = {'sternum': dict(), 'sacrum': dict()}
                temp_dict['sternum']['given_time'] = list(f['Sensors']['13746']['Time'])
                temp_dict['sacrum']['given_time'] = list(f['Sensors']['13864']['Time'])
                for sensor_key, sensor_dict in file_dict.items():
                    if 'sacrum' in sensor_key or 'sternum' in sensor_key:
                        for group_key, group_list in sensor_dict.items():
                            if 'gyroscope' in group_key or 'accelerometer' in group_key:
                                for i, sub_l in enumerate(group_list):
                                    if i != 0:
                                        temp_dict[sensor_key][group_key + "_x"].append(float(sub_l[0]))
                                        temp_dict[sensor_key][group_key + "_y"].append(float(sub_l[1]))
                                        temp_dict[sensor_key][group_key + "_z"].append(float(sub_l[2]))
                                        temp_dict[sensor_key][group_key + "_abs_x"].append(abs(temp_dict[sensor_key][group_key + "_x"][-1]))
                                        temp_dict[sensor_key][group_key + "_abs_y"].append(abs(temp_dict[sensor_key][group_key + "_y"][-1]))
                                        temp_dict[sensor_key][group_key + "_abs_z"].append(abs(temp_dict[sensor_key][group_key + "_z"][-1]))
                                        temp_dict[sensor_key][group_key + "_abs_x_sum"][0] += temp_dict[sensor_key][group_key + "_abs_x"][-1]
                                        temp_dict[sensor_key][group_key + "_abs_y_sum"][0] += temp_dict[sensor_key][group_key + "_abs_y"][-1]
                                        temp_dict[sensor_key][group_key + "_abs_z_sum"][0] += temp_dict[sensor_key][group_key + "_abs_z"][-1]
                                    else:
                                        temp_dict[sensor_key][group_key + "_x"] = [sub_l[0]]
                                        temp_dict[sensor_key][group_key + "_y"] = [sub_l[1]]
                                        temp_dict[sensor_key][group_key + "_z"] = [sub_l[2]]
                                        temp_dict[sensor_key][group_key + "_abs_x"] = [abs(float(sub_l[0]))]
                                        temp_dict[sensor_key][group_key + "_abs_y"] = [abs(float(sub_l[1]))]
                                        temp_dict[sensor_key][group_key + "_abs_z"] = [abs(float(sub_l[2]))]
                                        temp_dict[sensor_key][group_key + "_abs_x_sum"] = [float(abs(sub_l[0]))]
                                        temp_dict[sensor_key][group_key + "_abs_y_sum"] = [float(abs(sub_l[1]))]
                                        temp_dict[sensor_key][group_key + "_abs_z_sum"] = [float(abs(sub_l[2]))]
                            elif "given_time" in group_key:
                                start_offset = 0
                                for j, val in enumerate(group_list):
                                    if j != 0:
                                        temp_dict[sensor_key]["time_micro"].append(val-start_offset)
                                    else:
                                        start_offset = val
                                        temp_dict[sensor_key]["time_micro"] = [0]

                result_data_dict[os.path.basename(file)] = temp_dict
        except Exception:
            print("ERROR: Had issues with ", file)
            # traceback.print_exc()
            print("Moving to next file")


def write_raw_data_csv(file_config_dict, dir_path):
    with open(os.path.join(dir_path, 'raw_data.csv'), 'w+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["file_name", "sensor", "data_type"])
        for file_name, file_data in file_config_dict.items():
            if "IMPORTANT" not in file_name and "example" not in file_name:
                for sensor_key, sensor_dict in file_data.items():
                    if 'sacrum' in sensor_key or 'sternum' in sensor_key:
                        for group_key, group_data in sensor_dict.items():
                            try:
                                new_row = [file_name, sensor_key, group_key] + group_data
                                csv_writer.writerow(new_row)
                            except Exception:
                                print("Issues writing {} {} {} to csv".format(file_name, sensor_key, group_key))
                                new_row = [file_name, sensor_key, group_key, "something_went_wrong"]
                                csv_writer.writerow(new_row)


def trim_data_by_valid_time(data_set, start_time_micro, end_time_micro, new_data_sets):
    start_point = 0
    for i, val in enumerate(data_set["time_micro"]):
        if val >= start_time_micro:
            start_point = i
            break
    last_index = len(data_set["time_micro"]) - 1
    end_point = last_index
    for j, val in enumerate(data_set["time_micro"][::-1]):
        if val <= end_time_micro:
            end_point = last_index - j
            break
    no_trim = False
    if end_point <= start_point:
        no_trim = True
    for group_key, group_data in data_set.items():
        if 'abs' not in group_key:
            if no_trim:
                new_data_sets[str(group_key) + "_trimmed"] = list(map(float, group_data))
            else:
                new_data_sets[str(group_key) + "_trimmed"] = list(map(float, group_data[start_point:end_point+1]))
            if "time" not in group_key:
                new_data_sets[str(group_key) + "_trimmed_abs"] = list(map(abs, new_data_sets[str(group_key) + "_trimmed"]))
                new_data_sets[str(group_key) + "_trimmed_abs_sum"] = [sum(new_data_sets[str(group_key) + "_trimmed_abs"])]


def find_outliers(data_set):
    outliers = list()
    no_outlier_list = list()
    temp_data_set = deepcopy(data_set)
    sorted(temp_data_set)
    q1, q3 = np.percentile(temp_data_set, [25,75])
    iqr = q3 - q1
    lower_range = q1 - (1.5 * iqr)
    upper_range = q3 + (1.5 * iqr)
    for num in data_set:
        if num < lower_range or num > upper_range:
            outliers.append(num)
        else:
            no_outlier_list.append(num)
    return q1, q3, iqr, lower_range, upper_range, outliers, no_outlier_list


def process_data(result_dict, config_dict):
    processed_data = dict()
    for file_name, file_data in result_dict.items():
        processed_data[file_name] = dict()
        if "IMPORTANT" not in file_name and "example" not in file_name and file_name in config_dict:
            for sensor_key, sensor_data in file_data.items():
                if 'sacrum' in sensor_key or 'sternum' in sensor_key:
                    processed_data[file_name][sensor_key] = dict()
                    trim_data_by_valid_time(sensor_data, config_dict[file_name]["start_time_micro"], config_dict[file_name]["end_time_micro"], processed_data[file_name][sensor_key])
                    old_processed_sensor_data = deepcopy(processed_data[file_name][sensor_key])
                    for group_key, group_data in old_processed_sensor_data.items():
                        if "trimmed" in group_key and "abs" not in group_key:
                            q1, q3, iqr, lower_range, upper_range, outliers, no_outlier_list = find_outliers(group_data)
                            processed_data[file_name][sensor_key][str(group_key) + "outlier_vars"] = [q1, q3, iqr, lower_range, upper_range]
                            processed_data[file_name][sensor_key][str(group_key) + "_outliers"] = outliers
                            processed_data[file_name][sensor_key][str(group_key) + "_no_outliers"] = no_outlier_list
                            processed_data[file_name][sensor_key][str(group_key) + "_no_outliers_abs"] = list(map(abs, no_outlier_list))
                            processed_data[file_name][sensor_key][str(group_key) + "_no_outliers_abs_sum"] = sum(processed_data[file_name][sensor_key][str(group_key) + "_no_outliers_abs"])
    return processed_data


def write_processed_data_csv(file_config_dict, dir_path):
    with open(os.path.join(dir_path, 'processed_data.csv'), 'w+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["file_name", "sensor", "data_type"])
        for file_name, file_data in file_config_dict.items():
            if "IMPORTANT" not in file_name and "example" not in file_name:
                for sensor_key, sensor_data in file_data.items():
                    if 'sacrum' in sensor_key or 'sternum' in sensor_key:
                        for group_key, group_data in sensor_data.items():
                            if "outlier_vars" in group_key:
                                new_row = [file_name, sensor_key, group_key] + ["Q1 Q3 IQR Lower_Bound Upper_Bound"] + list(group_data)
                            else:
                                if isinstance(group_data, list):
                                    new_row = [file_name, sensor_key, group_key] + group_data
                                else:
                                    new_row = [file_name, sensor_key, group_key, group_data]
                            try:
                                csv_writer.writerow(new_row)
                            except Exception:
                                print("Issues writing {} {} {} to csv".format(file_name, sensor_key, group_key))
                                new_row = [file_name, sensor_key, group_key, "something_went_wrong"]
                                csv_writer.writerow(new_row)


def hd5_converter():
    print("starting")
    hd5_files, dir_path = get_hd5_files()
    if not dir_path or not hd5_files:
        return
    print("hd5_files", hd5_files)
    print("parsing files")
    result_dict = dict()
    parse_hd5_files(hd5_files, result_dict)
    print("writing raw data to csv")
    write_raw_data_csv(result_dict, dir_path)

    print("Getting config file")
    config_file = get_config_file()
    # config_file = get_config_file(dir_path)
    if not config_file:
        return
    print("Parsing config_file ", config_file)
    file_config_dict = parse_config_file(config_file)
    print("Processing data ")
    processed_data = process_data(result_dict, file_config_dict)
    print("Writing processed data to csv")
    write_processed_data_csv(processed_data, dir_path)


if __name__ == '__main__':
    hd5_converter()
