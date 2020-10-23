import os
import re
import docx
class Searcher():

    def __init__(self,mainDir):
        self.mainDir = mainDir
        self.topLevelName = []

    def searchDataFolderName(self):
        self.topLevelName = [re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+",name).group(0)
                          for name in os.listdir(self.mainDir) if
             os.path.isdir(os.path.join(self.mainDir, name))
                        and re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+",name) is not None]


        return self.topLevelName

    def searchDateData(self):
        date = [re.match(r"(\d+.\d+.\d+)", name).group(0)
                        for name in os.listdir(self.mainDir) if
                        os.path.isdir(os.path.join(self.mainDir, name))
                        and re.match(r"(\d+.\d+.\d+)\s([А-Я]+|[а-я]+)\-[1-9]+", name) is not None]

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

    def searchDrugsData(self):
        for folderName in self.topLevelName:
            path = os.path.join(self.mainDir,folderName)
            #print (path)
            for i in self.walklevel(path,level=0):
                for prot in i[-1]:
                    if "Протокол от " in prot:
                        print (prot)
                        doc = docx.Document(prot)
                        fullText = []
                        for para in doc.paragraphs:
                            fullText.append(para.text)
                        print('\n'.join(fullText))
        return

    def walklevel(self,some_dir, level=1):
        some_dir = some_dir.rstrip(os.path.sep)
        assert os.path.isdir(some_dir)
        num_sep = some_dir.count(os.path.sep)
        for root, dirs, files in os.walk(some_dir):
            yield root, dirs, files
            num_sep_this = root.count(os.path.sep)
            if num_sep + level <= num_sep_this:
                del dirs[:]
    # def getText(filename):
    #     doc = docx.Document(filename)
    #     fullText = []
    #     for para in doc.paragraphs:
    #         fullText.append(para.text)
    #     return '\n'.join(fullText)
    # def load_prot(self, dirs):
    #     prot = []
    #     drugs_return = []
    #     for dir in dirs:
    #         for f in next(os.walk(self.dir + '/' + dir)):
    #             for l in f:
    #                 if 'docx' in l and 'Протокол от' in l:
    #                     text = docx2txt.process(self.dir + '/' + dir + '/' + l)
    #                     text_drugs = text[text.find(u"Вещество"):text.find(u"Вещество") + 300]
    #                     indx_drugs = ([(m.start(0), m.end(0)) for m in re.finditer('\d\n|[а-я]\.\n', text_drugs)])
    #                     # print text_drugs
    #                     drugs = np.array([i[:-1] for i in
    #                                       re.findall(u'[А-Я,а-я]+\,|[А-Я,а-я]+\s[А-Я,а-я]+\,',
    #                                                  text_drugs[indx_drugs[0][0]:indx_drugs[-2][0]])])
    #
    #                     mass_rat_str = text[text.find(u"Масса"):text.find(u"Масса") + 20]
    #                     prot.append(int(re.findall(r'\d+', mass_rat_str)[0]))
    #                     drugs_return.append(drugs)
    #
    #     # print prot
    #     return prot, drugs_return

Search = Searcher(mainDir="/mnt/data/N_img")
Search.searchDataFolderName()
Search.searchDrugsData()
#
#print(Search.searchDateData())