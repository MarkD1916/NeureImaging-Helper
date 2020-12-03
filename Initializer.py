from Data import Searcher
from Parser import Parser
from DBUtils import Utils
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
#"D:/N_img"
class InitializerDB():

    def __init__(self,mainDir):
        self.search = Searcher(mainDir=mainDir)
        self.parser = Parser()
        self.experiments = []
        self.drugs = []
        self.cords = []
        self.boundary = []
        self.rat = {}

    def getExperiments(self):
        metaData = {"ID":[],"path":[],"name":[],"date":[]}
        date = self.search.searchDateData()
        path,name = self.search.searchExpPath()
        metaData["path"] = path
        metaData["name"] = name
        metaData["date"] = date
        metaData["ID"] = [x for x in range(1,len(path)+1)]
        self.experiments = metaData
        self.experiments = np.transpose(list(self.experiments.values()))



    def makeRowsForTable(self,data, keys):
        columns = [[] for i in range(len(keys)+1)]
        for expID in data.keys():
            for k,numCol in zip(keys,range(1,len(columns)+1)):
                for row in data[expID][k]:
                    columns[numCol].append(row)
                    if numCol == 1:
                        columns[0].append(expID)

        rows = np.transpose(columns)
        return rows

    def getRoiLLMData(self):
        filesPath = self.search.searchRoiLLMFile()
        roiLLMData = self.parser.parseRoiLlmFile(filesPath)
        drugsTableData=self.makeRowsForTable(roiLLMData,['Drug','Valve'])
        boundaryTableData = self.makeRowsForTable(roiLLMData,['Rostral','Caudal','Medial','Lateral'])
        cordsTableData = self.makeRowsForTable(roiLLMData, ['xValue', 'yValue'])
        self.drugs = drugsTableData
        self.cords = cordsTableData
        self.boundary = boundaryTableData
        print (self.experiments)

    def setDataInDB(self):

        return


Init = InitializerDB("/mnt/data/N_img")
Init.getExperiments()
Init.getRoiLLMData()