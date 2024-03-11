# run it when task param modified
import sys
import json
import math
import numpy
import gzip
import os
from scipy.sparse import csr_matrix
# import cupy
sys.path.append(".")

from config import config
import utils.IOUtils as IOUtils
from utils.HPOUtils import HPOUtils
from model.HPO import HPO
from model.HPO import HPOTree
from model.Disease import Disease
from model.Gene import Gene

def calcMICAMatrix():
    ancestorIndexsList = [node.ancestorIndexs for node in HPOUtils.HPOTree.nodes]

    IOUtils.showInfo("Calculating MICA Matrix")
    HPOCount = len(HPOUtils.HPOTree.getValidHPOTermList())
    ICList = HPOUtils.HPOTree.ICList
    
    MICAMatrix = numpy.zeros([HPOCount, HPOCount], dtype=numpy.float32)

    # calculate MICA Matrix, only lower triangle
    for index1 in range(0, HPOCount):
        node1AncestorIndexs = ancestorIndexsList[index1]
        for index2 in range (0, index1):
            commonAncestorIndexs = node1AncestorIndexs & ancestorIndexsList[index2]
            MICAMatrix[index1, index2] = max([ICList[ancestorIndex] for ancestorIndex in commonAncestorIndexs])
    IOUtils.showInfo("MICA Matrix calc finished, saving result")
    numpy.savez_compressed(config.MICAMatirxPath, MICAMatrix=MICAMatrix)
    IOUtils.showInfo("MICA Matrix saved")

def main():
    IOUtils.init(3)
    HPOUtils.loadIC()
    calcMICAMatrix()


if (__name__ == '__main__'):
    main()