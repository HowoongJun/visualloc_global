# Main class for visual localization global
import imp
from gcore.hal import *

class CVisualLocGlobal(CVisualLocalizationCore):
    def __init__(self, model):
        if model == "mymodule":
            self.__module = imp.load_source(model, "./gcore/mymodule.py")
        elif model == "netvlad":
            print("Model: NetVLAD")
            self.__module = imp.load_source(model, "./globalfeature_ref/netvlad/netvlad.py")
        elif model == "gem":
            print("Model: GeM")
            self.__module = imp.load_source(model, "./globalfeature_ref/gem/gem.py")

    def __del__(self):
        print("GlobalFeature Destructor!")

    def Open(self):
        self.__model = self.__module.CModel()
    
    def Close(self):
        self.__model.Close()

    def Read(self):
        return self.__model.Read()

    def Write(self, strDescPath, strImgName):
        self.__model.Write(strDescPath, strImgName)

    def Setting(self, eCommand:int, Value = None):
        self.__model.Setting(eCommand, Value)

    def Reset(self):
        self.__model.Reset()
        self.__image = None
