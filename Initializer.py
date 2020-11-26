from Data import Searcher
from Parser import Parser
from DBUtils import Utils
#"D:/N_img"
class InitializerDB():

    def __init__(self,mainDir):
        self.search = Searcher(mainDir=mainDir)
        self.parser = Parser()
        self.experiments = {}
    def getExperiments(self):
        metaData = {"ID":[],"path":[],"name":[],"date":[]}
        date = self.search.searchDateData()
        path,name = self.search.searchExpPath()
        metaData["path"] = path
        metaData["name"] = name
        metaData["date"] = date
        metaData["ID"] = [1,4,5,7]#[x for x in range(1,len(path)+1)]
        return metaData

    def setExperimentsDataInDB(self):
        pass

    def getRoiLLMData(self):
        filesPath = self.search.searchRoiLLMFile()
        roiLLMData = self.parser.parseRoiLlmFile(filesPath)
        print  (roiLLMData)
        return
Init = InitializerDB("/mnt/data/N_img")
Init.getExperiments()
Init.getRoiLLMData()