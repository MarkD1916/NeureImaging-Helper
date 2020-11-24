import os
import re
#import docx
import numpy as np
from os import listdir
from os.path import isfile, join
import openpyxl

class Searcher():

    def __init__(self,mainDir):
        self.mainDir = mainDir
        self.topLevelName = []
        self.drugsList=[]
        self.date = []
        self.TrepanationWindowBordersNameCell = ["G2","G3","G4","G5"]
        self.TrepanationWindowBordersSizeCell = ["H2", "H3", "H4", "H5"]
        self.ROILLMFiles = []




    def getDrugsList(self):
        drugsList = np.loadtxt("./drugsFile.txt",dtype='str',delimiter='\t')
        self.drugsList = drugsList

    def searchExpPath(self):
        self.topLevelName = [self.mainDir+"/"+re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+",name).group(0)
                          for name in os.listdir(self.mainDir) if
             os.path.isdir(os.path.join(self.mainDir, name))
                        and re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+",name) is not None]
        name = [re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+", name).group(0)
                             for name in os.listdir(self.mainDir) if
                             os.path.isdir(os.path.join(self.mainDir, name))
                             and re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+", name) is not None]


        return self.topLevelName, name

    def searchExpMethod(self):
        methods = []
        for folderName,d in zip(self.topLevelName,self.date):
            path = os.path.join(self.mainDir,folderName,d+"_coordinates","prog")

            try:
                meth = np.unique([f.split('_',1)[1].split('.')[0] for f in listdir(path) if isfile(join(path, f))])
            except FileNotFoundError:
                meth = "No xlsx file"
            methods.append(meth)
        return methods
    def searchDateData(self):
        date = [re.match(r"(\d+.\d+.\d+)", name).group(0)
                        for name in os.listdir(self.mainDir) if
                        os.path.isdir(os.path.join(self.mainDir, name))
                        and re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+", name) is not None]
        self.date = date

        return date

    def searchRatName(self):
        name = [''.join(re.findall(r"([А-Я]+|[а-я]+)(\-)([1-9]+)", name)[0])
                for name in os.listdir(self.mainDir) if
                os.path.isdir(os.path.join(self.mainDir, name))
                and len(re.findall(r"([А-Я]+|[а-я]+)(\-)([1-9]+)", name))>0
                ]
        return name

    def searchCoordData(self):
        return

    # def searchDrugsData(self):
    #     AllDrugs=[]
    #     for folderName in self.topLevelName:
    #         path = os.path.join(self.mainDir,folderName)
    #         for i in self.walklevel(path,level=0):
    #             Drugs = []
    #             for prot in i[-1]:
    #
    #                 if "Протокол от " in prot:
    #
    #                     text = docx2txt.process(os.path.join(path,prot))
    #                     text_drugs = text[text.find(u"Вещество"):text.find(u"Вещество") + 300]
    #                     for i,j in zip(np.unique(self.drugsList),range(len(self.drugsList))):
    #                         if i.strip() in text_drugs:
    #                             Drugs.append(i.strip())
    #                     if len(re.findall(r"[1-9]\n", text_drugs))>len(np.unique(Drugs)):
    #                         Drugs.append("Есть неизвестные вещества")
    #                     AllDrugs.append(np.unique(Drugs))
    #             if len(Drugs) == 0:
    #                 AllDrugs.append(["Не обнаружен протокол"])
    #
    #     return AllDrugs


    def walklevel(self,some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]

    def searchRoiLLMFile(self):
        for folderName,d in zip(self.topLevelName,self.date):
            path = os.path.join(self.mainDir,folderName,d+"_coordinates","prog",d+"_ROI_LLM.xlsx")
            try:
                workbook = openpyxl.load_workbook(path,data_only=True)
                self.ROILLMFiles.append(path)
            except FileNotFoundError:
                self.ROILLMFiles.append("No file")
        return self.ROILLMFiles

    def searchBounderyData(self):
        bounderyInfoID = {}
        borders = []
        for path, ID in zip(self.ROILLMFiles,range(1,len(self.ROILLMFiles)+1)):
            if path!="No file":
                bordersSizeList = [[], []]
                workbook = openpyxl.load_workbook(path,data_only=True)
                sh = workbook["Sheet1"]
                for cellName, bordersSize in zip(self.TrepanationWindowBordersNameCell,self.TrepanationWindowBordersSizeCell):
                    bordersSizeList[0].append(sh[cellName].value)
                    bordersSizeList[1].append(str(sh[bordersSize].value))
                bounderyInfoID[ID] = bordersSizeList

        return bounderyInfoID

    def searchDrugs(self):
        coordsInfoID={}
        for path,ID in zip(self.ROILLMFiles,range(1,len(self.ROILLMFiles)+1)):
            decodingColumnDrugName = "C"
            if path != "No file":
                workbook = openpyxl.load_workbook(path, data_only=True)
                sh = workbook["Sheet1"]
                val = 2
                drugsNameList=[]
                while val!=None:
                    drugName = sh[decodingColumnDrugName+str(val)].value
                    if drugName==None:
                        break
                    drugsNameList.append(drugName)
                    val+=1
                coordsInfoID[ID] = drugsNameList
        return coordsInfoID

    def searchValve(self):

        valveInfo = {}
        for path, ID in zip(self.ROILLMFiles, range(1, len(self.ROILLMFiles) + 1)):
            decodingColumnDrugName = "B"
            if path != "No file":
                workbook = openpyxl.load_workbook(path, data_only=True)
                sh = workbook["Sheet1"]
                val = 2
                valvesNameList = []
                while val != None:
                    drugName = sh[decodingColumnDrugName + str(val)].value
                    if drugName == None:
                        break
                    valvesNameList.append(drugName)
                    val += 1
                if len(valvesNameList)==0:
                    valvesNameList = ["Не указан"]

                valveInfo[ID] = valvesNameList
        return valveInfo




# Search = Searcher(mainDir="D:/N_img")
# Search.searchDataFolderName()
# Search.searchDateData()
# Search.searchRoiLLMFile()
# print(Search.searchBounderyData())
# Search.searchCoordsInfo()