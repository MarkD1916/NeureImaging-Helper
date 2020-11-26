import unittest
from Initializer import InitializerDB
import numpy as np
class TestInitializerDBMethods(unittest.TestCase):
    def setUp(self):
        self.init = InitializerDB("/mnt/data/N_img")
    def test_length(self):

        metaDataLens = []
        metaData = self.init.getExperiments()
        for k in metaData.keys():
            metaDataLens.append(len(metaData[k]))

        if len(np.unique(metaDataLens))==1:
            print ("Длины массивов равны")
        else:
            print ("Длинны массивов не равны")

    def test_notNone(self):
        metaData = self.init.getExperiments()
        for k in metaData.keys():
            if None in metaData[k]:
                print ("None в столбце {}".format(k))
            else:
                print ("None не найдено в столбце {}".format(k))


if __name__ == '__main__':
    unittest.main()

