# from StreetEncoder.TextDetectionEncoder import *
# import torch, copy

class CImageProcessing():
    def __init__(self, bOD = False):
        # self.__device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__dInput = dict()
        # self.__oTextDetection = CTextDetectionEncoder()
        # if(bOD): self.__oObjectDetect = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        # if(not self.__oTextDetection.Open()):
        #     DebugPrint().error("Text detection module not opened")

    # def GetStreetEncoderImg(self, img):
    #     vCropImgs = self.__CropImgs(img)
    #     self.__dInput['org'] = self.ImageProcessing(img)
    #     self.__dInput['crop1'] = vCropImgs[0].to(self.__device, dtype=torch.float32)
    #     self.__dInput['crop2'] = vCropImgs[1].to(self.__device, dtype=torch.float32)
    #     self.__dInput['crop3'] = vCropImgs[2].to(self.__device, dtype=torch.float32)
    #     return self.__dInput

    def Reset(self):
        self.__dInput = dict()
        self.__oTextDetection.Reset()

    # def __CropImgs(self, image):
    #     # self.__oTextDetection.Control(eTextDetectionEncoderInfo.IMAGE, image)
    #     # vTextDetImgs = self.__oTextDetection.Read()
    #     vCropImgs = []
    #     for crop in vTextDetImgs:
    #         oImgTensor = torch.from_numpy(crop)
    #         w, h, c = oImgTensor.shape
    #         vCropImgs.append(torch.reshape(oImgTensor, (1, c, w, h)))
    #     return vCropImgs

    # def ObjectDetectionMask(self, query, match):
    #     image1 = copy.deepcopy(query)
    #     image2 = copy.deepcopy(match)
    #     oOdResult1 = self.__oObjectDetect(image1)
    #     oOdResult2 = self.__oObjectDetect(image2)
    #     image1 = self.__ProcessOD(oOdResult1, image1)
    #     image1 = self.__ProcessOD(oOdResult2, image1)
    #     image2 = self.__ProcessOD(oOdResult1, image2)
    #     image2 = self.__ProcessOD(oOdResult2, image2)
    #     return image1, image2

    def ImageProcessing(self, image, resize=False):
        oImage = image#cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if(resize):
            oImage = cv2.resize(oImage, (256, 256), cv2.INTER_AREA)
        w, h, c = oImage.shape
        # oImage = np.expand_dims(oImage, axis=0)
        # oImage = torch.from_numpy(oImage).to(self.__device, dtype=torch.float32)
        # oImage = torch.reshape(oImage, (1, c, w, h))
        return oImage

    def __ProcessOD(self, od_result, image):
        for od in od_result.xyxy[0]:
            if(8 < od[5]):
                continue
            image[int(od[1]):int(od[3]), int(od[0]):int(od[2])] = 0
        return image