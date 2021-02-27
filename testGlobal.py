# Testing code for global feature
from GlobalFeature import *
import sys
import cv2

if __name__ == "__main__":
    strArg = "mymodule"
    if len(sys.argv) > 1:
        strArg = sys.argv[1]
    
    model = CVisualLocGlobal(strArg)
    model.Open()
    strImgPath = "./test.png"
    img = cv2.imread(strImgPath)
    if(img is None):
        sys.quit()
    iWidth = 1280
    iHeight = 720
    img = cv2.resize(img, dsize = (iWidth, iHeight), interpolation = cv2.INTER_LINEAR)
    model.Control(img)
    model.Read()
    
