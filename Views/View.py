# coding=utf-8
from tkinter import *
from Data import Searcher
import numpy as np
import matplotlib.pyplot as plt
class app(Searcher):
    def __init__(self):
        self.TrepanationWindowBordersNameCell = ["G2", "G3", "G4", "G5"]
        self.TrepanationWindowBordersSizeCell = ["H2", "H3","H4", "H5"]
        self.mainDir = "/mnt/data/N_img"
        self.root = Tk()
        self.root.title("NeuroImagingHelper")
        self.root.geometry("660x300")
        self.data = []
        self.root.resizable(width=False, height=False)
        self.ROILLMFiles = []
        self.listboxName = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxName.place(x=10, y=32)
        self.listboxName.config()

        self.listboxDate = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxDate.place(x=150, y=32)
        self.listboxDate.config()

        self.listboxDrugs = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxDrugs.place(x=290, y=32)
        self.listboxDrugs.config()

        self.listboxDrugsForPlot = Listbox(self.root, selectmode=MULTIPLE, exportselection=0, selectbackground='#c3f8fa')
        self.listboxDrugsForPlot.place(x=10, y=164)
        self.listboxDrugsForPlot.config()

        self.prev_button = Button(text=u"Построить график", background='#d8e1e1',command=self.plotBoundery)
        self.prev_button.place(x=440, y=32)
        self.prev_button.config()

        self.dirs = self.searchDataFolderName()

        self.idx = 0
        self.idxDate = 0
        self.idxDrugs = 0

        self.drugList = self.getDrugsList()
        self.drugs = self.searchDrugsData()
        self.name = self.searchRatName()

        self.date = self.searchDateData()
        self.ROILLMFiles = self.searchRoiLLMFile()
        self.Boundery = self.searchBounderyData()
        self.coordsInfo = self.searchCoordsInfo()


        self.selectedRatsByDrugs = range(len(self.dirs))

        self.g_i()
        self.selectName()

        self.g_i_Date()
        self.selectDate()

        self.g_i_Drugs()

        self.root.configure(background='#d8e1e1')
        self.root.mainloop()

    def selectName(self, *args):
        value_name = [self.listboxName.get(idx) for idx in self.listboxName.curselection()]
        value_idx = [idx for idx in self.listboxName.curselection()]
        if len(value_name) == 0:
            self.listboxName.select_set(0)
            value_name = [self.listboxName.get(0)]
            value_idx = [0]
        name = value_name
        self.idx = value_idx
        print (self.idx, "Name index")
        return value_name, value_idx

    def g_i(self,selectedDrugsIndex=None):
        if len(np.array(self.name)[selectedDrugsIndex].shape)==2:
            self.listboxName.delete(0, 'end')
            itemList = np.array(self.name)[selectedDrugsIndex][0]
        else:
            self.listboxName.delete(0, 'end')
            itemList = np.array(self.name)[selectedDrugsIndex]
        for item in itemList:
            self.listboxName.insert(END, item)
        self.listboxName.bind('<<ListboxSelect>>', self.selectName)
        self.listboxName.select_set(0)
        self.listboxName.event_generate("<<ListboxSelect>>")

    def selectDate(self, *args):
        value_name = [self.listboxDate.get(idx) for idx in self.listboxDate.curselection()]
        value_idx = [idx for idx in self.listboxDate.curselection()]
        if len(value_name) == 0:
            self.listboxDate.select_set(0)
            value_name = [self.listboxDate.get(0)]
            value_idx = [0]
        self.date = value_name
        self.idxDate = value_idx
        print (self.idxDate, "Date index")
        return value_name, value_idx

    def g_i_Date(self):
        self.listboxDate.delete(0, 'end')
        for item in self.date:
            self.listboxDate.insert(END, item)
        self.listboxDate.bind('<<ListboxSelect>>', self.selectDate)
        self.listboxDate.select_set(0)
        self.listboxDate.event_generate("<<ListboxSelect>>")

    def selectDrugs(self, *args):
        self.selectedRatsByDrugs = []
        value_name = [self.listboxDrugs.get(idx) for idx in self.listboxDrugs.curselection()]
        value_idx = [idx for idx in self.listboxDrugs.curselection()]
        if len(value_name) == 0:
            self.listboxDrugs.select_set(0)
            value_name = [self.listboxDrugs.get(0)]
            value_idx = [0]
        selectedDrugs = value_name
        self.idxDrugs = value_idx
        for d, num in zip(self.drugs,range(len(self.drugs))):
            for sd in selectedDrugs:
                if sd in d:
                    self.selectedRatsByDrugs.append(num)
        self.selectedRatsByDrugs = np.unique(self.selectedRatsByDrugs)
        self.g_i(selectedDrugsIndex=self.selectedRatsByDrugs)
        return value_name, value_idx

    def g_i_Drugs(self):
        self.listboxDrugs.delete(0, 'end')
        for item in np.unique(np.concatenate(self.drugs)):
            self.listboxDrugs.insert(END, item)
        self.listboxDrugs.bind('<<ListboxSelect>>', self.selectDrugs)
        self.listboxDrugs.select_set(0)
        self.listboxDrugs.event_generate("<<ListboxSelect>>")

    def plotBoundery(self):
        boundary = np.array(self.Boundery)[self.selectedRatsByDrugs][self.idx]
        Rostral = float(boundary[0][1][0])
        Caudal = float(boundary[0][1][1])
        Medial = float(boundary[0][1][2])
        Lateral = float(boundary[0][1][3])
        plt.scatter(Caudal,Medial,color='green')
        plt.scatter(Rostral,Medial,color='green')
        plt.scatter(Caudal,Lateral,color='green')
        plt.scatter(Rostral,Lateral,color='green')
        xCR = np.linspace(Caudal,Rostral,num=5)
        yCR = [Medial]*5
        xCL = [Caudal]*5
        yCL = np.linspace(Medial,Lateral,num=5)
        xLR = np.linspace(Caudal,Rostral,num=5)
        yLR = [Lateral]*5
        xRL = [Rostral]*5
        yRL = np.linspace(Medial,Lateral,num=5)
        plt.plot(xCR,yCR,color='blue')
        plt.plot(xCL,yCL,color='blue')
        plt.plot(xLR,yLR,color='blue')
        plt.plot(xRL,yRL,color='blue')
        plt.show()
        return

A = app()
