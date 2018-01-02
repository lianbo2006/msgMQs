# !/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt


def file2list(filename):
    delay_list = []
    try:
        f1 = open(filename, "r")
        file_str = f1.readline()
        f1.close()
        delay_list = eval(file_str)
        # print(type(delay_list), len(delay_list))
        return delay_list

    except:
        return delay_list

def file2arrays(filename):
    delay_list1 = []
    delay_list2 = []
    try:
        f1 = open(filename, "r")
        file_str = f1.readline()
        delay_list1 = eval(file_str)
        file_str = f1.readline()
        delay_list2 = eval(file_str)
        f1.close()
        # print(type(delay_list1), len(delay_list1))
        # print(type(delay_list2), len(delay_list2))
        delay_array1 = np.array(delay_list1)
        delay_array2 = np.array(delay_list2)
        return delay_array1, delay_array2

    except:
        return delay_array1, delay_array2

def process_array(array):
    delay_avg = np.average(array)
    avg_array = np.full((119,), delay_avg)
    delay_std = np.std(array)
    # variance
    delay_var = np.var(array)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    frame_delay_plot = ax.plot(array*1000, "b.", label='frame_delay')
    delay_avg_plot = ax.plot(avg_array*1000, "r-", label='delay_avg')
    ax.legend(loc='upper right')
    plt.xlabel("frame")
    plt.ylabel("delay/ms")
    plt.savefig('delay_fig', dpi=600)


def process_arrays(array1, array2):
    delay_avg1 = np.average(array1)
    delay_avg2 = np.average(array2)
    avg_array1 = np.full((119,), delay_avg1)
    avg_array2 = np.full((119,), delay_avg2)
    delay_std1 = np.std(array1)
    delay_std2 = np.std(array2)
    # variance
    delay_var1 = np.var(array1)
    delay_var2 = np.var(array2)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    frame_delay_plot1 = ax.plot(array1*1000, "b.", label='frame_delay_local')
    delay_avg_plot1 = ax.plot(avg_array1*1000, "r-", label='delay_avg_local')
    frame_delay_plot2 = ax.plot(array2 * 1000, "k.", label='frame_delay_cloud')
    delay_avg_plot2 = ax.plot(avg_array2 * 1000, "r-", label='delay_avg_cloud')
    ax.legend(loc='best')
    plt.xlabel("frame")
    plt.ylabel("delay/ms")
    # plt.show()
    plt.savefig('delay_fig_double', dpi=600)
    pass


def main():
    delay_file_name = "delay_list_local_cloud.txt"
    delay_array1, delay_array2 = file2arrays(delay_file_name)
    process_arrays(delay_array1,delay_array2)
    pass


if __name__ == '__main__':
    main()