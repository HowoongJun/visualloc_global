###
#
#       @Brief          eval.py
#       @Details        Evaluation for street encoder
#       @Org            Robot Learning Lab(https://rllab.snu.ac.kr), Seoul National University
#       @Author         Howoong Jun (howoong.jun@rllab.snu.ac.kr)
#       @Date           Aug. 05, 2022
#       @Version        v0.1
#
###

from map.streetview import *
# from nets.ImageTextEncoder import *
# from StreetEncoder.TextDetectionEncoder import *
import map.Map as Map
import os, copy, cv2, time, random
# from math import dist
from scipy import spatial
from eval.ImageProcessing import CImageProcessing
from gcore.hal import eSettingCmd
# from nets.pclbuilder import MoCo

class CEval():
    def __init__(self, IP, port=10001):
        self.__strResultPath = "./results/"
        self.__oStreetView = CStreetView(IP, port)
        self.__oImgProcess = CImageProcessing()
        if(port == 10000): self.__bIsCoexDataset = True
        else: self.__bIsCoexDataset = False

        if(port == 10002):
            self.__fMinMaxLat = [36.33, 36.388]
            self.__fMinMaxLon = [127.35, 127.379]
        else:
            self.__fMinMaxLat = [37.493, 37.51]
            self.__fMinMaxLon = [127.02, 127.063]

    def Open(self, model):
        self.__oModel = model
                
    def Run(self):
        now = time.localtime()
        self.__strResultPath += time.strftime("%Y%m%d_%H%M%S/", now)
        os.mkdir(self.__strResultPath)
        vStreetViewData = self.__RandomStreetView()
        vFeatureData = []
        DebugPrint().info("Downloaded " + str(len(vStreetViewData)) + " images!")
        for sv_data in vStreetViewData:
            oInputImg = self.__oImgProcess.ImageProcessing(sv_data.Image)
            self.__oModel.Setting(eSettingCmd.eSettingCmd_IMAGE_DATA, oInputImg)
            oFeature = self.__oModel.Read()
            oOutput = copy.deepcopy(sv_data)
            oOutput.Feature = oFeature
            vFeatureData.append(oOutput)

        for org in vFeatureData:
            oSrcImg = copy.deepcopy(org.Image)
            strSrcTag = "Src Image(" + str(org.ID) + "): " + str(org.Latitude) + ", " + str(org.Longitude)
            oSrcImg = cv2.putText(oSrcImg, strSrcTag, (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            oConcatImg = oSrcImg
            vDistOrder = []
            for cpr in vFeatureData:
                if(org.ID == cpr.ID):
                    continue
                oCprImg = copy.deepcopy(cpr.Image)
                # fDist = dist(org.Feature, cpr.Feature)
                fDist = spatial.distance.cosine(org.Feature, cpr.Feature)
                strCprTag = str(cpr.ID) + ": " + str(cpr.Latitude) + ", " + str(cpr.Longitude) + ", " + str(cpr.Heading) + " deg"
                oCprImg = cv2.putText(oCprImg, strCprTag, (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                oCprImg = cv2.putText(oCprImg, str(fDist), (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                dCprImg = {'dist': fDist, 'img': oCprImg}
                vDistOrder.append(dCprImg)
            vDistOrder = sorted(vDistOrder, key=lambda d: d['dist'])
            for dist_order in vDistOrder[0:5]:
                oConcatImg = cv2.hconcat([oConcatImg, dist_order['img']])
            cv2.imwrite(self.__strResultPath + str(org.ID) + "_" + str(org.Heading) + ".png", oConcatImg)
                
        return True

    def __RandomStreetView(self):
        uRadius = 30
        if(self.__bIsCoexDataset): vHeading = ['0', '1', '2', '3', '4', '5']
        else: vHeading = ['l', 'r']
        fLat = random.uniform(self.__fMinMaxLat[0], self.__fMinMaxLat[1])
        fLon = random.uniform(self.__fMinMaxLon[0], self.__fMinMaxLon[1])
        self.__oStreetView.Control(Map.eMapInfo.eMapInfo_LATITUDE, fLat)
        self.__oStreetView.Control(Map.eMapInfo.eMapInfo_LONGITUDE, fLon)
        uCounter = 0
        while(1):
            uCounter += 1
            if(uCounter > 50):
                DebugPrint().info("Resample main node Lat,lon")
                fLat = random.uniform(self.__fMinMaxLat[0], self.__fMinMaxLat[1])
                fLon = random.uniform(self.__fMinMaxLon[0], self.__fMinMaxLon[1])
                self.__oStreetView.Control(Map.eMapInfo.eMapInfo_LATITUDE, fLat)
                self.__oStreetView.Control(Map.eMapInfo.eMapInfo_LONGITUDE, fLon)
                uCounter = 0
                uRadius = 10
            self.__oStreetView.Control(Map.eMapInfo.eMapInfo_RADIUS, uRadius)
            self.__oStreetView.Open()
            vStreetViewData = []
            for heading in vHeading:
                self.__oStreetView.Control(Map.eMapInfo.eMapInfo_HEADING, heading)
                vStreetViewData_Heading = self.__oStreetView.Read()
                if(vStreetViewData_Heading is not None):
                    vStreetViewData += vStreetViewData_Heading

            if(vStreetViewData is None): continue
            if(len(vStreetViewData) < 100):
                DebugPrint().info("Expanding radius into.. " + str(uRadius + 10))
                uRadius += 10
                continue
            return vStreetViewData