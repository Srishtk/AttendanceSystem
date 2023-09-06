import cv2
import face_recognition
import pickle
import os

imageList = []
idList = []
encodingList = []
pathList=[]

def generatingList():
# importing images
    folderPath = 'images'
    pathList = os.listdir(folderPath)

    for path in pathList:
        subFolderPath = os.path.join(folderPath, path)
        images = os.listdir(subFolderPath)
        if images:
            for img in images:
                imageArray=cv2.imread(os.path.join(subFolderPath, img))
                imageList.append(imageArray)
                name = os.path.splitext(img)[0]
                img_final = cv2.cvtColor(imageArray, cv2.COLOR_BGR2RGB)
                encoding = face_recognition.face_encodings(img_final)
                if encoding:
                    encoding=encoding[0]
                    encodingList.append(encoding)
                    print("Adding",name)
                    idList.append(name)
                else:
                    pass
    faceEncodingswithIds = [encodingList, idList]
    return faceEncodingswithIds

def check():
    ids=[]
    for id in idList:
        idname=id.split('_')[0]
        ids.append(idname)
    for path in pathList:
        if path in ids:
            pass
        else:
            return False
    return True





# print(idList)
# def encodeImage(imageList):
#
#     for img in imageList:
#         print("print")
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encoding = face_recognition.face_encodings(img)
#         if encoding:
#             encoding=encoding[0]
#             encodingList.append(encoding)
#         else:
#             print("encoding not performed")
#     return encodingList

if(check()):
    faceEncodingswithIds=generatingList()
    file = open("model.pkl", "wb")
    pickle.dump(faceEncodingswithIds, file)
    file.close()
