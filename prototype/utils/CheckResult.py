import sys
import os
import math
import multiprocessing
sys.path.append('.')

from config import config
import utils.IOUtils as IOUtils

def checkFolder(path, finalList):
    IOUtils.showInfo(f'loading {path}')
    files = os.listdir(path)
    for file in files:
        if (os.path.isdir(f'{path}/{file}')):
            checkFolder(f'{path}/{file}', finalList)
        else:
            finalList.put(f'{path}/{file}')

def check(file):
    with open(file) as fp:
        lines = fp.readlines()
    for line in lines:
        if ('nan' in line or 'inf' in line):
            IOUtils.showInfo(file)
            with open("./ProblemFiles.txt", 'at') as fp:
                fp.writelines(file + '\n')
            break

def main():
    finalList = multiprocessing.Queue()
    checkFolder('./splitResult', finalList)
    
    childPIDList = list()
    lock = multiprocessing.Lock()
    for i in range(config.CPUCores):
        pid = os.fork()
        if (pid == 0):
            while True:
                lock.acquire()
                if (finalList.empty()):
                    lock.release()
                    break
                file = finalList.get()
                lock.release()
                check(file)
            os._exit(0)
        else:
            childPIDList.append(pid)
    
    for pid in childPIDList:
        os.waitpid(pid, 0)
    



main()