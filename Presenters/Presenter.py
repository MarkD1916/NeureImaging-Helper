from Initializer import InitializerDB
from Data import Searcher
import numpy as np
import os
class InitPresenter():
    def __init__(self):
        self.utils=None

    def createNewDatabase(self,dbPath,dbName):
        Init = InitializerDB(dbPath,dbName)
        Init.getExperiments()
        Init.getRoiLLMData()
        Init.createTables()
        Init.insertDataInDB()
        self.utils = Init.getDB()
        return self.utils

    def getDrugs(self,utils = None):
        if self.utils==None:
            self.utils = utils
        drugs = np.ravel(self.utils.selectFromExpAndMetaExp("DrugName", "Drugs"))
        return drugs

    def getName(self,utils = None):
        if self.utils==None:
            self.utils = utils
        name = np.ravel(self.utils.selectAllFromTable("Experiments", "Name"))
        return name

class UpdatePresenter():
    def __init__(self):
        pass

class InsertPresenter():
    def __init__(self):
        pass

class ObserverPresenter():

    def getPath(utils):
        mainDir = '/'.join(utils.selectFieldFromTable("Path","Experiments")[0][0].split('/')[:-1])
        # def getCurrentPath(self):
        S = Searcher(mainDir=mainDir)
        print(len(S.searchExpPath()[1]))