from enum import Enum
import numpy as np
import dataclasses as dataclass

class ePixelFormat(Enum):
    eUNKNOWN_FORMAT = 0
    e8BIT = 10
    eGRAY8 = 11
    eRGB8 = 12
    eBGR8 = 13
    e16BIT = 20
    eGRAY12 = 21
    eGRAY14 = 22
    eGRAY16 = 23
    eRGB12 = 24
    eBGR12 = 25
    eRGB14 = 26
    eBGR14 = 27
    eRGB16 = 28
    eBGR16 = 29
    e32BIT = 30
    eGRAY32U = 31
    eRGB32U = 32
    eBGR32U = 33
    eGRAY32F = 34
    eRGB32F = 35
    eBGR32F = 36
    eCOMPRESSED = 50
    eYUV420P8 = 51
    eYUYV422I8 = 52
    eUYVY422I8 = 53

class eEncoding(Enum):
    eRAW = 0
    ePNG = 1
    eJPG = 2

@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class CImageTopic():
    def __init__(self, Width:np.uint16 = 1280, Height:np.uint16 = 720, PixelFormat:ePixelFormat = ePixelFormat.eRGB8, \
                Data:np.array = np.zeros((1, 1), dtype=np.uint8), Enc:eEncoding = eEncoding.eRAW):
        self.__Width = Width
        self.__Height = Height
        self.__PixelFormat = ePixelFormat(PixelFormat)
        self.__Data = Data
        self.__Enc = Enc

    @property
    def PixelFormat(self) -> ePixelFormat:
        return self.__PixelFormat
    
    @property
    def Height(self) -> np.uint16:
        return self.__Height

    @property
    def Width(self) -> np.uint16:
        return self.__Width

    @property
    def Data(self) -> np.array:
        return self.__Data

    @Data.setter
    def Data(self, Data:np.array) -> None:
        self.__Data = Data
        
    @property
    def Enc(self) -> eEncoding:
        return self.__Enc

    @Enc.setter
    def Enc(self, Enc:eEncoding) -> None:
        self.__Enc = Enc
    