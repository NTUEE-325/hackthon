import cv2
import mediapipe as mp
import numpy as np
from gym import *
from utility import *
from constant import *
# from controller import *
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

cap = cv2.VideoCapture(0)


sleepHistory = open("./data/SleepHistory.txt", 'x')

while cap.isOpened():
    cur_time = time.time()
    success, image = cap.read()
    h, w, _ = image.shape

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.flip(image, 1)
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
                # SetMode("night")

            # detect if the quilt cover the body
            quilt_cover = True
            if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility > 0.8 or results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].visibility > 0.8:
                # send signal
                if quilt_cover:
                    record_dangerous_sleeping()
                    quilt_cover = False

                    time_record = np.zeros(5)
                    time_record[QUILT_COVER_FALSE_INDEX] = time.time()
                    init_strength = air_conditioner_strength

                air_conditioner_strength = QUILT_COVER_MODE_BASE_STRENGTH + (init_strength-QUILT_COVER_MODE_BASE_STRENGTH)*math.exp(-(
                    time.time()-time_record[QUILT_COVER_FALSE_INDEX])/air_conditioner_strength_time_constant)

                # send to arduino (direction_x, direction_y)
            else:
                if quilt_cover:
                    time_record = np.zeros(5)
                    time_record[QUILT_COVER_TRUE_INDEX] = time.time()
                    init_strength = air_conditioner_strength

                    air_conditioner_strength = QUILT_NOT_COVER_MODE_BASE_STRENGTH + (init_strength-QUILT_NOT_COVER_MODE_BASE_STRENGTH)*math.exp(-(
                        time.time()-time_record[QUILT_COVER_FALSE_INDEX])/air_conditioner_strength_time_constant)
                quilt_cover = True

            air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                posX, posY)

        elif gym_detect(image, results.pose_landmarks, detect_times):
            # send signal
            last_time = time.time()
            if mode != "gym":
                time_record = np.zeros(5)
                time_record[GYM_INDEX] = time.time()
                init_strength = air_conditioner_strength
                print("gym mode")
                mode = "gym"
                # SetMode("gym")
                print("gym:", gym_detect(
                    image, results.pose_landmarks, detect_times))

                '''sleepHistory = open("../data/SleepHistory.txt", "a")
                sleepHistory.write(
                    str(time.asctime(time.localtime(time.time())))+'\n')
                sleepHistory.close()'''

            air_conditioner_direction = calculate_air_conditioner_direction(
                posX, posY)
            air_conditioner_strength = GYM_MODE_BASE_STRENGTH + (init_strength-GYM_MODE_BASE_STRENGTH)*math.exp(-(
                time.time()-time_record[GYM_INDEX])/air_conditioner_strength_time_constant)

        elif study_detect(results.pose_landmarks, chair_pos, chair_size):
            last_time = time.time()
            if mode != "study":
                print("study mode")
                # SetMode("study")
                mode = "study"

                time_record = np.zeros(5)
                time_record[STUDY_INDEX] = time.time()
                init_strength = air_conditioner_strength

            air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                posX, posY)
            air_conditioner_strength = STUDY_MODE_BASE_STRENGTH + (init_strength-STUDY_MODE_BASE_STRENGTH)*math.exp(-(
                time.time()-time_record[STUDY_INDEX])/air_conditioner_strength_time_constant)

        else:
            if cur_time-last_time > buffer_time:
                if mode != "normal":
                    # SetMode("normal")
                    print("normal mode")
                    mode = "normal"
                    time_record = np.zeros(5)
                    time_record[NORMAL_INDEX] = time.time()
                    init_strength = air_conditioner_strength

                air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                    posX, posY)
                air_conditioner_strength = NORMAL_MODE_BASE_STRENGTH + (init_strength-NORMAL_MODE_BASE_STRENGTH)*math.exp(-(
                    time.time()-time_record[NORMAL_INDEX])/air_conditioner_strength_time_constant)
                # print("normal")
                # send normal signal to arduino

    else:
        results2 = objectron.process(image)
        if results2.detected_objects:
            last_detect_chair_time = time.time()
            if mode != "normal":
                # SetMode("normal")
                print("normal mode")
                mode = "normal"
                time_record = np.zeros(5)
                time_record[NORMAL_INDEX] = time.time()
                init_strength = air_conditioner_strength

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

    # text3 = 'fps:' + str(fps)
    # cv2.putText(image, text3, (100, 150), cv2.FONT_HERSHEY_SIMPLEX,
    # 1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.circle(
        image, (int(air_conditioner_direction[0]*w), int(air_conditioner_direction[1]*h)), 15, (255, 0, 0), -1)
    if results.pose_landmarks:
        cv2.circle(
            image, (int(get_body(results.pose_landmarks)[0]*w), int(get_body(results.pose_landmarks)[1]*h)), 15, (0, 255, 0), -1)
        text3 = str(air_conditioner_strength)
        cv2.putText(image, text3, (100, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow('MediaPipe Pose', image)

    background = cv2.imread("./img/background.jpg")

    draw_result(background, air_conditioner_direction, mode,
                math.floor(air_conditioner_strength*5)+1)

    cv2.imshow('result', background)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
