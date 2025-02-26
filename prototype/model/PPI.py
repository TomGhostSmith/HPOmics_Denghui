import os
import sys
import json
import numpy
import networkx
from tqdm import tqdm
import multiprocessing
sys.path.append('.')

from config import config
from utils import IOUtils
from utils import ParallelUtils

class PPI():
    def __init__(self) -> None:
        self.network = networkx.Graph()  # this is a undirected graph
        self.geneLink = dict()
        # self.multiprocessingManager = multiprocessing.Manager()
        # self.cachedShortestPath = self.multiprocessingManager.dict()
        self.cachedShortestPath = None
        self.averageWeight = None
        self.maxWeight = 0
        self.nodeIndexMap = dict()
        self.shortestPathMatrix = None

    def _getWeight(self, weight):
        return self.averageWeight/weight


    def loadPPI(self):
        totalWeight = 0
        weightCount = 0
        with open(config.geneLinkPath) as fp:
            self.geneLink = json.load(fp)
            for startGene, relatedGenes in self.geneLink.items():
                for endGene, weight in relatedGenes.items():
                    if (weight > self.maxWeight):
                        self.maxWeight = weight
                    totalWeight += weight
                    weightCount += 1
            self.averageWeight = totalWeight / weightCount

            for startGene, relatedGenes in self.geneLink.items():
                for endGene, weight in relatedGenes.items():
                    w = self._getWeight(weight)
                    self.network.add_edge(startGene, endGene, weight=w)
                    # self.network.add_edge(startGene, endGene, weight=weight)
                    # self.network.add_edge(startGene, endGene)
        IOUtils.showInfo("PPI loaded")

    def getShortestPath(self, source, target):
        sourceID = self.nodeIndexMap.get(source)
        targetID = self.nodeIndexMap.get(target)
        if (sourceID != None and targetID != None):
            length = self.cachedShortestPath[sourceID, targetID]
        else:
            length = float('inf')
        path = None
        return length, path
    
        # length = None
        # paths = self.cachedShortestPath.get(source)
        # if (paths != None):
        #     length = paths.get(target)
        
        # if (length == None):
        #     length = float('inf')
        # path = None

        # return length, path
    
        
    def calculateAllShortestPathFromSource(self, source):
        return source, networkx.single_source_dijkstra_path_length(self.network, source)
    
    def cacheAll(self):
        sourceNodes = list(self.network.nodes)
        shortestPathDicts = ParallelUtils.parallelWithResult(sourceNodes, self.calculateAllShortestPathFromSource, unpack=False)
        for source, lengthDict in shortestPathDicts:
            self.cachedShortestPath[source] = lengthDict
    
    def saveCache(self):
        with open(config.PPIShortestPathCache, 'wt') as fp:
            json.dump(self.cachedShortestPath, fp, indent=2)

    def convertdict2Matrix(self):
        if (os.path.exists(config.oldPPIShortestPathCache)):
            with open(config.oldPPIShortestPathCache) as fp:
                self.cachedShortestPath = json.load(fp)
        IOUtils.showInfo('Loaded cached shortest path dict')
        nodes = list(self.network.nodes)
        for idx, node in enumerate(nodes):
            self.nodeIndexMap[node] = idx
        with open(config.PPIIndexMap, 'wt') as fp:
            json.dump(self.nodeIndexMap, fp, indent=2)
        self.shortestPathMatrix = numpy.zeros((len(nodes), len(nodes)))
        self.shortestPathMatrix -= 1   # all diconnected are -1

        progress = tqdm(total=len(nodes))
        for source, d in self.cachedShortestPath.items():
            for terminal, distance in d.items():
                sourceID = self.nodeIndexMap[source]
                terminalID = self.nodeIndexMap[terminal]
                self.shortestPathMatrix[sourceID][terminalID] = distance
            progress.update(1)

        progress.close()
        
        numpy.savez_compressed(config.PPIShortestPathCache, shortestPathMatrix=self.shortestPathMatrix)
        IOUtils.showInfo('Done')
        

        
        

    def loadCache(self):
        if (len(self.geneLink) != 0):
            return
        self.loadPPI()
        if (os.path.exists(config.PPIShortestPathCache)):
            # with open(config.PPIShortestPathCache) as fp:
            #     self.cachedShortestPath = json.load(fp)
            self.cachedShortestPath = numpy.load(config.PPIShortestPathCache)['shortestPathMatrix']
            with open(config.PPIIndexMap) as fp:
                self.nodeIndexMap = json.load(fp)
        else:
            self.cacheAll()
            self.saveCache()
    
    def clearCache(self):
        # self.cachedShortestPath = self.multiprocessingManager.dict()
        self.cachedShortestPath = None
    


ppi = PPI()
ppi.loadPPI()
ppi.convertdict2Matrix()
# ppi.getShortestPath("GCDH", "SMN2")