import cv2
import mediapipe as mp
import numpy as np
import time
from gym import *
from utility import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_objectron = mp.solutions.objectron


objectron = mp_objectron.Objectron(static_image_mode=False,
                            max_num_objects=1,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.99,
                            model_name='Chair')

objectron2 = mp_objectron.Objectron(static_image_mode=False,
                            max_num_objects=1,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.99,
                            model_name='Cup')

detect_times = [time.time(),0,time.time(),0]

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)


mode = "normal"
# modes = [normal, study, night, gym]

last_time = 0 #last time change mode
buffer_time = 60

while cap.isOpened():
    cur_time = time.time()
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = pose.process(image)
    

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    image = cv2.flip(image, 1)

    if results.pose_landmarks:
        text = str(results.pose_landmarks.landmark[0].x)
        cv2.putText(image, text, (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 255, 255), 1, cv2.LINE_AA)
        text2 = str(results.pose_landmarks.landmark[0].y)
        cv2.putText(image, text2, (100, 100), cv2.FONT_HERSHEY_SIMPLEX,
        1, (0, 255, 255), 1, cv2.LINE_AA)

        # deal with gym 
        
        # if observe gym pose
        # enter gym mode
        
        if night_detect(image):
            
            last_time = time.time()

            text = "Night Mode"
            print("night mode")
            cv2.putText(image, text, (50, 200), cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 255), 1, cv2.LINE_AA)


            
            # detect if the quilt cover the body

            if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility > 0.8 or results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility > 0.8:
                # send signal

                posX, posY = get_body(results.pos_landmarks)

                if posX > 0.5:
                    direction_x = "LEFT"
                else:
                    direction_x = "RIGHT"

                if posY > 0.5:
                    direction_y = "UP"
                else:
                    direction_y = "DOWN"

                #send to arduino (direction_x, direction_y)

        

        elif gym_detect(results.pose_landmarks.landmark, detect_times):
            # send signal
            print("gym")

        
        elif study_detect():
            print("study")

        
        else:
            if cur_time-last_time > buffer_time:
                print("normal")
                # send normal signal to arduino

    else:
        results2 = objectron.process(image)
        if results2.detected_objects:
            for detected_object in results2.detected_objects:
                print(detected_object)
                """
                mp_drawing.draw_landmarks(
                image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                mp_drawing.draw_axis(image, detected_object.rotation,
                                    detected_object.translation)
                """
    #text3 = 'fps:' + str(fps)
    #cv2.putText(image, text3, (100, 150), cv2.FONT_HERSHEY_SIMPLEX,
    #1, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()