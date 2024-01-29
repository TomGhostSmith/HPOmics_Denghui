# taskType = 'disease'
taskType = 'gene'

# project paths
projectPath = "."
resultPath = f"{projectPath}/result"
dataPath = f"{projectPath}/data"

# HPO version and anontations
HPOVersion = "20231009"
HPOTermFilePath = f"{dataPath}/HPO_obo/hp{HPOVersion}.obo"
gene2PhenotypeAnnotationPath = f"{dataPath}/annotation/genes_to_phenotype_{HPOVersion}.txt"
disease2PhenotypeAnnotationPath = f"{dataPath}/annotation/phenotype_{HPOVersion}.hpoa"
# phenotype2GeneAnnotationPath = f"{dataPath}/annotation/phenotype_to_gene_{HPOVersion}.txt"

# preprocess files
geneListPath = f"{dataPath}/preprocess/geneList_{HPOVersion}.txt"
diseaseListPath = f"{dataPath}/preprocess/diseaseList_{HPOVersion}.txt"
# HPOListPath = f"{dataPath}/preprocess/HPOList_{HPOVersion}.txt"  # forbid to use HPOList. Use HPO Tree instead for more information on replacement
gene2PhenotypeJsonPath = f"{dataPath}/preprocess/gene2phenotype_{HPOVersion}.json"
disease2PhenotypeJsonPath = f"{dataPath}/preprocess/disease2phenotype_{HPOVersion}.json"
ICFromDiseasePath = f"{dataPath}/preprocess/ICFromDisease_{HPOVersion}.json"
ICFromGenePath = f"{dataPath}/preprocess/ICFromGene_{HPOVersion}.json"
integratedICPath = f"{dataPath}/preprocess/integratedIC_{HPOVersion}.json"