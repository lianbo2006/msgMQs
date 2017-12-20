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

def process_array(array):
    delay_avg = np.average(array)
    avg_array = np.full((119,), delay_avg)
    delay_std = np.std(array)
    # variance
    delay_var = np.var(array)
    plt.plot(array*1000, "b.", avg_array*1000, "m-")
    plt.xlabel("frame")
    plt.ylabel("delay/ms")
    plt.savefig('delay_fig', dpi=600)

    pass


def main():
    delay_file_name = "delay_list.txt"
    delay_array = np.array(file2list(delay_file_name))
    process_array(delay_array)
    pass


if __name__ == '__main__':
    main()