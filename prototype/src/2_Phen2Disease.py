import sys
import os
import numpy
import json
import multiprocessing
sys.path.append(".")

from config import config
import utils.IOUtils as IOUtils
from utils.HPOUtils import HPOUtils
from model.Patient import Patient
from utils.DiseaseUtils import DiseaseUtils
from utils.GeneUtils import GeneUtils

def evaluateOne(file):
    # extract file name
    dotIndex = str(file).rfind('.')
    if (dotIndex != -1):
        fileName = str(file)[:dotIndex]
    else:
        fileName = str(file)

    # extract HPO term and replace old term with new
    with open(file=f"{config.patientPath}/{file}", mode='rt', encoding='utf-8') as fp:
        HPOList, totalIC = HPOUtils.extractPreciseHPONodes(fp.readlines())
    
    patient = Patient(fileName=fileName, HPOList=HPOList, info=None, taskType=config.taskType, totalIC=totalIC)  # info can be used in the future

    if (patient.taskType == 'disease'):
        DiseaseUtils.evaluate(patient)
    else:
        GeneUtils.evaluate(patient)

    with open(file=f'{config.splitResultPath}/{fileName}.csv', mode='wt', encoding='utf-8') as fp:
        fp.writelines(patient.getResult())


def evaluate():
    patientFiles = sorted(os.listdir(config.patientPath))
    processedCount = 0
    totalCount = len(patientFiles)

    # start and end index can be modified to skip some patient
    startIndex = 0
    # endIndex = 1
    endIndex = len(patientFiles)

    # pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # manager = multiprocessing.Manager()
    # diseaseEvaluatorManager = manager.Namespace()
    # diseaseEvaluatorManager.instance = diseaseEvaluator

    # geneEvaluatorManager = manager.Namespace()
    # geneEvaluatorManager.instance = diseaseEvaluator

    fileQueue = multiprocessing.Queue()
    # fileQueue = list()

    for file in patientFiles:
        # skip folders
        if (os.path.isdir(f"{config.patientPath}/{file}")):
            processedCount += 1
            IOUtils.showInfo(f"[{processedCount}/{totalCount}] Skipped folder {str(file)}")
            continue

        # check index to skip some patients do not need to process
        if (processedCount < startIndex or processedCount >= endIndex):
            processedCount += 1
            IOUtils.showInfo(f"[{processedCount}/{totalCount}] Skipped file {str(file)}")
            continue



        # dotIndex = str(file).rfind('.')
        # if (dotIndex != -1):
        #     fileName = str(file)[:dotIndex]
        # else:
        #     fileName = str(file)

        # # extract HPO term and replace old term with new
        # with open(file=f"{config.patientPath}/{file}", mode='rt', encoding='utf-8') as fp:
        #     HPOList, totalIC = HPOUtils.extractPreciseHPONodes(HPOTree, fp.readlines())
        
        # patient = Patient(fileName=fileName, HPOList=HPOList, info=None, taskType=config.taskType, totalIC=totalIC)  # info can be used in the future

        


            # test: use all ancestors
            # HPOInput = fp.readlines()
            # totalIC = 0
            # HPOList = set()
            # HPONodes = list(HPOTree.HPOList.values())
            # for HPOTerm in HPOInput:
            #     validNode = HPOTree.getHPO(HPOTerm.strip())
            #     if (validNode != None):
            #         HPOList.add(validNode)
            #         for ancestorIndex in validNode.ancestorIndexs:
            #             HPOList.add(HPONodes[ancestorIndex])
            # for HPONode in HPOList:
            #     totalIC += HPOTree.ICList[HPONode.index]
        

        # can be modified to execute disease task and gene task customly

        # evaluate case
        processedCount += 1

        fileQueue.put((file, processedCount))
        # fileQueue.append((file, processedCount))
        

        

        # geneEvaluator.addTask(file)

        # pool.apply_async(func=evaluateOne, args=(HPOTree, diseaseEvaluatorManager, geneEvaluatorManager, file, processedCount))

        # p = multiprocessing.Process(target=evaluateOne, args=(HPOTree, diseaseEvaluator, geneEvaluator, file, processedCount))
        # processes.append((processedCount, file, p))
        # p.start()
        # IOUtils.showInfo(f"[{processedCount}/{totalCount}] Loaded task for file {str(file)}")
    
    if (config.supportFork):
        fileQueueLock = multiprocessing.Lock()
        childPIDList = list()

        for _ in range (config.CPUCores):
            pid = os.fork()
            if (pid == 0):
                while True:
                    fileQueueLock.acquire()
                    if (fileQueue.empty()):
                    # if (len(fileQueue) == 0):
                        fileQueueLock.release()
                        break
                    (task, index) = fileQueue.get()
                    # (task, index) = fileQueue.pop(0)
                    fileQueueLock.release()
                    evaluateOne(task, index)
                    IOUtils.showInfo(f"[{index}/{totalCount}] Processed {str(task)}")
                os._exit(0)
            else:
                IOUtils.showInfo(f'Forked subprocess with pid {pid}')
                childPIDList.append(pid)
        
        for pid in childPIDList:
            os.waitpid(pid, 0)
    else:
        while (not fileQueue.empty()):
            (task, index) = fileQueue.get()
            evaluateOne(task)
            IOUtils.showInfo(f"[{index}/{totalCount}] Processed {str(task)}")
    


    # pool.close()
    # pool.join()
        
    # processedCount = startIndex
    # for (index, file, p) in processes:
    #     p.join()

def main():
    IOUtils.showInfo("Start evaluate")
    evaluate()
    IOUtils.showInfo("Process finished")

if (__name__ == '__main__'):
    main()