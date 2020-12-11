import openpyxl

class Parser():
    def __init__(self):
        pass

    def getDataFromColumnXlsx(self, sh, decodingColumn):
        val = 2
        drugsNameList = []
        while val != None:
            drugName = sh[decodingColumn + str(val)].value
            if drugName == None:
                break
            drugsNameList.append(drugName)
            val += 1
        return drugsNameList


    def parseRoiLlmFile(self,ROILLMFiles):
        InfoID = {}
        for path, ID in zip(ROILLMFiles,range(1,len(ROILLMFiles)+1)):
            fileInfo={"drugName":[],"valve":[],"xValue":[],"yValue":[],"rostral":[],"caudal":[],"medial":[],"lateral":[]}
            TrepanationWindowBordersNameCell = ["H2", "H3", "H4", "H5"]
            TrepanationWindowBordersSizeCell = ["K2", "K3", "K4", "K5"]
            if path!="No file":
                workbook = openpyxl.load_workbook(path,data_only=True)
                sh = workbook["Sheet1"]
                for cellName, bordersSize in zip(TrepanationWindowBordersNameCell,TrepanationWindowBordersSizeCell):
                    func = lambda s: s[:1].lower() + s[1:] if s else ''
                    fileInfo[func(sh[cellName].value)]=[sh[bordersSize].value]
                for k, column in zip(fileInfo.keys(),["C","B","E","F"]):
                    fileInfo[k] = self.getDataFromColumnXlsx(sh=sh,decodingColumn=column)
            else:
                for k in fileInfo.keys():
                    fileInfo[k] = ["Файл не найден"]
            InfoID[ID] = fileInfo
        return InfoID