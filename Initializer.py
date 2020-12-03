from Data import Searcher
from Parser import Parser
from DBUtils import Utils
import sys
import numpy as np
from  Models.Model import *
np.set_printoptions(threshold=sys.maxsize)
#"D:/N_img"
class InitializerDB():

    def __init__(self,mainDir):
        self.search = Searcher(mainDir=mainDir)
        self.parser = Parser()
        self.utils = Utils()
        self.experiments = []
        self.drugs = []
        self.cords = []
        self.boundary = []
        self.models = {"Drugs":Drugs()}



    def getExperiments(self):
        metaData = {"path":[],"name":[],"date":[]}
        date = self.search.searchDateData()
        path,name = self.search.searchExpPath()
        metaData["path"] = path
        metaData["name"] = name
        metaData["date"] = date
        self.experiments = metaData
        self.experiments = np.transpose(list(self.experiments.values()))

    def makeRowsForTable(self,data, keys,model):
        columns = [[] for i in range(len(keys)+1)]

        for expID in data.keys():
            for k,numCol in zip(keys,range(1,len(columns)+1)):

                for row in data[expID][k]:
                    setattr(self.models[model], k,row)
                    print(getattr(self.models[model], k))
                    columns[numCol].append(row)
                    if numCol == 1:
                        columns[0].append(expID)

        rows = np.transpose(columns)
        return rows

    def getRoiLLMData(self):
        filesPath = self.search.searchRoiLLMFile()
        roiLLMData = self.parser.parseRoiLlmFile(filesPath)
        drugsTableData=self.makeRowsForTable(roiLLMData,['drugName','Valve'],"Drugs")
        boundaryTableData = self.makeRowsForTable(roiLLMData,['Rostral','Caudal','Medial','Lateral'])
        cordsTableData = self.makeRowsForTable(roiLLMData, ['xValue', 'yValue'])
        self.drugs = drugsTableData
        self.cords = cordsTableData
        self.boundary = boundaryTableData
        self.dataForInsert = {"Experiments":self.experiments,"Boundary":self.boundary,"Drugs":self.drugs,
                              "Cords":self.cords}

    def createTables(self):
        self.utils.createTable("Experiments",
                      "ID INTEGER PRIMARY KEY , Path text NOT NULL, Name text NOT NULL, Date text NOT NULL")

        self.utils.createTable("Boundary",
                      "ID INTEGER PRIMARY KEY ,\
                      Rostral text NOT NULL,\
                      Caudal text NOT NULL, \
                      Medial text NOT NULL, \
                      Lateral text NOT NULL,\
                      ExpId INTEGER NOT NULL,FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")

        self.utils.createTable("Drugs",
                     "ID INTEGER PRIMARY KEY ,\
                      ExpId INTEGER NOT NULL,\
                      DrugName text NOT NULL,\
                      Valve INTEGER,\
                      FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")

        self.utils.createTable("Cords",
                     "ID INTEGER PRIMARY KEY ,\
                      xValue REAL,\
                      yValue REAL,\
                      Region Text,\
                      ExpId INTEGER NOT NULL,\
                      FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
        return
    def insertDataInDB(self):

        for name in self.dataForInsert.keys():
            #print(self.dataForInsert[name])
            #if len(self.utils.selectAllFromTable(name))==0:
            for exp in self.dataForInsert[name]:
                exp = np.insert(exp,0,None)
                #print (exp)
                self.utils.insertDataInTable(name, exp)
            self.utils.selectAllFromTable(name)


        return


Init = InitializerDB("/mnt/data/N_img")
Init.getExperiments()
Init.getRoiLLMData()
#Init.createTables()
#Init.insertDataInDB()