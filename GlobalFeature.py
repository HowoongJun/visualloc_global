# Main class for visual localization global
import imp
from gcore.hal import *
import common.Log as log

class CVisualLocGlobal(CVisualLocalizationCore):
    def __init__(self, model):
        self.__gemInput = None
        if model == "mymodule":
            self.__module = imp.load_source(model, "./gcore/mymodule.py")
        elif model == "netvlad":
            log.DebugPrint().info("Model: NetVLAD")
            self.__module = imp.load_source(model, "./globalfeature_ref/netvlad/netvlad.py")
        elif model == "gem":
            log.DebugPrint().info("Model: GeM")
            self.__module = imp.load_source(model, "./globalfeature_ref/gem/gem.py")
            self.__gemInput = int(input("GeM Input\n 1 = gem pool fully connected\n 2 = gem pool learned whitening transformation \n 3 = mac pooling with pre-trained Image Net \n"))
        elif model == "cam":
            log.DebugPrint().info("Model: CAM")
            self.__module = imp.load_source(model, "./globalfeature_ref/cam/cam.py")
        else:
            log.DebugPrint().error("Model name error! Check model name again")

    def __del__(self):
        log.DebugPrint().info("GlobalFeature Destructor!")

    def Open(self):
        self.__model = self.__module.CModel()
        if(self.__gemInput is not None):
            self.__model.Setting(eSettingCmd.eSettingCmd_GEM, self.__gemInput)

    def Close(self):
        self.__model.Close()

    def Read(self):
        return self.__model.Read()
        
    def Write(self, strDescPath, strImgName):
        if(self.__model.Write(strDescPath, strImgName) is True):
            return True
        else:
            return False

    def Setting(self, eCommand:int, Value = None):
        self.__model.Setting(eCommand, Value)

    def Reset(self):
        self.__model.Reset()
        self.__image = None
