taskType = 'disease'
# taskType = 'gene'
GPUAvailable = False

# project paths
projectPath = "."
testsetName = "data3-Integrated-IC"
splitResultPath = f"{projectPath}/splitResult/{testsetName}"
resultPath = f"{projectPath}/result/{testsetName}"
# resultPath = f"{projectPath}/result/PhenoProResult/{testsetName}"
resultCSVPath = f"{projectPath}/result/{testsetName}Result.csv"
# resultCSVPath = f"{projectPath}/result/PhenoProResult/{testsetName}Result.csv"
dataPath = f"{projectPath}/data"
patientPath = f"{projectPath}/patient/{testsetName}"
# standardResultPath = f"{projectPath}/standardResult/{testsetName}"
standardResultPath = f"{projectPath}/standardResult/data3"

# HPO version and anontations
HPOVersion = "20231009"
# HPOVersion = "20221005"
HPOTermFilePath = f"{dataPath}/HPO_obo/hp{HPOVersion}.obo"
gene2PhenotypeAnnotationPath = f"{dataPath}/annotation/genes_to_phenotype_{HPOVersion}.txt"
disease2PhenotypeAnnotationPath = f"{dataPath}/annotation/phenotype_{HPOVersion}.hpoa"
# phenotype2GeneAnnotationPath = f"{dataPath}/annotation/phenotype_to_gene_{HPOVersion}.txt"
diseaseSynonymAnnotationPath = f"{dataPath}/synonym/diseaseSynonym.json"

# preprocess files
geneListPath = f"{dataPath}/preprocess/geneList_{HPOVersion}.txt"
diseaseListPath = f"{dataPath}/preprocess/diseaseList_{HPOVersion}.txt"
gene2PhenotypeJsonPath = f"{dataPath}/preprocess/gene2phenotype_{HPOVersion}.json"
disease2PhenotypeJsonPath = f"{dataPath}/preprocess/disease2phenotype_{HPOVersion}.json"
ICFromDiseasePath = f"{dataPath}/preprocess/ICFromDisease_{HPOVersion}.json"
ICFromGenePath = f"{dataPath}/preprocess/ICFromGene_{HPOVersion}.json"
integratedICPath = f"{dataPath}/preprocess/integratedIC_{HPOVersion}.json"
diseaseSynonymPath = f"{dataPath}/preprocess/diseaseSynonym.json"
# MICAMatirxPath = f"{dataPath}/preprocess/MICAMatrix_{HPOVersion}.npz"
# MICAMatirxPath = f"{dataPath}/preprocess/MICAMatrix_{HPOVersion}_Gene.npz"
MICAMatirxPath = f"{dataPath}/preprocess/MICAMatrix_{HPOVersion}_Integrated.npz"

phenoBrainPath = f"{dataPath}/PhenoBrain"
phenoBrainCCRD2ORPHAPath = f"{phenoBrainPath}/ccrd_to_orpha.json"
phenoBrainCCRD2HPOPath = f"{phenoBrainPath}/conpendium_hpo.json"

analysisPath = f"{projectPath}/analysis"

# special HPO terms
HPORoot = 'HP:0000001'
specialHPO = {
    'HP:0000005': 'Mode of inheritance',
    'HP:0000118': 'Phenotypic abnormality',
    'HP:0012823': 'Clinical modifier',
    'HP:0032223': 'Blood group',
    'HP:0032443': 'Past medical history',
    'HP:0040279': 'Frequency'
}

HPOClasses = {
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

# focusDisease = {'OMIM:612838', 'OMIM:611363', 'OMIM:201475'}
# focusDisease = {'OMIM:176270', 'OMIM:615873'}
focusDisease = {}