import sys
import importlib
sys.path.append('.')

from config import config
from utils import IOUtils
from utils.HPOUtils import HPOUtils
from utils.DiseaseUtils import DiseaseUtils
from utils.GeneUtils import GeneUtils

extractAnnotation = importlib.import_module('src.1_extractAnnotation')
preprocess = importlib.import_module('src.2_preprocess')
precalculate = importlib.import_module('src.3_precalculate')
Phen2Disease = importlib.import_module('src.4_Phen2Disease')
combine = importlib.import_module('src.5_combine')
evaluate = importlib.import_module('src.6_evaluate')

def setVersion(HPOVersion):
    config.HPOVersion = HPOVersion
    config.resetPath()

def setDataset(datasetName, taskType):
    config.datasetName = datasetName
    config.taskType = taskType
    config.resetPath()

def setPreprocess(localProportion):
    config.localProportion = localProportion
    config.resetPath()

def setPreCalculate(ICType, similarityMethod):
    config.ICType = ICType
    config.similarityMethod = similarityMethod
    config.resetPath()

def setCalculate(useAncestor):
    config.useAncestor = useAncestor
    config.resetPath()

def setCombine(params):
    config.scoreCombineMethods = params[0]
    if (config.taskType == 'disease'):
        config.gene2DiseaseMethod = params[1]
        config.gene2DiseaseProportionMethod = params[2]
        config.maxGeneProportion = params[3]
    else:
        config.disease2GeneMethod = params[1]
        config.disease2GeneProportionMethod = params[2]
        config.maxDiseaseProportion = params[3]
    config.usePPI = params[4]
    config.selfProportion = params[5]
    config.directProportion = params[6]
    config.indirectProportion = params[7]
    config.directScoreMethod = params[8]
    config.resetPath()

# def setTask(dataset, taskType, ICType, similarityMethod, HPOVersion):
#     config.datasetName = dataset
#     config.taskType = taskType
#     config.ICType = ICType
#     config.similarityMethod = similarityMethod
#     config.HPOVersion = HPOVersion
#     config.resetPath()

# def preprocessTask(ICType, HPOVersion):
#     config.autoLoadAnnotation = False
#     config.ICType = ICType
#     config.HPOVersion = HPOVersion
#     config.resetPath()
#     IOUtils.init()
#     preprocess.main()

# def setAutoAnnotation():
#     config.autoLoadAnnotation = True
#     HPOUtils.loadIC()
#     HPOUtils.loadSimilarity()

#     IOUtils.showInfo('Switch to evaluate mode')



# def runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, reCalculate=True):
#     setTask(dataset, taskType, ICType, similarityMethod, HPOVersion)
#     if (reCalculate):
#         Phen2Disease.main()
#     combine.main()
#     evaluate.main()

# def runAll(dataset, taskType, HPOVersion, reCalculate=True):
#     # ICTypes = ['disease', 'gene', 'integrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
#     ICTypes = ['disease', 'gene', 'integrated', 'local', 'diseaseIntegrated', 'geneIntegrated', 'integratedIntegrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
#     # similarityMethods = ['Lin', 'JC', 'IC', 'phrank', 'phenoBrain']
#     similarityMethods = ['Lin', 'JC', 'IC']

#     if (not reCalculate):
#         ICTypes = ['disease', 'gene', 'local', 'integrated']
#         similarityMethods = ['JC', 'IC']

#     for ICType in ICTypes:
#         for similarityMethod in similarityMethods:
#             runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, reCalculate)

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
            
# def testCombine(dataset, taskType, ICType, similarityMethod, HPOVersion, scoreCombineMethods):
#     setCombineMethods(scoreCombineMethods, 'max', 'float', 1, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'max', 'float', 0.9, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'max', 'fixed', 1, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'max', 'fixed', 0.9, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'average', 'float', 1, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'average', 'float', 0.9, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'average', 'fixed', 1, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'average', 'fixed', 0.9, False, 1, 1, 1, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)

#     setCombineMethods(scoreCombineMethods, 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     # setCombineMethods(scoreCombineMethods, 'max', 'float', 0.9, True, 0.1, 0.1, 0.8, 'average')
#     # runTask(dataset, taskType, ICType, similarityMethod, HPOVersion)
#     # setCombineMethods(scoreCombineMethods, 'max', 'float', 0.9, True, 0.2, 0.3, 0.5, 'average')
#     # runTask(dataset, taskType, ICType, similarityMethod, HPOVersion)
#     setCombineMethods(scoreCombineMethods, 'max', 'fixed', 1, True, 0.1, 0.1, 0.8, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     setCombineMethods(scoreCombineMethods, 'max', 'fixed', 1, True, 0.2, 0.3, 0.5, 'average')
#     runTask(dataset, taskType, ICType, similarityMethod, HPOVersion, False)
#     # setCombineMethods(scoreCombineMethods, 'max', 'fixed', 0.9, True, 0.1, 0.1, 0.8, 'average')
#     # runTask(dataset, taskType, ICType, similarityMethod, HPOVersion)
#     # setCombineMethods(scoreCombineMethods, 'max', 'fixed', 0.9, True, 0.2, 0.3, 0.5, 'average')
#     # runTask(dataset, taskType, ICType, similarityMethod, HPOVersion)

def preprocessAll():  # assume version, dataset are set
    # localProportions = [1, 0.75, 0.5, 0.25]
    localProportions = [0.5]
    # ICTypes = ['disease', 'gene', 'integrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
    # ICTypes = ['disease', 'gene', 'integrated', 'local', 'diseaseIntegrated', 'geneIntegrated', 'integratedIntegrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
    ICTypes = ['disease', 'gene', 'integrated', 'local']
    # similarityMethods = ['Lin', 'JC', 'IC', 'phrank', 'phenoBrain']
    similarityMethods = ['Lin', 'JC', 'IC']
    extractAnnotation.main()
    for localProportion in localProportions:
        setPreprocess(localProportion)
        preprocess.main()
    for ICType in ICTypes:
        for similarityMethod in similarityMethods:
            setPreCalculate(ICType, similarityMethod)
            if (ICType != 'local'):
                precalculate.main()
            else:
                for localProportion in localProportions:
                    setPreprocess(localProportion)
                    precalculate.main()

                



 
def runAll(combinations):  # assume version, dataset are set\
    # localProportions = [1, 0.75, 0.5, 0.25]
    localProportions = [0.5]
    # ICTypes = ['disease', 'gene', 'integrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
    # ICTypes = ['disease', 'gene', 'integrated', 'local', 'diseaseIntegrated', 'geneIntegrated', 'integratedIntegrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
    # ICTypes = ['phrankDisease', 'phrankGene', 'phrankIntegrated']
    # ICTypes = ['disease', 'gene', 'integrated', 'local']
    ICTypes = ['disease', 'gene', 'integrated', 'local']
    # similarityMethods = ['Lin', 'JC', 'IC', 'phrank', 'phenoBrain']
    similarityMethods = ['IC', 'Lin']
    # similarityMethods = ['Lin']
    # useAncestors = ['none', 'patient', 'target', 'both']
    useAncestors = ['none']

    # test for use ancestor
    # setPreprocess(localProportions[2])
    # setPreCalculate(ICTypes[0], similarityMethods[0])
    # for useAncestor in useAncestors:
    #     setCalculate(useAncestor)
    #     Phen2Disease.main()
    #     for combination in combinations:
    #         setCombine(combination[0], combination[1], combination[2], combination[3], combination[4], combination[5], combination[6], combination[7], combination[8])
    #         combine.main()
    #         evaluate.main()

    # # test for IC and similarity
    # setPreprocess(localProportions[2])
    # for ICType in ICTypes:
    #     for similarityMethod in similarityMethods:
    #         setPreCalculate(ICType, similarityMethod)
    #         setCalculate(useAncestors[0])
    #         Phen2Disease.main()
    #         for combination in combinations:
    #             setCombine(combination[0], combination[1], combination[2], combination[3], combination[4], combination[5], combination[6], combination[7], combination[8])
    #             combine.main()
    #             evaluate.main()

    # test for proportion
    # for localProportion in localProportions:
    #     setPreprocess(localProportion)
    #     # setPreCalculate(ICTypes[0], similarityMethods[0])
    #     setPreCalculate('local', similarityMethods[0])
    #     setCalculate(useAncestors[0])
    #     Phen2Disease.main()
    #     for combination in combinations:
    #         setCombine(combination[0], combination[1], combination[2], combination[3], combination[4], combination[5], combination[6], combination[7], combination[8])
    #         combine.main()
    #         evaluate.main()


    for localProportion in localProportions:
        setPreprocess(localProportion)
        for ICType in ICTypes:
            for similarityMethod in similarityMethods:
                setPreCalculate(ICType, similarityMethod)
                for useAncestor in useAncestors:
                    setCalculate(useAncestor)
                    Phen2Disease.main()
                    for combination in combinations:
                        setCombine(combination)
                        combine.main()
                        evaluate.main()

def main():
    HPOVersions = ['20231009']
    # datasets = {'data10': 'gene', 
    #             'data4-1': 'gene',
    #             'data5-2': 'gene'}
    # datasets = {'data5-1': 'gene', 
    #             'data5-3': 'gene',
    #             'data6': 'gene'}
    datasets = {
                # 'data3': 'disease',
                # 'data11-1': 'disease',
                'data11-2': 'disease',
                'data11-3': 'disease'
                }
    combinations = list()
    # combinations.append((['double'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['p2dg'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'float', 1, True, 0.01, 0.09, 0.9, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'float', 1, True, 0.5, 0.3, 0.2, 'average'))
    combinations.append((['double', 'p2dg'], 'max', 'float', 1, True, 0.8, 0.1, 0.1, 'average'))

    # combinations.append((['double', 'p2dg'], 'max', 'float', 0.8, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'float', 0.6, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'float', 0.4, True, 0.1, 0.1, 0.8, 'average'))
    combinations.append((['double', 'p2dg'], 'max', 'float', 0.2, True, 0.1, 0.1, 0.8, 'average'))

    combinations.append((['double', 'p2dg'], 'max', 'float', 0.2, True, 0.8, 0.1, 0.1, 'average'))
    combinations.append((['double', 'p2dg'], 'max', 'float', 0.2, False, 1, 1, 1, 'average'))
    combinations.append((['double', 'p2dg'], 'max', 'fixed', 0, False, 1, 1, 1, 'average'))

    # combinations.append((['double', 'p2dg'], 'max', 'fixed', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'fixed', 0.8, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'fixed', 0.6, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'fixed', 0.4, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'max', 'fixed', 0.2, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['p2dg', 'dg2p'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))

    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.5, 0.3, 0.2, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.8, 0.1, 0.1, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'float', 1, False, 1, 1, 1, 'average'))

    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'float', 0.9, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'float', 0.8, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'fixed', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'fixed', 0.9, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'max', 'fixed', 0.8, True, 0.1, 0.1, 0.8, 'average'))
    
    for HPOVersion in HPOVersions:
        setVersion(HPOVersion)
        for (dataset, taskType) in datasets.items():
            setDataset(dataset, taskType)
            if (dataset != 'data3' and dataset != 'data11-1' and dataset != 'data11-2'):
                preprocessAll()
            runAll(combinations)
            


    # preprocessTask(ICType='disease', HPOVersion='20231009')
    # preprocessTask(ICType='gene', HPOVersion='20231009')
    # preprocessTask(ICType='integrated', HPOVersion='20231009')
    # preprocessTask(ICType='phrankDisease', HPOVersion='20231009')
    # preprocessTask(ICType='phrankGene', HPOVersion='20231009')
    # preprocessTask(ICType='phrankIntegrated', HPOVersion='20231009')
    # preprocessTask(ICType='diseaseIntegrated', HPOVersion='20231009')
    # preprocessTask(ICType='geneIntegrated', HPOVersion='20231009')
    # preprocessTask(ICType='integratedIntegrated', HPOVersion='20231009')

    # useAncestors = ['both', 'patient', 'gene', 'none']

    # for dset in datasets:
    #     setTask(dset, 'gene', 'local', 'Lin', '20231009')
    #     preprocessTask('local', '20231009')
    #     setTask(dset, 'gene', 'localIntegrated', 'Lin', '20231009')
    #     preprocessTask('localIntegrated', '20231009')


    # # setAutoAnnotation()



    # for dset in datasets:
    #     for useAncestor in useAncestors:
    #         config.useAncestor = useAncestor
    #         # test for merge method
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', True)
    #         setCombineMethods(['double', 'p2dg'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['p2dg', 'dg2p'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['p2dg'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double'], 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)

    #         # test for ppi
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.5, 0.3, 0.2, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.8, 0.1, 0.1, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 1, False, 1, 1, 1, 'average')
    #         runAll(dset, 'gene', '20231009', False)

    #         # test for convert method
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 0.9, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 0.8, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'fixed', 1, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'fixed', 0.9, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)
    #         setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'fixed', 0.8, True, 0.1, 0.1, 0.8, 'average')
    #         runAll(dset, 'gene', '20231009', False)

        # setCombineMethods(['double', 'p2dg', 'dg2p'], 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average')
        # runAll(dset, 'gene', '20231009', False)
        # setCombineMethods(['double', 'p2dg'], 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average')
        # runAll(dset, 'gene', '20231009', False)
        # setCombineMethods(['p2dg', 'dg2p'], 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average')
        # runAll(dset, 'gene', '20231009', False)


    # runTask('data10', 'gene', 'diseaseIntegrated', 'Lin', '20231009')
    # runTask('data10', 'gene', 'geneIntegrated', 'Lin', '20231009')
    # runTask('data10', 'gene', 'integratedIntegrated', 'Lin', '20231009')

    # testCombine('data10', 'gene', 'disease', 'Lin', '20231009', ['double'])
    # testCombine('data10', 'gene', 'disease', 'Lin', '20231009', ['dg2p', 'p2dg'])
    # testCombine('data10', 'gene', 'disease', 'Lin', '20231009', ['double', 'p2dg'])
    # testCombine('data10', 'gene', 'disease', 'Lin', '20231009', ['double', 'dg2p'])
    # testCombine('data10', 'gene', 'disease', 'Lin', '20231009', ['double', 'dg2p', 'p2dg'])

    # testCombine('data10', 'gene', 'integrated', 'JC', '20231009', ['double'])
    # testCombine('data10', 'gene', 'integrated', 'JC', '20231009', ['dg2p', 'p2dg'])
    # testCombine('data10', 'gene', 'integrated', 'JC', '20231009', ['double', 'p2dg'])
    # testCombine('data10', 'gene', 'integrated', 'JC', '20231009', ['double', 'dg2p'])
    # testCombine('data10', 'gene', 'integrated', 'JC', '20231009', ['double', 'dg2p', 'p2dg'])

    # testCombine('data10', 'gene', 'gene', 'JC', '20231009', ['double'])
    # testCombine('data10', 'gene', 'gene', 'JC', '20231009', ['dg2p', 'p2dg'])
    # testCombine('data10', 'gene', 'gene', 'JC', '20231009', ['double', 'p2dg'])
    # testCombine('data10', 'gene', 'gene', 'JC', '20231009', ['double', 'dg2p'])
    # testCombine('data10', 'gene', 'gene', 'JC', '20231009', ['double', 'dg2p', 'p2dg'])
    
    # testCombine('data10', 'gene', 'gene', 'IC', '20231009', ['double'])
    # testCombine('data10', 'gene', 'gene', 'IC', '20231009', ['dg2p', 'p2dg'])
    # testCombine('data10', 'gene', 'gene', 'IC', '20231009', ['double', 'p2dg'])
    # testCombine('data10', 'gene', 'gene', 'IC', '20231009', ['double', 'dg2p'])
    # testCombine('data10', 'gene', 'gene', 'IC', '20231009', ['double', 'dg2p', 'p2dg'])
    

    # runTask('data10', 'gene', 'disease', 'Lin', '20231009')
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


    IOUtils.showInfo('Batch process finished')


if (__name__ == '__main__'):
    main()
