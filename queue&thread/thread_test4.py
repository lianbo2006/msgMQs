#-*-coding:utf-8-*-

import threading
import time

def run(n):
    global num
    num +=1
    time.sleep(1)

num = 0


def run_thread():
    t_obj =[]
    lock = threading.Lock()
    for i in range(12000):
        lock.acquire()
        t = threading.Thread(target=run, args=(str(i),))
        t.start()
        t_obj.append(t)
        lock.release()

    # for r in t_obj:
    #     r.join()

    print num


def main():
    run_thread()

if __name__ == '__main__':
    main()