# Main class for visual localization global
import imp
import tensorflow.compat.v1 as tf

class CVisualLocGlobal():
    def __init__(self, model):
        if model == "mymodule":
            self.__module = imp.load_source(model, "./gcore/mymodule.py")
        elif model == "netvlad":
            print("Model: NetVLAD")
            self.__module = imp.load_source(model, "./globalfeature_ref/netvlad/netvlad.py")

    def __del__(self):
        print("GlobalFeature Destructor!")

    def Open(self):
        self.__model = self.__module.CModel()
    
    def Close(self):
        self.__model.Close()

    def Read(self):
        return self.__model.Read()

    def Write(self):
        self.__model.Write()

    def Control(self, oImage):
        if(tf.config.experimental.list_physical_devices('GPU')):
            self.__gpuCheck = True
        else:
            self.__gpuCheck = False

        self.__image = oImage
        self.__model.Control(oImage = self.__image, bGPUFlag = self.__gpuCheck)

    def Reset(self):
        self.__model.Reset()
