import os
import datetime
import sys
import json
sys.path.append(".")

from config import config
# from config import Config
# config = Config()



def checkdir(path):
    if (not os.path.exists(path)):
        os.makedirs(path)
        print(f'Making new folder for {path}')

def showInfo(message, type='INFO'):
    if (type == 'WARN' and config.ignoreWarning == True):
        return
    if (type == 'PROC' and config.ignoreSmallProcess):
        return
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    msg = f"{currentTime} ({os.getpid()}) [{type}] {message}"
    print(msg)
    with open('/home/joy/Log/HPOmics', 'at') as fp:
        fp.write(msg + '\n') 

# create folders if not exists
def init():
    showInfo(f'Task: {config.taskName}. Use GPU: {config.GPUAvailable}. CPU Cores: {config.CPUCores}. Use fork: {config.supportFork}')
    folders = [
        config.projectPath,
        config.splitResultPath,
        config.resultPath,
        config.dataPath,
        config.patientPath,
        config.standardResultPath,
        config.analysisPath
    ]
    for folder in folders:
        checkdir(folder)
init()