class Patient:
    def __init__(self, fileName, HPOList, info, taskType, totalIC):
        self.fileName = fileName
        self.HPOList = HPOList
        self.info = info
        self.results = None
        self.taskType = taskType
        self.totalIC = totalIC
    
    # output result in lines
    def getResult(self):
        result = list()
        result.append('id, name, score\n')
        if (self.taskType == 'disease'):
            for (disease, score) in self.results.items():
                # result.append(f'{disease.id}, {str(disease.name).replace(",", " ")}, {score}\n')
                result.append(f'{disease.id}, , {score}\n')
        else:
            for (gene, score) in self.results:
                result.append(f'{gene.id}, {str(gene.name).replace(",", " ")}, {score}\n')

        return result