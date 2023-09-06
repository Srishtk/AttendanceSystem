import pickle
import cv2
import face_recognition
import numpy as np
import time


# load the face encodings
file = open("model.pkl", "rb")
faceEncodingswithId = pickle.load(file)
file.close()
encodingList, idList = faceEncodingswithId
# print(idList)


# setup camera
cam = cv2.VideoCapture(0)
frame_skip = 4  # Process every 4th frame
frame_counter = 0
duration=10 #automatically shut the camera in 10 secs
start_time = time.time()
while True:
    flag = False
    ret, frame = cam.read()
    # if frame is None:
    #     print("empty")

    # Resize the frame
    smallframe = cv2.resize(frame, (0, 0), None, 0.75, 0.75)
    # checking after every 4th frame only
    if frame_counter % frame_skip == 0:
        face_locations = face_recognition.face_locations(smallframe)
        face_encodings = face_recognition.face_encodings(smallframe, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            results = face_recognition.compare_faces(encodingList, face_encoding)
            faceDist = face_recognition.face_distance(encodingList, face_encoding)
            # print(results)
            # print(faceDist)
            index = np.argmin(faceDist)
            if results[index]:
                # making a rectangle
                cv2.rectangle(smallframe, (left, top), (right, bottom), (0, 250, 0), 2)
                id = idList[index]
                id = id.split('_')[0]

                # result=Users.query.get(id)
                # username=result.userName
                # record=Attendance(
                #     userId=id,
                #     userName=username,
                #     AttendanceTime=datetime.now()
                # )
                # db.session.add(record)
                # db.session.commit()
                print(id)
                flag = True
        cv2.imshow('Video', smallframe)

    frame_counter += 1
    #after 10 secs
    elapsed_time = time.time() - start_time
    if elapsed_time >= duration:
        break
    #if matching face is found
    if flag == True:
        break
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
cam.release()
cv2.destroyAllWindows()
