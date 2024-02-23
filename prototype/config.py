import multiprocessing

class Config():
    def __init__(self) -> None:
        # task settings
        self.projectPath = "."
        self.datasetName = f"data3"
        self.taskType = 'disease'       # can be 'disease', 'gene'
        self.ICType = 'disease'         # can be 'disease', 'gene', 'integrated'
        self.similarityMethod = 'Lin'   # can be 'Lin', 'JC', 'IC'
        self.HPOVersion = "20231009"    # can be 20231009, 20221005
        self.autoLoadAnnotation = True # if True, then will load IC, similarity and annotations when init. Use True after preprocess

        # output settings
        self.ignoreWarning = True

        # evaluate settings
        self.focusTop = [1, 3, 5, 10, 20, 50, 100]

        # hardware settings
        self.GPUAvailable = False
        self.CPUCores = multiprocessing.cpu_count()
        self.supportFork = False

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
        # path settings
        self.taskName = f"{self.datasetName}({self.ICType},{self.similarityMethod})-{self.taskType}"
        self.dataPath = f"{self.projectPath}/data"
        self.splitResultPath = f"{self.projectPath}/splitResult/{self.taskName}"

        self.resultCSVPath = f"{self.projectPath}/result/{self.taskName}_Result.csv"
        self.resultPath = f"{self.projectPath}/result/{self.taskName}"

        # patientPath = f"/home/joy/Data/HPOmicsData/data/{datasetName}"
        # standardResultPath = f"/home/joy/Data/HPOmicsData/standardResult/{datasetName}"
        self.patientPath = f"{self.projectPath}/patient/{self.datasetName}"
        self.standardResultPath = f"{self.projectPath}/standardResult/{self.datasetName}"

        # HPO version and anontation settings
        self.HPOTermFilePath = f"{self.dataPath}/HPO_obo/hp{self.HPOVersion}.obo"
        self.gene2PhenotypeAnnotationPath = f"{self.dataPath}/annotation/genes_to_phenotype_{self.HPOVersion}.txt"
        self.disease2PhenotypeAnnotationPath = f"{self.dataPath}/annotation/phenotype_{self.HPOVersion}.hpoa"
        # phenotype2GeneAnnotationPath = f"{dataPath}/annotation/phenotype_to_gene_{HPOVersion}.txt"
        self.diseaseSynonymAnnotationPath = f"{self.dataPath}/synonym/diseaseSynonym.json"

        # preprocess files settings
        self.geneListPath = f"{self.dataPath}/preprocess/geneList_{self.HPOVersion}.txt"
        self.diseaseListPath = f"{self.dataPath}/preprocess/diseaseList_{self.HPOVersion}.txt"
        self.gene2PhenotypeJsonPath = f"{self.dataPath}/preprocess/gene2phenotype_{self.HPOVersion}.json"
        self.disease2PhenotypeJsonPath = f"{self.dataPath}/preprocess/disease2phenotype_{self.HPOVersion}.json"
        self.ICFromDiseasePath = f"{self.dataPath}/preprocess/ICFromDisease_{self.HPOVersion}.json"
        self.ICFromGenePath = f"{self.dataPath}/preprocess/ICFromGene_{self.HPOVersion}.json"
        self.integratedICPath = f"{self.dataPath}/preprocess/integratedIC_{self.HPOVersion}.json"
        self.diseaseSynonymPath = f"{self.dataPath}/preprocess/diseaseSynonym.json"
        self.MICAMatirxPath = f"{self.dataPath}/preprocess/MICAMatrix_{self.HPOVersion}_{self.ICType}.npz"

        # other settings
        self.phenoBrainPath = f"{self.dataPath}/PhenoBrain"
        self.phenoBrainCCRD2ORPHAPath = f"{self.phenoBrainPath}/ccrd_to_orpha.json"
        self.phenoBrainCCRD2HPOPath = f"{self.phenoBrainPath}/conpendium_hpo.json"

        self.analysisPath = f"{self.projectPath}/analysis"

        
config = Config()