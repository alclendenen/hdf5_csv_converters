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


def recursive_traverse_unknown_struct(h5_struct, result_data_dict, last_key=""):
    if isinstance(h5_struct, h5py.Group):
        if last_key:
            result_data_dict[last_key] = dict()
        for key in h5_struct.keys():
            if last_key:
                recursive_traverse_unknown_struct(h5_struct[key], result_data_dict[last_key], key)
            else:
                recursive_traverse_unknown_struct(h5_struct[key], result_data_dict, key)
    elif isinstance(h5_struct, h5py.Dataset):
        if last_key:
            result_data_dict[last_key] = list(h5_struct)
        else:
            result_data_dict["dataset_as_list"] = list(h5_struct)
    # elif isinstance(h5_struct, h5py.AttributeManager):
    else:
        print("Unhandled struct type {}".format(type(h5_struct)))


def recursive_write_unknown_struct_to_csv(h5_struct, csv_writer, last_key="", current_keys=None):
    if current_keys is None:
        current_keys = list()
    if isinstance(h5_struct, h5py.Group):
        if last_key:
            current_keys.append(last_key)
        for key in h5_struct.keys():
            if last_key:
                recursive_write_unknown_struct_to_csv(h5_struct[key], csv_writer, key, deepcopy(current_keys))
            else:
                recursive_write_unknown_struct_to_csv(h5_struct[key], csv_writer, key, deepcopy(current_keys))
    elif isinstance(h5_struct, h5py.Dataset):
        if last_key:
            current_keys.append(last_key)
            current_keys += list(h5_struct)
        else:
            current_keys.append("dataset_as_list")
            current_keys += list(h5_struct)
        try:
            csv_writer.writerow(current_keys)
        except Exception:
            print("Error while trying to write csv row")
    # elif isinstance(h5_struct, h5py.AttributeManager):
    else:
        print("Unhandled struct type {}".format(type(h5_struct)))


def generic_parse_hd5_files(hd5_files, result_data_dict):
    for file in hd5_files:
        try:
            with h5py.File(file, "r") as h5_struct:
                recursive_traverse_unknown_struct(h5_struct, "", result_data_dict)
        except Exception:
            print("ERROR: Had issues with ", file)
            # traceback.print_exc()
            print("Moving to next file")


def generic_write_hd5_files_to_csv(hd5_files, dir_path):
    for file in hd5_files:
        try:
            with h5py.File(file, "r") as h5_struct:
                with open(os.path.join(dir_path, 'raw_data.csv'), 'w+', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    recursive_write_unknown_struct_to_csv(h5_struct, csv_writer, "")
        except Exception:
            print("ERROR: Had issues with ", file)
            # traceback.print_exc()
            print("Moving to next file")


def write_raw_data_csv(file_config_dict, dir_path):
    with open(os.path.join(dir_path, 'raw_data.csv'), 'w+', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for file_name, file_data in file_config_dict.items():
            if "IMPORTANT" not in file_name and "example" not in file_name:
                for sensor_key, sensor_dict in file_data.items():
                    if 'sacrum' in sensor_key or 'sternum' in sensor_key:
                        for group_key, group_data in sensor_dict.items():
                            new_row = [file_name, "{}_{}".format(sensor_key, group_key)] + group_data
                            # new_row = [file_name, "{}_{}".format(sensor_key, group_key)]
                            csv_writer.writerow(new_row)


def hd5_converter():
    print("starting")
    hd5_files, dir_path = get_hd5_files()
    if not dir_path or not hd5_files:
        return
    print("hd5_files", hd5_files)
    print("parsing files")
    result_dict = dict()
    generic_parse_hd5_files(hd5_files, result_dict)
    print("writing raw data to csv")
    write_raw_data_csv(result_dict, dir_path)


if __name__ == '__main__':
    hd5_converter()
