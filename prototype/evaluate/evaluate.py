import sys
import os
sys.path.append(".")

import config.config as config
import utils.IOUtils as IOUtils

def main():
    files = os.listdir(config.standardResultPath)
    result = dict()

    MRR = 0

    tops = dict()
    tops[1] = 0
    tops[5] = 0
    tops[10] = 0
    tops[20] = 0
    tops[50] = 0
    tops[100] = 0

    totalCount = len(files)
    for file in files:
        with open(f"{config.standardResultPath}/{file}") as fp:
            standardResult = fp.readline().strip()
            # print(f"standard result for {file}: {standardResult}")
        with open(f"{config.resultPath}/{file}.csv") as fp:
            index = -1
            line = fp.readline().strip()
            found = False
            while (line):
                index += 1
                if (line.split(',')[0] == standardResult):
                    result[file] = index
                    found = True
                    break
                line = fp.readline().strip()
            MRR += 1/index
            for threshold in tops.keys():
                if (index <= threshold):
                    tops[threshold] += 1
            
            if (not found):
                result[file] = 'NIL'

    print("rank\tnum\tratio")
    for (threshold, count) in tops.items():
        print(f"top{threshold}\t{count}\t{(100*count/totalCount):.2f}%")
    print(f"\nMRR {(100*MRR/totalCount):.2f}")

    # print(f"top1\ttop3\ttop5\ttop10")
    # print(f"{top1} \t{top3} \t{top5}% \t{top10} ")
    # print(f"{(100*top1/totalCount):.2f}%\t{(100*top3/totalCount):.2f}%\t{(100*top5/totalCount):.2f}%\t{(100*top10/totalCount):.2f}%")

    res = list()
    res.append("name, rank\n")
    for (name, index) in result.items():
        res.append(f"{name}, {index}\n")

    with open("./result.csv", 'wt', encoding='utf-8') as fp:
        fp.writelines(res)

if (__name__ == '__main__'):
    main()