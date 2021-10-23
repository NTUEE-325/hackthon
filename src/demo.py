import cv2
import mediapipe as mp
import numpy as np
import time
from gym import *
from utility import *
#from controller import *
import os
if os.path.exists("./data/SleepHistory.txt"):
    os.remove("./data/SleepHistory.txt")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mp_objectron = mp.solutions.objectron

# detect chair
objectron = mp_objectron.Objectron(static_image_mode=False,
                                   max_num_objects=1,
                                   min_detection_confidence=0.5,
                                   min_tracking_confidence=0.99,
                                   model_name='Chair')

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(1)


mode = "init"
# modes = [normal, study, night, gym]
last_detect_chair_time = 0
last_time = 0  # last time change mode
buffer_time = 5
chair_pos = 0
chair_size = 0
# detect for the gym mode
detect_times = [time.time(), 0, time.time(), 0, 0]

time_record = [0, 0, 0, 0, 0]
# time_record records the ongoing time for each mode. only one of them is nonzero.
# indices: [quilt_cover_true, quilt_cover_false, gym, normal, study]
air_conditioner_strength_time_constant = 100
# time constant for the adjustment of air conditioner strength (exponential interpolation)
air_conditioner_strength = 0
# strength of the air conditioner
# when setting the real air conditioner strength, the strength is mapped to 1~5(int):
# floor(air_conditioner_strength*5)+1

center = (600, 350)
arrow_length = 100
# direction of the wind: initially at the center
air_conditioner_direction = [0, 0]
'''
if want to have "opposite direction":
    1. detect the direction of people with respect to the point (0.5, 0.5)
    2. air_conditioner_distance + people_position(respect to (0.5, 0.5)) remains constant (0.5)
    ex. the people is in (0.2, 0.3). then the direction is (0.5, 0.5)+(0.3, 0.2)*sqrt(12)/sqrt(13)

this is implemented in utility.py.
'''


sleepHistory = open("./data/SleepHistory.txt", 'x')


while cap.isOpened():
    cur_time = time.time()
    success, image = cap.read()
    h, w, _ = image.shape
    #print(h, w)
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #image = cv2.flip(image, 1)
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
    if cur_time-last_detect_chair_time > buffer_time and (mode != "study"):
        chair_pos = 0
        chair_size = 0
    if results.pose_landmarks:

        # deal with gym
        # if observe gym pose
        # enter gym mode
        posX, posY = get_body(results.pose_landmarks)

        if night_detect(image):

            last_time = time.time()

            if mode != "night":
                print("night mode")
                mode = "night"
                #SetMode("night")

            # detect if the quilt cover the body
            quilt_cover = False
            if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility > 0.8 or results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility > 0.8:
                # send signal
                if not quilt_cover:
                    record_dangerous_sleeping()
                    quilt_cover = True

                air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                    posX, posY)
                # send to arduino (direction_x, direction_y)
            else:
                quilt_cover = False

        elif gym_detect(image, results.pose_landmarks, detect_times):
            # send signal
            last_time = time.time()
            if mode != "gym":
                print("gym mode")
                mode = "gym"
                # SetMode("gym")
                air_conditioner_direction = calculate_air_conditioner_direction(
                    posX, posY)
                print("gym:", gym_detect(
                    image, results.pose_landmarks, detect_times))

                '''sleepHistory = open("../data/SleepHistory.txt", "a")
                sleepHistory.write(
                    str(time.asctime(time.localtime(time.time())))+'\n')
                sleepHistory.close()'''

            else:
                air_conditioner_direction = calculate_air_conditioner_direction(
                    posX, posY)

        elif study_detect(results.pose_landmarks, chair_pos, chair_size):
            last_time = time.time()
            if mode != "study":
                air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                    posX, posY)
                print("study mode")
                # SetMode("study")
                mode = "study"
            if mode == "study":
                air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                    posX, posY)

        else:
            if cur_time-last_time > buffer_time:
                if mode != "normal":
                    # SetMode("normal")
                    air_conditioner_direction = (
                        calculate_air_conditioner_direction_inverse(posX, posY))
                    print("normal mode")
                    mode = "normal"
                else:
                    air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                        posX, posY)
                # print("normal")
                # send normal signal to arduino

    else:
        results2 = objectron.process(image)
        if results2.detected_objects:
            last_detect_chair_time = time.time()
            if mode != "normal":
                #SetMode("normal")
                print("normal mode")
                mode = "normal"
            for detected_object in results2.detected_objects:
                mp_drawing.draw_landmarks(
                    image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                mp_drawing.draw_axis(image, detected_object.rotation,
                                     detected_object.translation)
                chair_pos = detected_object.landmarks_2d.landmark[0]
                text = str(chair_pos.x)
                cv2.putText(image, text, (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 1, cv2.LINE_AA)
                text2 = str(chair_pos.y)
                cv2.putText(image, text2, (100, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 255), 1, cv2.LINE_AA)
                chair_size = detected_object.scale

    #text3 = 'fps:' + str(fps)
    # cv2.putText(image, text3, (100, 150), cv2.FONT_HERSHEY_SIMPLEX,
    # 1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.circle(
        image, (int(air_conditioner_direction[0]*w), int(air_conditioner_direction[1]*h)), 15, (255, 0, 0), -1)
    if results.pose_landmarks:
        cv2.circle(
            image, (int(get_body(results.pose_landmarks)[0]*w), int(get_body(results.pose_landmarks)[1]*h)), 15, (0, 255, 0), -1)
        text3 = str(get_fan_angle(
            air_conditioner_direction[0], air_conditioner_direction[1]))
        cv2.putText(image, text3, (100, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('MediaPipe Pose', image)

    background = cv2.imread("./img/background.jpg")
    text = str(mode)

    normalized = ((air_conditioner_direction[0]-0.5)**2+(air_conditioner_direction[1]-0.5)**2)**0.5
    start_pos = (int(center[0]-arrow_length*(air_conditioner_direction[0]-0.5)/normalized), int(center[1]-arrow_length*(air_conditioner_direction[1]-0.5)/normalized))
    end_pos = (int(center[0]+arrow_length*(air_conditioner_direction[0]-0.5)/normalized), int(center[1]+arrow_length*(air_conditioner_direction[1]-0.5)/normalized))
    print(normalized)
    print(air_conditioner_direction[0], air_conditioner_direction[1])
    
    cv2.arrowedLine(background, start_pos, end_pos,
                    (0, 0, 0), 2, tipLength=0.5)



    cv2.putText(background, text, (70, 280),
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow('result', background)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
