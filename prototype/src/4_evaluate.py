import sys
import os
import numpy
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils

# when the case has multiple standard diseases, here is the method to calculate the final index(rank) of the prediction
def calcIndex(indexes):
    if (len(indexes) == 1):
        return indexes[0]
    else:
        return numpy.min(indexes)

def main():
    files = os.listdir(config.standardResultPath)
    result = dict()

    MRR = 0

    tops = dict()
    tops[1] = 0
    tops[3] = 0
    tops[5] = 0
    tops[10] = 0
    tops[20] = 0
    tops[50] = 0
    tops[100] = 0

    totalCount = len(files)
    if (config.taskType == 'disease'):
        resultIndex = 0
    else:
        resultIndex = 1
    for file in files:
        # skip folders
        if (os.path.isdir(f"{config.standardResultPath}/{file}")):
            totalCount -= 1
            continue

        indexes = list()
        with open(f"{config.standardResultPath}/{file}") as fp:
            lines = fp.readlines()
        standardResults = [line.strip() for line in lines]
        with open(f"{config.resultPath}/{file}.csv") as fp:
            line = fp.readline().strip()
            currentIndex = -1
            while (line):
                currentIndex += 1
                if (line.split(',')[resultIndex].strip() in standardResults):
                    indexes.append(currentIndex)
                line = fp.readline().strip()

            if (len(indexes) == 0):
                result[file] = 'NIL'
            else:
                index = calcIndex(indexes)
                MRR += 1/index
                for threshold in tops.keys():
                    if (index <= threshold):
                        tops[threshold] += 1
                result[file] = index


    res = list()
    res.append("name,rank\n")
    for (name, index) in result.items():
        res.append(f"{name},{index}\n")

    print("rank\tnum\tratio")
    res.append("\nrank, num, ratio\n")
    for (threshold, count) in tops.items():
        print(f"top{threshold}\t{count}\t{(100*count/totalCount):.2f}%")
        res.append(f"top{threshold},{count},{(100*count/totalCount):.2f}%\n")
    print(f"\nMRR {(100*MRR/totalCount):.2f}")
    res.append(f"\nMRR,{(100*MRR/totalCount):.2f}")


    with open(config.resultCSVPath, 'wt', encoding='utf-8') as fp:
        fp.writelines(res)

if (__name__ == '__main__'):
    main()