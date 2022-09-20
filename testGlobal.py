# Testing code for global feature
from GlobalFeature import *
from gcore.hal import eSettingCmd
import sys, os, cv2
import argparse
from glob import glob
import tensorflow.compat.v1 as tf
import common.Log as log
import numpy as np
from eval.eval import *

parser = argparse.ArgumentParser(description='Test Global Feature')
parser.add_argument('--model', '--m', type=str, default='mymodule', dest='model',
                    help='Model select: mymodule, netvlad, gem, cam')
parser.add_argument('--db', '--d', type=str, dest='db',
                    help='DB creation mode: DB file save path')
parser.add_argument('--path', '--p', type=str, dest='path',
                    help='Image file path')
parser.add_argument('--resize', '--z', default = '[1280,720]', dest='resize',
                    help='Resize image [width, height] (default = [1280,720]')
parser.add_argument('--channel', '--c', type=int, default = 3, dest='channel',
                    help='Image channel')
parser.add_argument('--mode', '--o', type=str, dest='mode',
                    help='Mode select: makedb, query, match')
args = parser.parse_args()

def readFolder(strImgFolder):
    if(not os.path.isdir(strImgFolder)):
        log.DebugPrint().warning("Path does not exist!")
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
    print(len(strFileList))
    for fileIdx in strFileList:
        strImgPath = args.path + '/' + fileIdx
        oModel.Setting(eSettingCmd.eSettingCmd_IMAGE_DATA, imageRead(strImgPath))
        if(oModel.Write(args.db, fileIdx) is False):
            log.DebugPrint().error("Fail to write DB for image " + str(fileIdx))
            return False
        log.DebugPrint().info(str(fileIdx) + " Image finished!")
        oModel.Reset()
    return True

def queryCheck(oModel):
    strFileList = readFolder(args.path)
    if(strFileList is False):
        return False
    for fileIdx in strFileList:
        strImgPath = args.path + '/' + fileIdx
        oModel.Setting(eSettingCmd.eSettingCmd_IMAGE_DATA, imageRead(strImgPath))
        vResult = oModel.Read()
        # print(vResult)
        oModel.Reset()
    return True

def queryMatch(oModel):
    strQueryList = readFolder(args.path)
    strDbPath = args.db + '/' + args.model + '/'
    strDbList = [os.path.basename(x) for x in glob(strDbPath + '*.npy')]
    if(strQueryList is False):
        return False
    for fileIdx in strQueryList:
        strQueryPath = args.path + '/' + fileIdx
        oModel.Setting(eSettingCmd.eSettingCmd_IMAGE_DATA, imageRead(strQueryPath))
        vResult = oModel.Read()
        vEucDist = []
        vMatchedImage = []
        for dbIdx in strDbList:
            strNpyPath = strDbPath + dbIdx
            vDbResult = np.load(strNpyPath)
            fEucDist = np.linalg.norm(np.abs(vDbResult - vResult))
            vEucDist.append(fEucDist)

        for idxTopN in range(0, 5):
            minIdx = np.argmin(vEucDist)
            vMatchedImage.append(strDbList[minIdx].replace('.npy', ''))
            vEucDist[minIdx] = float('inf')
        log.DebugPrint().info(str(fileIdx) + ": " + str(vMatchedImage))

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
        log.DebugPrint().info("Using GPU..")
        return True
    else:
        log.DebugPrint().info("Using CPU..")
        return False

if __name__ == "__main__":
    strModel = args.model

    model = CVisualLocGlobal(strModel)
    model.Open()
    model.Setting(eSettingCmd.eSettingCmd_IMAGE_CHANNEL, args.channel)
    model.Setting(eSettingCmd.eSettingCmd_CONFIG, checkGPU)
    if(args.mode == "makedb"):
        log.DebugPrint().info("DB Creation Mode!")
        if(makeDB(model) is False):
            log.DebugPrint().error("DB Creation Error!")
    elif(args.mode == "query"):
        log.DebugPrint().info("Query mode!")
        if(queryCheck(model) is False):
            log.DebugPrint().error("Query Mode Error!")
    elif(args.mode == "match"):
        log.DebugPrint().info("Matching mode!")
        if(queryMatch(model) is False):
            log.DebugPrint().error("Matching Mode Error!")
    elif(args.mode == "streetview"):
        log.DebugPrint().info("Streetview mode!")
        oEval = CEval("147.46.111.251")
        oEval.Open(model)
        oEval.Run()