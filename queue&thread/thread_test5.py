#-*-coding:utf-8-*-

import threading

lock = threading.RLock()

def run():
    lock.acquire()
    run1()
    run2()
    lock.release()

def run1():
    lock.acquire()
    lock.release()

def run2():
    lock.acquire()
    lock.release()

def main():
    for i in range(10):
        t = threading.Thread(target=run)
        t.start()
    while threading.active_count()!=1:
        print threading.active_count()


    print threading.active_count()

if __name__ == '__main__':
    main()