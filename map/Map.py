###
#
#       @Brief          Map.py
#       @Details        Common map objects for map2graph
#       @Org            Robot Learning Lab(https://rllab.snu.ac.kr), Seoul National University
#       @Author         Howoong Jun (howoong.jun@rllab.snu.ac.kr)
#       @Date           Apr. 28, 2022
#       @Version        v0.1
#
###
from enum import IntEnum
from dataclasses import dataclass

class eMapInfo(IntEnum):
    eMapInfo_LATITUDE = 1
    eMapInfo_LONGITUDE = 2
    eMapInfo_VERTICAL = 3
    eMapInfo_HORIZONTAL = 4
    eMapInfo_XYSTEP = 5
    eMapInfo_RADIUS = 6
    eMapInfo_HEADING = 7
    eMapInfo_DES_HEAD = 8
    
    eMapQuery = 9

class eQueryInfo(IntEnum):
    eQueryInfo_POI = 1
    eQueryInfo_STREETVIEW = 2
    eQueryInfo_NODE = 3
    eQueryInfo_KEYWORD = 4
    
@dataclass
class CMapData():
    id: int = None
    place_name: str = None
    latitude: float = None
    longitude: float = None
    heading: float = None