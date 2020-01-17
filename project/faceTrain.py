import os
import cv2
import numpy as np
from PIL import Image

import pickle

recognizer = cv2.face.LBPHFaceRecognizer_create();
path = 'dataSet'

def getImagesWithID(path):
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces=[]
    IDs = []
    for imagepath in imagepaths:
        faceImg = Image.open(imagepath).convert('L');  # convert to single channel( gray scale)
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagepath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return np.array(IDs),faces

IDs,faces = getImagesWithID(path)   # trả về 2 mảng id và face tương ứng

recognizer.train(faces,IDs)

recognizer.save('recognizer/trainningData.yml')
cv2.destroyAllWindows()