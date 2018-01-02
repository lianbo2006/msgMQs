#!/usr/bin/env python

import threading
import time

def run(n):
    print("task", n)
    time.sleep(2)

def run_thread():
    start = time.time()
    t1 = threading.Thread(target=run, args=("t1",))
    t2 = threading.Thread(target=run, args=("t2",))
    t1.start()
    t2.start()
    end = time.time()
    print("run_thread cost %.2fs" %(end - start))

def run_run():
    start = time.time()
    run("r1")
    run("r2")
    end = time.time()
    print("run_run cost %.2fs" %(end - start))


def main():
    run_thread()
    # time.sleep(2)
    # run_run()

if __name__ == '__main__':
    main()