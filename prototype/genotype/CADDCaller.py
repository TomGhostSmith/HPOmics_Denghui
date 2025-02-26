import os
import subprocess
import gzip
import multiprocessing
import json
import sys
import math

import time

sys.path.append('.')

from config import config
from utils import IOUtils

def processOneFile(inputPath, outputPath):
    params = ["-a", "-g", "GRCh38", "-c", "12", "-o", outputPath, inputPath]
    subprocess.run(['bash', config.CADDPath] + params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    scores = dict()

    while (not os.path.exists(outputPath)):
        time.sleep(0.5)

    with gzip.open(filename=outputPath, mode='rt') as fp:
        fp.readline()  # skip first line
        title = fp.readline().strip()[1:]
        titleTerms = title.split('\t')
        geneNameIndex = titleTerms.index('GeneName')
        scoreIndex = titleTerms.index('PHRED')

        line = fp.readline()
        while (line):
            terms = line.strip().split('\t')
            geneName = terms[geneNameIndex]
            score = float(terms[scoreIndex])
            if (geneName  != 'NA'):
                if (scores.get(geneName) == None or scores.get(geneName) < score):
                    scores[geneName] = score

            line = fp.readline()
        
    
    os.remove(path=outputPath)
    return scores

def processOneCase(file):
    # if (config.supportFork):
    if (not os.path.exists(f"{config.CADDInputFolder}/{file}")):
        return dict()
    elif (config.useForkWhenCADD):
        manager = multiprocessing.Manager()
        scores = manager.dict()

        lock = manager.Lock()
        # lock = multiprocessing.Lock()
        lines = list()
        with open(file=f"{config.CADDInputFolder}/{file}", mode='rt') as fp:
            for line in fp:
                if (line.startswith("##")):
                    continue
                elif (line.startswith("#")):
                    titleLine = line
                else:
                    lines.append(line)
        
        lineCountPerProcess = math.ceil(len(lines) / config.CPUCores)
        childPIDList = list()
        for i in range(config.CPUCores):
            pid = os.fork()
            if (pid == 0):
                startIndex =  i * lineCountPerProcess
                endIndex = min((i + 1) * lineCountPerProcess, len(lines))
                inputPath = f"{config.CADDTempFolder}/{i}-{file}"
                outputPath = f"{config.CADDTempFolder}/{i}-{file.replace('.vcf', '.tsv.gz')}"
                with open(file=inputPath, mode='wt', encoding='utf-8') as fp:
                    fp.write(titleLine)
                    fp.writelines(lines[startIndex:endIndex])
                
                thisScores = processOneFile(inputPath, outputPath)
                lock.acquire()
                for (geneName, score) in thisScores.items():
                    if (scores.get(geneName) == None or scores.get(geneName) < score):
                        scores[geneName] = score
                lock.release()

                os._exit(0)
            else:
                IOUtils.showInfo(f'Forked subprocess with pid {pid}', 'PROC')
                childPIDList.append(pid)
        
        for pid in childPIDList:
            os.waitpid(pid, 0)
        
    else:
        inputPath = f"{config.CADDInputFolder}/{file}"
        outputPath = f"{config.CADDOutputFolder}/{file.replace('.vcf', '.tsv.gz')}"
        scores = processOneFile(inputPath, outputPath)

    # only use in test
    scores = dict(sorted(scores.items(), key=lambda pair:pair[1], reverse=True))
    with open(f"{config.CADDOutputFolder}/{file.replace('.vcf', '')}.json", mode='wt') as fp:
        json.dump(scores, fp, indent=2)
    return scores


def main():
    files = os.listdir(config.CADDInputFolder)
    count = 0
    IOUtils.showInfo('startProcess')
    fileList = multiprocessing.Queue()
    totalCount = len(files)
    for file in files:
        count += 1
        if (count < 0):
            IOUtils.showInfo(f"skip {file} {count}/{len(files)}", "PROC")
            continue
        if (os.path.isdir(f"{config.CADDInputFolder}/{file}")):
            IOUtils.showInfo(f"skip folder {file} {count}/{len(files)}", "PROC")
            continue
        # if (os.path.exists(f"{config.CADDOutputFolder}/{file.replace('.vcf', '.json')}")):
        #     continue
        fileList.put((file, count))

    if (config.supportFork):
        queueLock = multiprocessing.Lock()
        childPIDList = list()

        for _ in range (config.CPUCores):
            pid = os.fork()
            if (pid == 0):
                while True:
                    queueLock.acquire()
                    if (fileList.empty()):
                        queueLock.release()
                        break
                    (file, index) = fileList.get()
                    queueLock.release()
                    processOneCase(file)
                    IOUtils.showInfo(f"[{index}/{totalCount}] Processed {str(file)}")
                os._exit(0)
            else:
                IOUtils.showInfo(f'Forked subprocess with pid {pid}', 'PROC')
                childPIDList.append(pid)
        
        for pid in childPIDList:
            os.waitpid(pid, 0)
            
        IOUtils.showInfo("VCF files processed")


if (__name__ == "__main__"):
    main()