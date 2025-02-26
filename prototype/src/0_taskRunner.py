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
    config.CADDMethod = params[1]
    config.CADDMinValue = params[2]
    config.CADDMAxProportion = params[3]
    if (config.taskType == 'disease'):
        config.gene2DiseaseMethod = params[4]
        config.gene2DiseaseProportionMethod = params[5]
        config.maxGeneProportion = params[6]
    else:
        config.disease2GeneMethod = params[4]
        config.disease2GeneProportionMethod = params[5]
        config.maxDiseaseProportion = params[6]
    config.usePPI = params[7]
    config.selfProportion = params[8]
    config.directProportion = params[9]
    config.indirectProportion = params[10]
    config.directScoreMethod = params[11]
    config.resetPath()

def preprocessAll():  # assume version, dataset are set
    # localProportions = [1, 0.75, 0.5, 0.25]
    localProportions = [0.5]
    # ICTypes = ['disease', 'gene', 'integrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
    # ICTypes = ['disease', 'gene', 'integrated', 'local', 'diseaseIntegrated', 'geneIntegrated', 'integratedIntegrated', 'phrankDisease', 'phrankGene', 'phrankIntegrated']
    # ICTypes = ['disease', 'gene', 'integrated', 'local']
    ICTypes = ['disease']
    # similarityMethods = ['Lin', 'JC', 'IC', 'phrank', 'phenoBrain']
    # similarityMethods = ['Lin', 'JC', 'IC']
    similarityMethods = ['Lin']
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
    # ICTypes = ['disease', 'gene', 'integrated', 'local']
    # ICTypes = ['disease']  # Phen2Disease all
    ICTypes = ['integrated'] # Phen2Disease2 all
    # ICTypes = ['gene']   
    # ICTypes = ['disease', 'integrated']
    # similarityMethods = ['Lin', 'JC', 'IC', 'phrank', 'phenoBrain']
    # similarityMethods = ['IC', 'Lin', 'JC']
    # similarityMethods = ['Lin']   # Phen2Disease all
    similarityMethods = ['IC']  # Phen2Disease2 all
    # similarityMethods = ['Lin', 'IC']
    # useAncestors = ['none', 'patient', 'target', 'both']
    # useAncestors = ['none', 'target']
    useAncestors = ['target']  # Phen2Disease2 clinical
    # useAncestors = ['none']      # Phen2Disease all, Phen2Disease2 non-clinical

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
                    # Phen2Disease.main()
                    for combination in combinations:
                        setCombine(combination)
                        combine.main()
                        evaluate.main()

def main():
    HPOVersions = ['20231009']
    datasets = {
                # 'data3': 'disease',
                'data4-1': 'gene',
                # 'data5-1': 'gene', 
                # 'data5-2': 'gene',
                # 'data5-3': 'gene',
                # 'data6': 'gene',
                # 'data10': 'gene', 
                # 'data11-1': 'disease',
                # 'data11-2': 'disease',
                # 'data11-3': 'disease',
                # 'data12': 'disease'
                }
    combinations = list()

    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0, False, 1, 0, 0, 'average'))  # Phen2Disease disease
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 1, False, 1, 0, 0, 'average'))  # Phen2Disease gene
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, False, 1, 0, 0, 'average'))  # Phen2Disease2 disease
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average'))  # Phen2Disease2 gene
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, "broadcast", 1, 0, 0, 'average'))  # Phen2Disease2 disease with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, "broadcast", 0.8, 0, 0.2, 'average'))  # Phen2Disease2 disease with new PPI
    # -- # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, "broadcast", 0.6, 0, 0.4, 'average'))  # Phen2Disease2 disease with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, "broadcast", 0.4, 0, 0.6, 'average'))  # Phen2Disease2 disease with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, "broadcast", 0.2, 0, 0.8, 'average'))  # Phen2Disease2 disease with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, "broadcast", 1, 0, 0, 'average'))  # Phen2Disease2 gene with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, "broadcast", 0.8, 0, 0.2, 'average'))  # Phen2Disease2 gene with new PPI
    combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, "broadcast", 0.6, 0, 0.4, 'average'))  # Phen2Disease2 gene with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, "broadcast", 0.4, 0, 0.6, 'average'))  # Phen2Disease2 gene with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, "broadcast", 0.2, 0, 0.8, 'average'))  # Phen2Disease2 gene with new PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, True, 0.2, 0.3, 0.5, 'average'))  # Phen2Disease2 disease with PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, False, 1, 0, 0, 'average'))  # Phen2Disease2 gene without PPI
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.8, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 0.8, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.6, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 0.6, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.4, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 0.4, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 0.2, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 0.2, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, True, 0.8, 0.1, 0.1, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, True, 0.5, 0.3, 0.2, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'fixed', 1, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'none', 0, 0, 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average'))
    # combinations.append((['double', 'p2dg'], 'fixed', 0, 0.2, 'max', 'fixed', 0.6, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'fixed', 0, 0.4, 'max', 'fixed', 0.6, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'fixed', 0, 0.6, 'max', 'fixed', 0.6, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'fixed', 0, 0.8, 'max', 'fixed', 0.6, False, 1, 0, 0, 'average'))
    # combinations.append((['double', 'p2dg'], 'fixed', 0, 1, 'max', 'fixed', 0.6, False, 1, 0, 0, 'average'))
    config.HPOmcisOutput = False
    config.inputType = 'plain'
    config.CADDMethod = 'none'
    # minValues = [0, 0.2, 0.4, 0.6, 0.8]
    # combinations.append((['double'], 'multiply', 0.5, 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['p2dg'], 'multiply', 0.5, 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'multiply', 0.5, 'max', 'float', 1, True, 0.01, 0.09, 0.9, 'average'))

    # for minValue in minValues:
    # minValue = 0
    # maxProportions = [1, 0.8, 0.6, 0.4, 0.2]
    # maxProportions = [1]
    # for maxProportion in maxProportions:
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 1, True, 0.1, 0.1, 0.8, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 1, True, 0.2, 0.3, 0.5, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 1, True, 0.5, 0.3, 0.2, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 1, True, 0.8, 0.1, 0.1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 1, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.45, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.5, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.55, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.65, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.6, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.75, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.8, True, 0.1, 0.1, 0.8, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.8, True, 0.2, 0.3, 0.5, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.8, True, 0.5, 0.3, 0.2, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.8, True, 0.8, 0.1, 0.1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.8, False, 1, 1, 1, 'average'))

        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.6, True, 0.8, 0.1, 0.1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.4, True, 0.8, 0.1, 0.1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.2, True, 0.8, 0.1, 0.1, 'average'))
        
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.6, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.4, False, 1, 1, 1, 'average'))
        # combinations.append((['double', 'p2dg'], 'fixed', minValue, maxProportion, 'max', 'fixed', 0.2, False, 1, 1, 1, 'average'))

    # combinations.append((['double', 'p2dg'], 'multiply', 0.5, 'max', 'fixed', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'multiply', 0.5, 'max', 'fixed', 0.8, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'multiply', 0.5, 'max', 'fixed', 0.6, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'multiply', 0.5, 'max', 'fixed', 0.4, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg'], 'multiply', 0.5, 'max', 'fixed', 0.2, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 1, True, 0.1, 0.1, 0.8, 'average'))

    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 1, True, 0.2, 0.3, 0.5, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 1, True, 0.5, 0.3, 0.2, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 1, True, 0.8, 0.1, 0.1, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 1, False, 1, 1, 1, 'average'))

    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 0.9, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'float', 0.8, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'fixed', 1, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'fixed', 0.9, True, 0.1, 0.1, 0.8, 'average'))
    # combinations.append((['double', 'p2dg', 'dg2p'], 'multiply', 0.5, 'max', 'fixed', 0.8, True, 0.1, 0.1, 0.8, 'average'))
    
    for HPOVersion in HPOVersions:
        setVersion(HPOVersion)
        for (dataset, taskType) in datasets.items():
            setDataset(dataset, taskType)
            # if (dataset != 'data3' and dataset != 'data11-1' and dataset != 'data11-2'):
            # preprocessAll()
            runAll(combinations)

            # setPreprocess(0.5)
            # setPreCalculate('disease', 'Lin')
            # setCalculate('none')
            # Phen2Disease.main()
            # setCombine(combinations[0])
            # combine.main()
            # evaluate.main()

            # setPreCalculate('integrated', 'IC')
            # if (dataset == 'data5-2' or dataset == 'data10' or dataset == 'data11-1' or dataset == 'data11-2' or dataset == 'data11-3'):
            #     setCalculate('target')
            # else:
            #     setCalculate('none')
            # Phen2Disease.main()
            # setCombine(combinations[1])
            # combine.main()
            # evaluate.main()
        
    IOUtils.showInfo('Batch process finished')


if (__name__ == '__main__'):
    main()
