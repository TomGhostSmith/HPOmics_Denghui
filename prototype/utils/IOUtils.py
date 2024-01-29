import os
import datetime
import sys
import json
sys.path.append(".")

import config.config as config



def mkdir(path):
    if (not os.path.exists(path)):
        os.mkdirs(path)
        print(f'--- Making new folder for {path}')

def showInfo(message, type='INFO'):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{currentTime} [{type}] {message}")

