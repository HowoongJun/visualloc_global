###
#
#       @Brief          streetview.py
#       @Details        Streetview object for map2graph by using map server
#       @Org            Robot Learning Lab(https://rllab.snu.ac.kr), Seoul National University
#       @Author         Howoong Jun (howoong.jun@rllab.snu.ac.kr)
#       @Date           Apr. 29, 2022
#       @Version        v0.1
#
###

from common.Log import DebugPrint
import urllib.request
import cv2, json, sys
import numpy as np
from map.Map import eMapInfo
from socket import timeout
from urllib.error import HTTPError, URLError
from dataclasses import dataclass
import copy

@dataclass
class CStreetViewData():
    Image:np.ndarray = None
    Heading:float = None
    ID: int = None
    Latitude:float = None
    Longitude:float = None
    Feature:np.ndarray = None

class CStreetView():
    def __init__(self, IP, port=10001):
        self.__strStreetviewDown_URL = "http://" + IP + ":" + str(port) + "/"
        self.__strStreetviewInfo_URL = "http://" + IP + ":21501/wgs/"
        self.__strHeading = None
        
    def Control(self, eInfo:int, Value=None):
        eInformation = eMapInfo(eInfo)
        if(eInformation == eMapInfo.eMapInfo_LATITUDE):
            self.__fLatitude = float(Value)
        elif(eInformation == eMapInfo.eMapInfo_LONGITUDE):
            self.__fLongitude = float(Value)
        elif(eInformation == eMapInfo.eMapInfo_RADIUS):
            self.__fRadius = float(Value)
        elif(eInformation == eMapInfo.eMapInfo_HEADING):
            if(Value is not None): self.__strHeading = str(Value)
        elif(eInformation == eMapInfo.eMapInfo_DES_HEAD):
            self.__fDesiredHeading = float(Value)

    def Open(self):
        self.__strInfoQuery_URL = self.__strStreetviewInfo_URL + str(self.__fLatitude) + "/" + str(self.__fLongitude) + "/" + str(self.__fRadius)
        self.__oRequestInfo = urllib.request.Request(self.__strInfoQuery_URL)
        self.__vLatLon = np.array((self.__fLatitude, self.__fLongitude))
        return self.__oRequestInfo
        
    def Read(self):
        try:
            oResponse = urllib.request.urlopen(self.__oRequestInfo, timeout=10)
        except timeout:
            DebugPrint().warn("URL not opened")
            return None
        except URLError:
            DebugPrint().error("URLError")
            return None
        else:
            uResCode = oResponse.getcode()
            if(uResCode == 200):
                strResponseBody = oResponse.read()
                oJsonData = json.loads(strResponseBody.decode('utf-8'))
                vStreetViewData = []
                for json_component in oJsonData['features']:
                    oStreetViewData = CStreetViewData()

                    uStreetviewID = json_component['properties']['id']
                    fLatitude = json_component['properties']['latitude']
                    fLongitude = json_component['properties']['longitude']
                    fCurrHeading = json_component['properties']['heading']

                    oStreetViewData.Heading = self.__CalculateHeading(fCurrHeading)
                    oStreetViewData.ID = uStreetviewID
                    oStreetViewData.Latitude = fLatitude
                    oStreetViewData.Longitude = fLongitude
                    oStreetViewData.Image = self.GetStreetView(uStreetviewID)
                    vStreetViewData.append(oStreetViewData)
                return vStreetViewData
        return None

    def Reset(self):
        self.__fLatitude = None
        self.__fLongitude = None
        self.__fRadius = None
        self.__strHeading = None

    def GetStreetView(self, streetview_id):
        strImgQuery_URL = self.__strStreetviewDown_URL + str(streetview_id)
        if(self.__strHeading is not None): strImgQuery_URL += "/" + self.__strHeading
        oRequestInfo = urllib.request.Request(strImgQuery_URL)
        oResponse = urllib.request.urlopen(oRequestInfo)
        uResCode = oResponse.getcode()
        if(uResCode == 200):
            byteResponseBody = oResponse.read()
            mImg = np.asarray(bytearray(byteResponseBody), dtype=np.uint8)
            if(mImg.size == 0): return None
            oImg = cv2.imdecode(mImg, cv2.IMREAD_COLOR)
            return oImg
        return None

    def __CalculateHeading(self, heading):
        fHeading = copy.deepcopy(heading)
        if(self.__strHeading == 'r'):
            fHeading = heading + 90
        elif(self.__strHeading == 'l'):
            fHeading = heading - 90
        elif(self.__strHeading == 'b'):
            fHeading = heading - 180
        if(fHeading < 0): fHeading += 360
        if(fHeading > 360): fHeading -= 360
        return fHeading

