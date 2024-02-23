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
    HPOUtils.loadAll()
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
    Phen2Disease.main()
    combine.main()
    evaluate.main()

def main():
    preprocessTask(ICType='disease', HPOVersion='20231009')
    preprocessTask(ICType='gene', HPOVersion='20231009')
    preprocessTask(ICType='integrated', HPOVersion='20231009')
    setAutoAnnotation()
    runTask(dataset='data3', taskType='disease', ICType='disease', similarityMethod='Lin', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='gene', similarityMethod='Lin', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='integrated', similarityMethod='Lin', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='disease', similarityMethod='JC', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='gene', similarityMethod='JC', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='integrated', similarityMethod='JC', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='disease', similarityMethod='IC', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='gene', similarityMethod='IC', HPOVersion='20231009')
    runTask(dataset='data3', taskType='disease', ICType='integrated', similarityMethod='IC', HPOVersion='20231009')

if (__name__ == '__main__'):
    preprocessTask(ICType='disease', HPOVersion='20231009')
    setAutoAnnotation()
    evaluate.main()
    # runTask(dataset='data3', taskType='disease', ICType='disease', similarityMethod='Lin', HPOVersion='20231009')
    # runTask(dataset='data6', taskType='gene', ICType='disease', similarityMethod='Lin', HPOVersion='20231009')