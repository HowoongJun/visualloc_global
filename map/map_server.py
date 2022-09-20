###
#
#       @Brief          map_server.py
#       @Details        map api handler for map server
#       @Org            Robot Learning Lab(https://rllab.snu.ac.kr), Seoul National University
#       @Author         Howoong Jun (howoong.jun@rllab.snu.ac.kr)
#       @Date           Apr. 27, 2022
#       @Version        v0.1
#
###
from map.Map import eMapInfo, eQueryInfo
from map.Map import CMapData
import urllib.request
import json

class CMapHandler():
    def __init__(self, IP):
        self.__strPOI_URL = "http://" + IP + ":21502/wgs/"
        self.__strStreetview_URL = "http://" + IP + ":21501/wgs/"
        self.__strNode_URL = "http://" + IP + ":21500/wgs/"

    def Control(self, eInfo:int, Value=None):
        eInformation = eMapInfo(eInfo)
        if(eInformation == eMapInfo.eMapInfo_LATITUDE):
            self.__fLatitude = float(Value)
        elif(eInformation == eMapInfo.eMapInfo_LONGITUDE):
            self.__fLongitude = float(Value)
        elif(eInformation == eMapInfo.eMapInfo_RADIUS):
            self.__fRadius = float(Value)
        elif(eInformation == eMapInfo.eMapQuery):
            self.__eQuery = eQueryInfo(Value)
        
    def Open(self):
        if(self.__eQuery == eQueryInfo.eQueryInfo_POI):
            self.__strQueryURL = self.__strPOI_URL
        elif(self.__eQuery == eQueryInfo.eQueryInfo_STREETVIEW):
            self.__strQueryURL = self.__strStreetview_URL
        elif(self.__eQuery == eQueryInfo.eQueryInfo_NODE):
            self.__strQueryURL = self.__strNode_URL
        self.__strQueryURL += str(self.__fLatitude) + "/" + str(self.__fLongitude) + "/" + str(self.__fRadius)
        self.__oRequest = urllib.request.Request(self.__strQueryURL)

    def Read(self):
        oResponse = urllib.request.urlopen(self.__oRequest)
        uResCode = oResponse.getcode()
        if(uResCode == 200):
            strResponseBody = oResponse.read()
            oJsonData = json.loads(strResponseBody.decode('utf-8'))
            vParsedData = []
            for json_component in oJsonData['features']:
                oParsedData = CMapData()
                oParsedData.id = json_component['properties']['id']
                oParsedData.place_name = json_component['properties']['name']
                oParsedData.longitude = json_component['properties']['longitude']
                oParsedData.latitude = json_component['properties']['latitude']
                if(self.__eQuery == eQueryInfo.eQueryInfo_STREETVIEW): oParsedData.heading = json_component['properties']['heading']
                vParsedData.append(oParsedData)
            return vParsedData
        return None
        
    