import sys
import os
import numpy
sys.path.append(".")

from config import config
from analysis import HPOAnalysis
import utils.IOUtils as IOUtils
from utils.HPOUtils import HPOUtils
from utils.DiseaseUtils import DiseaseUtils
from utils.GeneUtils import GeneUtils

# when the case has multiple standard diseases, here is the method to calculate the final index(rank) of the prediction
def calcIndex(indexes):
    if (len(indexes) == 1):
        return indexes[0]
    else:
        return numpy.min(indexes)

def main():
    # if run direct after combine, then there is no need to init again
    # HPOUtils.loadIC()
    # GeneUtils.reset()
    # DiseaseUtils.reset()
    files = sorted(os.listdir(config.standardResultPath))
    result = dict()

    separateTops = {
        category: {
            'tops': {topNum: 0 for topNum in config.focusTop},
            'MRR': 0,
            'totalCount': 0
        }
        for category in sorted(config.HPOClasses.values())
    }
    separateTops['None'] = {
        'tops': {topNum: 0 for topNum in config.focusTop},
        'MRR': 0,
        'totalCount': 0
    }
    separateTops['All'] = {
        'tops': {topNum: 0 for topNum in config.focusTop},
        'MRR': 0,
        'totalCount': 0
    }

    if (config.taskType == 'disease'):
        resultIndex = 0
    else:
        resultIndex = 1
    for file in files:
        # skip folders
        if (os.path.isdir(f"{config.standardResultPath}/{file}")):
            continue

        indexes = list()
        with open(f"{config.standardResultPath}/{file}") as fp:
            lines = fp.readlines()
        standardResults = [line.strip() for line in lines]
        standardResultTypeDistribution = HPOAnalysis.getStandardResultType(standardResults)
        if (len(list(standardResultTypeDistribution.keys())) > 0):
            standardResultType = list(standardResultTypeDistribution.keys())[0]
        else:
            standardResultType = 'None'

        with open(f"{config.resultPath}/{file}.csv") as fp:
            line = fp.readline().strip()
            currentIndex = -1
            while (line):
                currentIndex += 1
                if (line.split(',')[resultIndex].strip() in standardResults):
                    indexes.append(currentIndex)
                    break
                line = fp.readline().strip()

        if (len(indexes) == 0):
            result[file] = ('NIL', standardResultType)
        else:
            index = calcIndex(indexes)
            separateTops[standardResultType]['MRR'] += 1/index
            separateTops['All']['MRR'] += 1/index
            for threshold in config.focusTop:
                if (index <= threshold):
                    separateTops[standardResultType]['tops'][threshold] += 1
                    separateTops['All']['tops'][threshold] += 1
            result[file] = (index, standardResultType)

        separateTops[standardResultType]['totalCount'] += 1
        separateTops['All']['totalCount'] += 1

    # output module
    # output rank for each case
    res = list()
    res.append("name,rank,type\n")
    for (name, index) in result.items():
        res.append(f"{name},{index[0]},{index[1]}\n")

    # output summary of this dataset
    IOUtils.showInfo(f'Result for {config.combineParams}')
    topsTitle = ""
    for threshold in config.focusTop:
        topsTitle += f'top {threshold}\t'

    IOUtils.showInfo(f"{topsTitle} MRR \tcategory")
    topsTitle = topsTitle.replace('\t', ',')
    res.append(f"\ncategory,{topsTitle}MRR,n\n")

    separateTops = dict(sorted(separateTops.items(), key=lambda pair:pair[1]['totalCount'], reverse=True))

    for (category, categoryResult) in separateTops.items():
        topsContent = ""
        if (categoryResult['totalCount'] == 0):
            for threshold in config.focusTop:
                topsContent += "--   \t"
            MRRText = "--"
        else:
            for threshold in config.focusTop:
                topsContent += f"{(100 * categoryResult['tops'][threshold] / categoryResult['totalCount']):.2f}%\t"
            MRRText = f"{(100 * categoryResult['MRR'] / categoryResult['totalCount']):.2f}"
        IOUtils.showInfo(f"{topsContent}{MRRText} \t{category} (n={categoryResult['totalCount']})")
        topsContent = topsContent.replace('\t', ',')
        res.append(f"{category} (n={categoryResult['totalCount']}),{topsContent}{MRRText},{categoryResult['totalCount']}\n")

    # print("rank\tnum\tratio")
    # res.append("\nrank, num, ratio\n")
    # for (threshold, count) in tops.items():
    #     print(f"top{threshold}\t{count}\t{(100*count/totalCount):.2f}%")
    #     res.append(f"top{threshold},{count},{(100*count/totalCount):.2f}%\n")
    # print(f"\nMRR {(100*MRR/totalCount):.2f}")
    # res.append(f"\nMRR,{(100*MRR/totalCount):.2f}")


    with open(config.resultCSVPath, 'wt', encoding='utf-8') as fp:
        fp.writelines(res)

if (__name__ == '__main__'):
    main()
