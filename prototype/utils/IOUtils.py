import os
import datetime
import sys
import json
sys.path.append(".")

import config.config as config



def checkdir(path):
    if (not os.path.exists(path)):
        os.makedirs(path)
        print(f'Making new folder for {path}')

def showInfo(message, type='INFO'):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{currentTime} ({os.getpid()}) [{type}] {message}")

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
