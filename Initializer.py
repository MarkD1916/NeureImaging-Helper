from Data import Searcher
from Parser import Parser
from DBUtils import Utils
import sys
import numpy as np
from  Models.Model import *
import os
np.set_printoptions(threshold=sys.maxsize)
#"D:/N_img"
class InitializerDB():

    def __init__(self,mainDir,dbName):
        self.search = Searcher(mainDir=mainDir)
        self.parser = Parser()
        self.utils = Utils(os.path.join(mainDir, dbName+'.db'))
        self.experiments = []
        self.drugs = []
        self.cords = []
        self.boundary = []

    def getExperiments(self):
        expList = []
        metaData = {"path":[],"name":[],"date":[]}
        date = self.search.searchDateData()
        path,name = self.search.searchExpPath()
        metaData["path"] = path
        metaData["name"] = name
        metaData["date"] = date
        self.experiments = metaData
        self.experiments = np.transpose(list(self.experiments.values()))
        objs = [Experiments() for i in range(len(self.experiments))]
        for r,m in zip(self.experiments,objs):
            expList.append(self.make_model(m,['path','name','date'],r,mode='notFromFile'))
        self.experiments = expList

    def makeRowsForTable(self,data, keys,model):
        columns = [[] for i in range(len(keys)+1)]
        for expID in data.keys():
            for k,numCol in zip(keys,range(1,len(columns)+1)):
                for row in data[expID][k]:
                    columns[numCol].append(row)
                    if numCol == 1:
                        columns[0].append(expID)
        rows = np.transpose(columns)
        modelList = []
        objs = [model() for i in range(len(rows))]
        for r,m in zip(rows,objs):
            model = self.make_model(m,keys,r)
            modelList.append(model)
        return modelList

    def make_model(self, model, atr, value,mode='fromFile'):
        if mode=='fromFile':
            atr = np.insert(atr,0,'expID')
        for a,v in zip(atr,value):
            if a=='expID':
                v=int(v)
            setattr(model,a,v)
        return model

    def getRoiLLMData(self):
        filesPath = self.search.searchRoiLLMFile()
        roiLLMData = self.parser.parseRoiLlmFile(filesPath)
        drugsTableData=self.makeRowsForTable(roiLLMData,['drugName','valve'],model=Drugs)
        boundaryTableData = self.makeRowsForTable(roiLLMData,['rostral','caudal','medial','lateral'],model=Boundary)
        cordsTableData = self.makeRowsForTable(roiLLMData, ['xValue', 'yValue'],model=Cords)
        # сущности БД на данном этапе являются списком моделей с нужными атрибутами
        self.drugs = drugsTableData
        self.cords = cordsTableData
        self.boundary = boundaryTableData
        self.dataForInsert = {"Experiments": self.experiments, "Boundary": self.boundary, "Drugs": self.drugs,
                              "Cords": self.cords}

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
                      ExpId INTEGER NOT NULL,\
                      FOREIGN KEY (ExpId) REFERENCES Experiments(ID)")
        return

    def insertDataInDB(self):
        for name in self.dataForInsert.keys():
            for exp in self.dataForInsert[name]:
                self.utils.insertDataInTable(name, [list(exp.__dict__.values())])
        return

    def getDB(self):
        #print(WDelf.utils.selectAllFromTable('Drugs'))
        return self.utils

# Init = InitializerDB("D:/N_img")
# Init.getExperiments()
# Init.getRoiLLMData()
# # Init.createTables()
# # Init.insertDataInDB()
# Init.showData()