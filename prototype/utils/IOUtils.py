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
    with open('/home/joy/Log/hpomics', 'at') as fp:
        fp.write(msg + '\n') 

# create folders if not exists
def init(stage):
    showInfo('--------------------------------------------------------------------------')
    showInfo(f'Use GPU: {config.GPUAvailable}. CPU Cores: {config.CPUCores}. Use fork: {config.supportFork}.', 'CONFIG')
    if (stage == 1):
        showInfo(f'Extract annotation: {config.datasetParams}', 'TASK')
    elif (stage == 2):
        showInfo(f'Preprocess: {config.datasetParams}{config.dsSpecificParams}', 'TASK')
    elif (stage == 3):
        showInfo(f'Precalculate: {config.datasetParams}{config.taskParams}', 'TASK')
    elif (stage == 4):
        showInfo(f'Calculate: {config.calculateParams}', 'TASK')
    elif (stage == 5):
        showInfo(f'Combine: {config.combineParams}', 'TASK')
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