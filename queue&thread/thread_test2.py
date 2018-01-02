#-*-coding:utf-8-*-

import threading
import time

def run(n):
    print"task", n
    time.sleep(2)

def run_thread():
    t_obj =[]
    start = time.time()
    for i in range(50):
        t = threading.Thread(target=run, args=(str(i),))
        t.setDaemon(True) #启动守护线程
        t.start()
        t_obj.append(t)
    # time.sleep(1)
    # print threading.active_count()
    # for r in t_obj:
    #     r.join()

    end = time.time()
    # print "run_thread cost %.2fs" % (end - start)
    # print threading.active_count()

def main():
    run_thread()

if __name__ == '__main__':
    main()