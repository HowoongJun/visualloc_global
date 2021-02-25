# Testing code for global feature
from GlobalFeature import *
import sys
from gcore.ImageTopic import CImageTopic

if __name__ == "__main__":
    strArg = "mymodule"
    if len(sys.argv) > 1:
        strArg = sys.argv[1]
    
    model = CVisualLocGlobal(strArg)
    model.Open()
    model.Control()
    model.Read()
    
