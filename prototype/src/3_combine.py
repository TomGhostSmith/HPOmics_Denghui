import sys
import os
import math
sys.path.append('.')

import config.config as config
import evaluate.evaluate as evaluate


def calc(disease2Patient, patient2Disease, diseaseIC, patientIC):
    return (disease2Patient + patient2Disease)/(diseaseIC + patientIC) + patient2Disease/patientIC
    # return (disease2Patient + 4*patient2Disease)/(diseaseIC + 4*patientIC) + patient2Disease/patientIC
    # return patient2Disease/patientIC
    # if (diseaseIC != 0):
        # return ((disease2Patient + patient2Disease)/(diseaseIC + patientIC))
    #     return (disease2Patient + patient2Disease)/(diseaseIC + patientIC) + disease2Patient/diseaseIC
    # else:
        # return 0

def main():
    files = os.listdir(config.splitResultPath)
    for file in files:
        with open(f"{config.splitResultPath}/{file}") as fp:
            diseaseScores = fp.readlines()
        diseaseFinalScores = dict()
        for line in diseaseScores:
            if (line.startswith('id')):
                continue
            terms = line.strip().split(',')
            diseaseFinalScores[terms[0]] = calc(float(terms[2]), float(terms[3]), float(terms[4]), float(terms[5]))
        result = dict(sorted(diseaseFinalScores.items(), key=lambda pair : pair[1], reverse=True))
        lines = [f'{key}, , {value}\n' for (key, value) in result.items()]
        lines.insert(0, 'id, name, score\n')
        with open(f"{config.resultPath}/{file}", 'wt') as fp:
            fp.writelines(lines)
    
    evaluate.main()

if (__name__ == '__main__'):
    main()