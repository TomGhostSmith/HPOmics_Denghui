import multiprocessing

class Config():
    def __init__(self) -> None:
        # task settings
        self.projectPath = "/home/joy/Software/HPOmics/prototype"

        # version settings:
        self.HPOVersion = "20231009"    # can be '20231009' or '20221005'

        # dataset settings
        self.datasetName = f"data3"
        self.taskType = 'disease'       # can be 'disease' or 'gene'

        # dataset specific settings
        self.localProportion = 0.5

        # task settings:
        self.ICType = 'disease'         # can be 'disease' or 'gene' or 'integrated' or 'phankDisease' or 'phrankGene' or 'phrankIntegrated' or 'diseaseIntegrated' or 'geneIntegrated' or 'integratedIntegrated' or 'local' or 'localIntegrated'
        self.similarityMethod = 'Lin'   # can be 'Lin' or 'JC' or 'IC'
        # self.autoLoadAnnotation = False # if True, then will load IC, similarity and annotations when init. Use True after preprocess
        # self.useSynonym = False

        # calculate settings
        self.useAncestor = False

        # combine settings
        self.scoreCombineMethods = ['double', 'p2dg'] # list of 'double', 'p2dg', 'dg2p'
        self.CADDMethod = 'multiply' # can be 'multiply', 'none'
        self.CADDMinRatio = 0.5  # if no variant on this gene exists, final score should multiply with this minimum ratio

        # combine disease2gene setting
        self.disease2GeneMethod = 'max'  # 'average' or 'max'
        self.disease2GeneProportionMethod = 'float'  # 'fixed' (use max proportion) or 'float' (use (1 - 1/x) * max proportion)
        self.maxDiseaseProportion = 1

        # combine gene2disease setting
        self.gene2DiseaseMethod = 'max'
        self.gene2DiseaseProportionMethod = 'float'
        self.maxGeneProportion = 1

        # PPI method settings
        self.usePPI = True
        self.selfProportion = 0.1
        self.directProportion = 0.2
        self.indirectProportion = 0.7
        self.directScoreMethod = 'average'  # average or max

        # output settings
        self.ignoreWarning = True
        self.ignoreSmallProcess = True

        # evaluate settings
        self.focusTop = [1, 3, 5, 10, 20, 50, 100]

        # hardware settings
        # note: in cupy, matrix division has some problem and will lead to NaN or inf
        self.GPUAvailable = False   # should be False
        self.CPUCores = multiprocessing.cpu_count()
        # self.CPUCores = 1
        self.supportFork = True
        self.useForkWhenCADD = False

        # special HPO terms settings
        self.HPORoot = 'HP:0000001'
        self.specialHPO = {
            'HP:0000005': 'Mode of inheritance',
            'HP:0000118': 'Phenotypic abnormality',
            'HP:0012823': 'Clinical modifier',
            'HP:0032223': 'Blood group',
            'HP:0032443': 'Past medical history',
            'HP:0040279': 'Frequency'
        }

        self.HPOClasses = {
            'HP:0000119': 'genitourinary system abnormality',
            'HP:0000152': 'head and neck abnormality',
            'HP:0000478': 'eye abnormality',
            'HP:0000598': 'ear abnormality',
            'HP:0000707': 'nervous system abnormality',
            'HP:0000769': 'breast abnormality',
            'HP:0000818': 'endocrine system abnormality',
            'HP:0001197': 'abnormality of prenatal development or birth',
            'HP:0001507': 'growth abnormality',
            'HP:0001574': 'integument abnormality',
            'HP:0001608': 'voice abnormality',
            'HP:0001626': 'cardiovascular system abnormality',
            'HP:0001871': 'blood abnormality',
            'HP:0001939': 'metabolism/homeostasis abnormality',
            'HP:0002086': 'respiratory system abnormality',
            'HP:0002664': 'neoplasm',
            'HP:0002715': 'immune system abnormality',
            'HP:0025031': 'digestive system abnormality',
            'HP:0025142': 'constitutional symptom',
            'HP:0025354': 'abnormal cellular phenotype',
            'HP:0033127': 'musculoskeletal system abnormality',
            'HP:0040064': 'limbs abnormality',
            'HP:0045027': 'thoracic cavity abnormality'
        }

        # for debug: set focus disease, and output related info when processing
        self.focusDisease = {}
        self.resetPath()
    
    def resetPath(self):
        # set appendix
        # changes need to use different dataset/target: modify datasetParams
        # changes need to re-extractAnnotation: modify versionParams
        # changes need to re-preprocess: modify dsSpecificParams. e.g. localIC proportion
        # changes need to re-precalcualte: modify taskParams      e.g. ICType
        # changes need to re-calculate: modify calculateParams
        # changes need to re-combine: modify combineParams

        self.versionParams = f'_HPO={self.HPOVersion}'
        self.datasetParams = f'{self.datasetName}_target={self.taskType}'    # start with datasetName. e.g. data10_target=gene_...
        self.dsSpecificParams = f'_local={self.localProportion}'
        if (self.ICType.startswith('local')):
            self.localICParams = f'-{self.datasetName}-{self.localProportion}'
            self.ICName = f'{self.ICType}{self.localICParams}'
        else:
            self.localICParams = ''
            self.ICName = self.ICType
        self.taskParams = f'{self.versionParams}_IC={self.ICName}_similarity={self.similarityMethod}'
        self.calculateParams = f'{self.datasetParams}{self.taskParams}_ancestor={self.useAncestor}'
        if (self.taskType == 'gene'):
            self.combineParams = f'{self.calculateParams}_combine={"+".join(self.scoreCombineMethods)}_CADD={self.CADDMethod};{self.CADDMinRatio}_d2g={self.disease2GeneMethod};{self.disease2GeneProportionMethod};{self.maxDiseaseProportion}_ppi={self.usePPI};{self.selfProportion};{self.directProportion};{self.indirectProportion};{self.directScoreMethod}'
        else:
            self.combineParams = f'{self.calculateParams}_combine={"+".join(self.scoreCombineMethods)}_CADD={self.CADDMethod};{self.CADDMinRatio}_g2d={self.gene2DiseaseMethod};{self.gene2DiseaseProportionMethod};{self.maxGeneProportion}_ppi={self.usePPI};{self.selfProportion};{self.directProportion};{self.indirectProportion};{self.directScoreMethod}'

        # if (self.ICType.startswith('local')):
            # self.ICType = f'{self.ICType}-{self.datasetName}-{self.taskType}'


        # path settings
        self.dataPath = f"{self.projectPath}/data"
        self.splitResultPath = f"{self.projectPath}/splitResult/{self.calculateParams}"

        self.resultCSVPath = f"{self.projectPath}/result/{self.combineParams}_Result.csv"
        self.resultPath = f"{self.projectPath}/result/{self.combineParams}"

        self.patientPath = f"/home/joy/Data/HPOmicsData/data/{self.datasetName}"
        self.standardResultPath = f"/home/joy/Data/HPOmicsData/standardResult/{self.datasetName}"
        # self.patientPath = f"{self.projectPath}/patient/{self.datasetName}"
        # self.standardResultPath = f"{self.projectPath}/standardResult/{self.datasetName}"

        # HPO version and anontation settings
        self.HPOTermFilePath = f"{self.dataPath}/HPO_obo/hp{self.HPOVersion}.obo"
        self.gene2PhenotypeAnnotationPath = f"{self.dataPath}/annotation/genes_to_phenotype_{self.HPOVersion}.txt"
        self.disease2PhenotypeAnnotationPath = f"{self.dataPath}/annotation/phenotype_{self.HPOVersion}.hpoa"
        # phenotype2GeneAnnotationPath = f"{dataPath}/annotation/phenotype_to_gene_{HPOVersion}.txt"
        self.diseaseSynonymAnnotationPath = f"{self.dataPath}/synonym/diseaseSynonym.json"
        self.gene2DiseaseAnnotationPath = f"{self.dataPath}/annotation/genes_to_disease_{self.HPOVersion}.txt"

        # gene-protein link data
        self.gene2ProteinMapAnnotationPath = f"{self.dataPath}/link/gene_protein_map.gz"  # this file is from biomart
        self.proteinProteinInteractionAnnotationPath = f"{self.dataPath}/link/protein_link.gz"  # this is ppi data, which is from STRING database


        # extractAnnotation files settings
        self.geneListPath = f"{self.dataPath}/preprocess/geneList{self.versionParams}.txt"
        self.diseaseListPath = f"{self.dataPath}/preprocess/diseaseList{self.versionParams}.txt"
        self.gene2PhenotypeJsonPath = f"{self.dataPath}/preprocess/gene2phenotype{self.versionParams}.json"
        self.disease2PhenotypeJsonPath = f"{self.dataPath}/preprocess/disease2phenotype{self.versionParams}.json"
        self.disease2GeneJsonPath = f"{self.dataPath}/preprocess/disease2Gene{self.versionParams}.json"
        self.gene2DiseaseJsonPath = f"{self.dataPath}/preprocess/gene2Disease{self.versionParams}.json"
        self.diseaseSynonymPath = f"{self.dataPath}/preprocess/diseaseSynonym{self.versionParams}.json"
        self.geneLinkPath = f"{self.dataPath}/preprocess/geneLink{self.versionParams}.json"

        # extractAnnotation IC files settings
        self.diseaseICPath = f"{self.dataPath}/preprocess/diseaseIC{self.versionParams}.json"
        self.geneICPath = f"{self.dataPath}/preprocess/geneIC{self.versionParams}.json"
        self.integratedICPath = f"{self.dataPath}/preprocess/integratedIC{self.versionParams}.json"
        self.phrankDiseaseICPath = f"{self.dataPath}/preprocess/phrankDiseaseIC{self.versionParams}.json"
        self.phrankGeneICPath = f"{self.dataPath}/preprocess/phrankGeneIC{self.versionParams}.json"
        self.phrankIntegratedICPath = f"{self.dataPath}/preprocess/phrankIntegratedIC{self.versionParams}.json"
        self.diseaseIntegratedICPath = f"{self.dataPath}/preprocess/diseaseIntegratedIC{self.versionParams}.json"
        self.geneIntegratedICPath = f"{self.dataPath}/preprocess/geneIntegratedIC{self.versionParams}.json"
        self.integratedIntegratedICPath = f"{self.dataPath}/preprocess/integratedIntegratedIC{self.versionParams}.json"
        self.localICPath = f"{self.dataPath}/preprocess/local{self.localICParams}IC{self.versionParams}.json"
        self.localIntegratedPath = f"{self.dataPath}/preprocess/localIntegrated{self.localICParams}IC{self.versionParams}.json"
        self.currentUseICPath = f"{self.dataPath}/preprocess/{self.ICName}IC{self.versionParams}.json"

        # preprocess files settings
        self.MICAMatirxPath = f"{self.dataPath}/preprocess/MICAMatrix{self.taskParams}.npz"

        # other settings
        self.phenoBrainPath = f"{self.dataPath}/PhenoBrain"
        self.phenoBrainCCRD2ORPHAPath = f"{self.phenoBrainPath}/ccrd_to_orpha.json"
        self.phenoBrainCCRD2HPOPath = f"{self.phenoBrainPath}/conpendium_hpo.json"

        self.analysisPath = f"{self.projectPath}/analysis"

        # genotype CADD settings
        self.CADDPath = "/home/joy/Software/CADD/CADD-scripts/CADD.sh"
        self.CADDTempFolder = f"{self.projectPath}/temp"
        # self.CADDInputFolder = f"{self.projectPath}/genotype/input"
        self.CADDInputFolder = f"/home/joy/Data/HPOmicsData/data/data3vcf2"
        self.CADDOutputFolder = f"{self.projectPath}/CADDResult"

        
config = Config()
