import os
import sys
import time
import math
from tqdm import tqdm
import multiprocessing
sys.path.append('.')

from utils import IOUtils
from config import config

def parallel(paramList, func, maxThreads=multiprocessing.cpu_count(), threadProportion=1, unpack=True):
    threadCount = int(maxThreads * threadProportion)
    IOUtils.showInfo(f"Process {func.__name__} with {threadCount} threads")
    queue = multiprocessing.Queue()
    lock = multiprocessing.Lock()
    childPIDList = list()
    for params in paramList:
        queue.put(params)
    for _ in range(threadCount):
        pid = os.fork()
        if (pid == 0):
            while True:
                lock.acquire()
                if (queue.empty()):
                    lock.release()
                    break
                params = queue.get()
                lock.release()
                if (unpack):
                    func(*params)   
                else:
                    func(params)   
            os._exit(0)
        else:
            childPIDList.append(pid)

    for pid in childPIDList:
        os.waitpid(pid, 0)

def parallelWithResult(paramList, func, maxThreads=multiprocessing.cpu_count(), threadProportion=1, unpack=True):
    results = list()
    if (config.supportFork == True):
        threadCount = int(maxThreads * threadProportion)
        IOUtils.showInfo(f"Process {func.__name__}() on {len(paramList)} instances with {threadCount} threads", "PROC")
        queue = multiprocessing.Queue()
        lock = multiprocessing.Lock()
        childPIDList = list()
        connections = list()
        for idx, params in enumerate(paramList):
            parentConn, childConn = multiprocessing.Pipe()
            queue.put((idx, params, childConn))
            connections.append(parentConn)

        time.sleep(1)

        for _ in range(threadCount):
            pid = os.fork()
            if (pid == 0):
                # time.sleep(1) # in case the child quit too fast that parent haven't ready to wait pid
                while True:
                    lock.acquire()
                    if (queue.empty()):
                        lock.release()
                        break
                    idx, params, childConn = queue.get()
                    lock.release()
                    if (unpack):
                        result = func(*params)
                    else:
                        result = func(params)
                    # IOUtils.showInfo('Sending info')
                    childConn.send(result)
                    # IOUtils.showInfo('Sent')
                    childConn.close()
                
                # s = 0
                # for i in range(1000000):
                #     s += math.sqrt(i / 1.5)
                # time.sleep(30)  # in case the child quit too fast that parent haven't ready to wait pid
                # print('Done')
                os._exit(0)
            else:
                childPIDList.append(pid)

        progressBar = tqdm(total=len(paramList), desc=f"{func.__name__}()", unit="iter")

        for conn in connections:
            res = conn.recv()
            conn.close()
            results.append(res)
            progressBar.update(1)
        progressBar.close()
        for pid in childPIDList:
            os.waitpid(pid, 0)
    else:
        progressBar = tqdm(total=len(paramList), desc=f"{func.__name__}()", unit="iter")
        for param in paramList:
            if (unpack):
                res = func(*param)
            else:
                res = func(param)
            results.append(res)
            progressBar.update(1)
        progressBar.close()


    return results


# this is a test, showing that the result after parallel process is still in order

# import time
# def fun(num, num2):
#     IOUtils.showInfo(f"[{num}] start")
#     time.sleep(0.2)
#     IOUtils.showInfo(f"[{num}] end")
#     return num * num2 - 1
# params = [(i, 2) for i in range(1, 101)]
# res = parallelWithResult(params, fun)
# IOUtils.showInfo(res)