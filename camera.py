import time
import cv2
import face_recognition
import os
import subprocess

def capture(userid):
    target_folder='images'
    user_list=os.listdir(target_folder)
    if userid in user_list:
        print("Already exists",userid)
        return False
    else:
        userid_str = str(userid)
        user_folder = os.path.join(target_folder, userid_str)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
            print("New folder created")
        else:
            print("folder can't be created ")
            return False
    cam=cv2.VideoCapture(0)
    img_counter=1
    max_img=20
    while True:
        ret,frame =cam.read()
        if frame is None:
            print("empty frame")
            continue
        face_locations = face_recognition.face_locations(frame)
        for (top, right, bottom, left) in face_locations:
            # make a rectangle to show face is getting captured
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 250, 0), 2)
            # create a path to new folder
            img_file = f'{userid}_{img_counter}.png'
            img_path = os.path.join(user_folder, img_file)
            # writing the image to that location
            cv2.imwrite(img_path, frame)
            # increment img counter
            img_counter += 1
        cv2.imshow('Video', frame)
        if img_counter > max_img:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()
    # if (check()):
    #     faceEncodingswithIds = generatingList()
    #     file = open("model.pkl", "wb")
    #     pickle.dump(faceEncodingswithIds, file)
    #     file.close()
    subprocess.run(['python', 'encoding.py'])
    return True
