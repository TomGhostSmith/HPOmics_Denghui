import json
import sys
import importlib
sys.path.append('.')

from config import config

extractAnnotation = importlib.import_module('src.1_extractAnnotation')
preprocess = importlib.import_module('src.2_preprocess')
precalculate = importlib.import_module('src.3_precalculate')
Phen2Disease = importlib.import_module('src.4_Phen2Disease')
combine = importlib.import_module('src.5_combine')
evaluate = importlib.import_module('src.6_evaluate')

def main():
    taskName = sys.argv[1]
    # taskName = '1710422544812'
    taskPath = f'/home/joy/GhoST/HPOmics/Tasks/{taskName}'

    taskTypes = ['disease', 'gene']
    ICMethods = ['disease', 'gene', 'integrated', 'local']
    similarities = ['Lin', 'JC', 'IC']
    useAncestors = ['none', 'target']
    convertProportionMethods = ['none', 'fixed', 'float']  # note: none is not a valid choice in config
    CADDMethods = ['none', 'fixed']
    


    with open(file=f'{taskPath}/settings.json', mode='rt', encoding='utf-8') as fp:
        settings = json.load(fp)
    
    config.taskType = taskTypes[settings['taskType'] - 1]
    config.CADDMAxProportion = settings['caddMaxProportion']
    config.CADDMethod = CADDMethods[settings['caddMethod'] - 1]

    if (config.taskType == 'disease'):
        config.gene2DiseaseMethod = 'max'
        config.gene2DiseaseProportionMethod = convertProportionMethods[settings['convertProportionMethod'] - 1]
        config.maxGeneProportion = settings['convertMaxProportion']
    elif (config.taskType == 'gene'):
        config.disease2GeneMethod = 'max'
        config.disease2GeneProportionMethod = convertProportionMethods[settings['convertProportionMethod'] - 1]
        config.maxDiseaseProportion = settings['convertMaxProportion']
    
    config.ICType = ICMethods[settings['icMethod'] - 1]
    config.usePPI = settings['usePPI']
    if (config.usePPI):
        config.selfProportion = settings['ppiSelfProportion']
        config.directProportion = settings['ppiDirectProportion']
        config.indirectProportion = settings['ppiIndirectProportion']
    else:
        config.selfProportion = 1
        config.directProportion = 0
        config.indirectProportion = 0
    
    config.similarityMethod = similarities[settings['similarity'] - 1]
    config.useAncestor = useAncestors[settings['useAncestor'] - 1]

    config.datasetName = 'HPOmics'


    config.resetPath()
    config.inputType = 'json'
    config.patientPath = f'{taskPath}/patient'
    config.CADDInputFolder = f'{taskPath}/VCF'
    config.splitResultPath = f'{taskPath}/splitResult'
    config.resultPath = f'{taskPath}/finalResult'
    config.CADDOutputFolder = f'{taskPath}/CADD'
    config.HPOmcisOutput = True

    if (ICMethods == 'local'):
        config.localProportion = 0.5
        preprocess.main()
        precalculate.main()
    Phen2Disease.main()
    combine.main()

    


if (__name__ == '__main__'):
    main()