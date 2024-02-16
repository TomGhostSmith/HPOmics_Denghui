taskType = 'disease'
# taskType = 'gene'
GPUAvailable = False

# project paths
projectPath = "."
splitResultPath = f"{projectPath}/splitResult"
resultPath = f"{projectPath}/result"
dataPath = f"{projectPath}/data"
patientPath = f"{projectPath}/patient"
standardResultPath = f"{projectPath}/standardResult"

# HPO version and anontations
# HPOVersion = "20231009"
HPOVersion = "20221005"
HPOTermFilePath = f"{dataPath}/HPO_obo/hp{HPOVersion}.obo"
gene2PhenotypeAnnotationPath = f"{dataPath}/annotation/genes_to_phenotype_{HPOVersion}.txt"
disease2PhenotypeAnnotationPath = f"{dataPath}/annotation/phenotype_{HPOVersion}.hpoa"
# phenotype2GeneAnnotationPath = f"{dataPath}/annotation/phenotype_to_gene_{HPOVersion}.txt"
diseaseSynonymAnnotationPath = f"{dataPath}/synonym/diseaseSynonym.json"

# preprocess files
geneListPath = f"{dataPath}/preprocess/geneList_{HPOVersion}.txt"
diseaseListPath = f"{dataPath}/preprocess/diseaseList_{HPOVersion}.txt"
# HPOListPath = f"{dataPath}/preprocess/HPOList_{HPOVersion}.txt"  # forbid to use HPOList. Use HPO Tree instead for more information on replacement
gene2PhenotypeJsonPath = f"{dataPath}/preprocess/gene2phenotype_{HPOVersion}.json"
disease2PhenotypeJsonPath = f"{dataPath}/preprocess/disease2phenotype_{HPOVersion}.json"
ICFromDiseasePath = f"{dataPath}/preprocess/ICFromDisease_{HPOVersion}.json"
ICFromGenePath = f"{dataPath}/preprocess/ICFromGene_{HPOVersion}.json"
integratedICPath = f"{dataPath}/preprocess/integratedIC_{HPOVersion}.json"
similarityMatrixPath = f"{dataPath}/preprocess/similarity_{HPOVersion}.npz"
diseaseSynonymPath = f"{dataPath}/preprocess/diseaseSynonym.json"

phenoBrainPath = f"{dataPath}/PhenoBrain"
phenoBrainCCRD2ORPHAPath = f"{phenoBrainPath}/ccrd_to_orpha.json"
phenoBrainCCRD2HPOPath = f"{phenoBrainPath}/conpendium_hpo.json"

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