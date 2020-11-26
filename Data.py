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
        self.date = []
        self.ROILLMFiles = []

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









# Search = Searcher(mainDir="D:/N_img")
# Search.searchDataFolderName()
# Search.searchDateData()
# Search.searchRoiLLMFile()
# print(Search.searchBounderyData())
# Search.searchCoordsInfo()