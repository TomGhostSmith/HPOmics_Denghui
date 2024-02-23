import sys
import os
import math
import multiprocessing
sys.path.append('.')

import config.config as config
from utils import IOUtils


def calc(disease2Patient, patient2Disease, diseaseIC, patientIC):
    # return (disease2Patient + patient2Disease)/(diseaseIC + patientIC)
    if (patientIC != 0 and diseaseIC + patientIC != 0):
        return (disease2Patient + patient2Disease)/(diseaseIC + patientIC) + patient2Disease/patientIC
    # if (patientIC != 0):
        # return patient2Disease/patientIC
    else:
        return 0
    # return (disease2Patient + 4*patient2Disease)/(diseaseIC + 4*patientIC) + patient2Disease/patientIC
    # return patient2Disease/patientIC
    if (diseaseIC != 0):
        return (disease2Patient/diseaseIC + patient2Disease/patientIC)/2
        # return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC))
    #     return (disease2Patient + patient2Disease)/(diseaseIC + patientIC) + disease2Patient/diseaseIC
    else:
        return patient2Disease/patientIC
        # return 0


    if (diseaseIC == 0):
        return 0
    elif (disease2Patient/diseaseIC > 0.25):
    # elif (diseaseIC > patientIC):
        return patient2Disease/patientIC
    else:
        return patient2Disease/patientIC * 0.95
        # return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC) + patient2Disease/patientIC)/2
        # return (disease2Patient/diseaseIC + patient2Disease/patientIC)/2

        # return max(patient2Disease/patientIC, disease2Patient/diseaseIC)
        # return (patient2Disease/patientIC*diseaseIC + disease2Patient/diseaseIC*patientIC)/(patientIC + diseaseIC)

def combineFiles(files):
    for file in files:
        # skip folders
        if (os.path.isdir(f"{config.splitResultPath}/{file}")):
            continue

        with open(f"{config.splitResultPath}/{file}") as fp:
            scores = fp.readlines()
        finalScores = dict()
        for line in scores:
            if (line.startswith('id')):
                continue
            terms = line.strip().split(',')
            if (config.taskType == 'disease'):
                finalScores[terms[0]] = calc(float(terms[2]), float(terms[3]), float(terms[4]), float(terms[5]))
            else:
                finalScores[terms[1]] = calc(float(terms[2]), float(terms[3]), float(terms[4]), float(terms[5]))
        result = dict(sorted(finalScores.items(), key=lambda pair : pair[1], reverse=True))
        if (config.taskType == 'disease'):
            lines = [f'{key}, , {value}\n' for (key, value) in result.items()]
        else:
            lines = [f' ,{key}, {value}\n' for (key, value) in result.items()]
        lines.insert(0, 'id, name, score\n')
        with open(f"{config.resultPath}/{file}", 'wt') as fp:
            fp.writelines(lines)

def main():
    IOUtils.init()
    IOUtils.showInfo("Start combining splitted results")
    files = sorted(os.listdir(config.splitResultPath))

    if (config.supportFork):
        caseCountForOne = math.ceil(len(files) / config.CPUCores)
        childPIDList = list()

        for i in range (config.CPUCores):
            pid = os.fork()
            if (pid == 0):
                startIndex = i * caseCountForOne
                endIndex = min((i + 1) * caseCountForOne, len(files))   # this index is not included
                combineFiles(files[startIndex:endIndex])
                os._exit(0)
            else:
                IOUtils.showInfo(f'Forked subprocess with pid {pid}')
                childPIDList.append(pid)
        
        for pid in childPIDList:
            os.waitpid(pid, 0)
    else:
        combineFiles(files)

        
    IOUtils.showInfo("Combination finished")
    
if (__name__ == '__main__'):
    main()