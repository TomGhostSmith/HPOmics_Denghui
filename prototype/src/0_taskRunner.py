import sys
import importlib
sys.path.append('.')

from config import config
from utils import IOUtils
from utils.HPOUtils import HPOUtils
from utils.DiseaseUtils import DiseaseUtils
from utils.GeneUtils import GeneUtils

preprocess = importlib.import_module('src.1_preprocess')
Phen2Disease = importlib.import_module('src.2_Phen2Disease')
combine = importlib.import_module('src.3_combine')
evaluate = importlib.import_module('src.4_evaluate')

def preprocessTask(ICType, HPOVersion):
    config.autoLoadAnnotation = False
    config.ICType = ICType
    config.HPOVersion = HPOVersion
    config.resetPath()
    IOUtils.init()
    preprocess.main()

def setAutoAnnotation():
    config.autoLoadAnnotation = True
    HPOUtils.loadIC()
    HPOUtils.loadSimilarity()
    DiseaseUtils.reset()
    GeneUtils.reset()
    IOUtils.showInfo('Switch to evaluate mode')
    

def runTask(dataset, taskType, ICType, similarityMethod, HPOVersion):
    config.datasetName = dataset
    config.taskType = taskType
    config.ICType = ICType
    config.similarityMethod = similarityMethod
    config.HPOVersion = HPOVersion
    config.resetPath()
    IOUtils.init()
    HPOUtils.loadIC()
    HPOUtils.loadSimilarity()   # still need to load because HPOVersion and IC type may be different
    Phen2Disease.main()
    combine.main()
    evaluate.main()

def runAll(dataset, taskType, HPOVersion):
    ICTypes = ['disease', 'gene', 'integrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
    similarityMethods = ['Lin', 'JC', 'IC', 'phrank', 'phenoBrain']

    for ICType in ICTypes:
        for similarityMethod in similarityMethods:
            runTask(dataset, taskType, ICType, similarityMethod, HPOVersion)

    # runTask(dataset, taskType, ICType='disease', similarityMethod='Lin', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='gene', similarityMethod='Lin', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='integrated', similarityMethod='Lin', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='disease', similarityMethod='JC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='gene', similarityMethod='JC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='integrated', similarityMethod='JC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='disease', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='gene', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='integrated', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='disease', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='gene', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='integrated', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='disease', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='gene', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='integrated', similarityMethod='IC', HPOVersion=HPOVersion)

    # runTask(dataset, taskType, ICType='phrankDisease', similarityMethod='Lin', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankGene', similarityMethod='Lin', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankIntegrated', similarityMethod='Lin', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankDisease', similarityMethod='JC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankGene', similarityMethod='JC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankIntegrated', similarityMethod='JC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankDisease', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankGene', similarityMethod='IC', HPOVersion=HPOVersion)
    # runTask(dataset, taskType, ICType='phrankIntegrated', similarityMethod='IC', HPOVersion=HPOVersion)



def main():
    config.useSynonym = False
    config.resetPath()
    # preprocessTask(ICType='disease', HPOVersion='20231009')
    # preprocessTask(ICType='gene', HPOVersion='20231009')
    # preprocessTask(ICType='integrated', HPOVersion='20231009')
    # preprocessTask(ICType='phrankDisease', HPOVersion='20231009')
    # preprocessTask(ICType='phrankGene', HPOVersion='20231009')
    # preprocessTask(ICType='phrankIntegrated', HPOVersion='20231009')
    setAutoAnnotation()
    runTask('data10', 'gene', 'disease', 'Lin', '20231009')
    # runAll('data10', 'gene', '20231009')
    # runAll('data10', 'gene', '20221005')
    # runAll('data3', 'disease', '20231009')
    # runAll('data3', 'disease', '20221005')
    # runAll('data4-1', 'gene', '20231009')
    # runAll('data4-1', 'gene', '20221005')
    # runAll('data5-1', 'gene', '20231009')
    # runAll('data5-1', 'gene', '20221005')
    # runAll('data5-2', 'gene', '20231009')
    # runAll('data5-2', 'gene', '20221005')
    # runAll('data5-3', 'gene', '20231009')
    # runAll('data5-3', 'gene', '20221005')
    # runAll('data6', 'gene', '20231009')
    # runAll('data6', 'gene', '20221005')
    # runAll('data10', 'gene', '20231009')
    # runAll('data10', 'gene', '20210413')
    # runAll('data10', 'gene', '20221005')
    # runAll('data11-1', 'disease', '20231009')
    # runAll('data11-1', 'disease', '20221005')
    # runAll('data11-2', 'disease', '20231009')
    # runAll('data11-2', 'disease', '20221005')
    # runAll('data11-3', 'disease', '20231009')
    # runAll('data11-3', 'disease', '20221005')


if (__name__ == '__main__'):
    main()
