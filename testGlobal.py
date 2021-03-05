# Testing code for global feature
from GlobalFeature import *
from gcore.hal import eSettingCmd
import sys, os, cv2
import argparse
from glob import glob
import tensorflow.compat.v1 as tf

parser = argparse.ArgumentParser(description='Test Global Feature')
parser.add_argument('--model', '--m', type=str, default='mymodule', dest='model',
                    help='Model select: mymodule, netvlad, gem')
parser.add_argument('--db', '--d', default=None, dest='db',
                    help='DB creation mode: DB file save path')
parser.add_argument('--path', '--p', type=str, dest='path',
                    help='Image file path')
parser.add_argument('--resize', '--z', default = '[1280,720]', dest='resize',
                    help='Resize image [width, height] (default = [1280,720]')
parser.add_argument('--channel', '--c', type=int, default = 3, dest='channel',
                    help='Image channel')
args = parser.parse_args()

def readFolder(strImgFolder):
    if(not os.path.isdir(strImgFolder)):
        print("Path does not exist!")
        return False
    strPngList = [os.path.basename(x) for x in glob(strImgFolder + "*.png")]
    strJpgList = [os.path.basename(x) for x in glob(strImgFolder + "*.jpg")]
    strFileList = strPngList + strJpgList
    strFileList.sort()
    return strFileList

def makeDB(oModel) -> bool:
    strFileList = readFolder(args.path)
    if(strFileList is False):
        return False
    for fileIdx in strFileList:
        strImgPath = args.path + '/' + fileIdx
        model.Setting(eSettingCmd.eSettingCmd_IMAGE_DATA, imageRead(strImgPath))
        model.Write(args.db, fileIdx)
        model.Reset()
    return True

def queryCheck(oModel):
    strFileList = readFolder(args.path)
    if(strFileList is False):
        return False
    for fileIdx in strFileList:
        strImgPath = args.path + '/' + fileIdx
        model.Setting(eSettingCmd.eSettingCmd_IMAGE_DATA, imageRead(strImgPath))
        result = model.Read()
        print(result)
        model.Reset()
    return True

def imageRead(strImgPath):
    oImage = cv2.imread(strImgPath)
    if(oImage is None):
        return False
    lResize = list(eval(args.resize))
    iWidth = lResize[0]
    iHeight = lResize[1]
    if(args.channel == 1):
        oImage = cv2.cvtColor(oImage, cv2.COLOR_BGR2GRAY)
    oImgResize = cv2.resize(oImage, dsize=(iWidth, iHeight), interpolation = cv2.INTER_LINEAR)
    return oImgResize

def checkGPU():
    if(tf.config.experimental.list_physical_devices('GPU')):
        print("Using GPU..")
        return True
    else:
        print("Using CPU..")
        return False

if __name__ == "__main__":
    strModel = args.model

    model = CVisualLocGlobal(strModel)
    model.Open()
    model.Setting(eSettingCmd.eSettingCmd_IMAGE_CHANNEL, args.channel)
    model.Setting(eSettingCmd.eSettingCmd_CONFIG, checkGPU)
    if(args.db is not None):
        print("DB Creation Mode!")
        if(makeDB(model) is False):
            print("DB Creation Error!")
    else:
        print("Query mode!")
        if(queryCheck(model) is False):
            print("Query Mode Error!")