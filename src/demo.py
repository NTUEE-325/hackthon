import cv2
import numpy as np
from gym import *
from utility import *
from constant import *
#from controller import *

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

init()


frame = 0
while cap.isOpened():
    cur_time = time.time()
    success, image = cap.read()
    h, w, _ = image.shape
    frame += 1
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.

    warning = False
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

    # clear not in picture chair
    if cur_time-last_detect_chair_time > buffer_time and (mode != "study"):
        chair_pos = 0
        chair_size = 0

    if results.pose_landmarks:

        posX, posY = get_body(results.pose_landmarks)

        if night_detect(image):

            last_time = cur_time

            if mode != "night":
                init_strength = air_conditioner_strength
                time_record[QUILT_COVER_TRUE_INDEX] = cur_time
                time_record[QUILT_COVER_FALSE_INDEX] = cur_time
                print("night mode")
                mode = "night"
                # SetMode("night")

            # detect if the quilt cover the body

            if (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].visibility > 0.8) or (
                    results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].visibility > 0.8):
                # no cover
                if quilt_cover:
                    record_dangerous_sleeping()
                    quilt_cover = False

                    time_record[QUILT_COVER_FALSE_INDEX] = cur_time
                    init_strength = air_conditioner_strength

                air_conditioner_strength = QUILT_COVER_MODE_BASE_STRENGTH + (init_strength-QUILT_COVER_MODE_BASE_STRENGTH)*math.exp(-(
                    cur_time-time_record[QUILT_COVER_FALSE_INDEX])/air_conditioner_strength_time_constant)
                warning = True
            else:  # cover
                if not quilt_cover:
                    time_record[QUILT_COVER_TRUE_INDEX] = cur_time
                    init_strength = air_conditioner_strength

                air_conditioner_strength = QUILT_COVER_MODE_BASE_STRENGTH + (init_strength-QUILT_COVER_MODE_BASE_STRENGTH)*math.exp(-(
                    cur_time-time_record[QUILT_COVER_TRUE_INDEX])/air_conditioner_strength_time_constant)

                quilt_cover = True

            air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                posX, posY)

        elif gym_detect(image, results.pose_landmarks, detect_times, mode):
            last_time = cur_time
            if mode != "gym":
                time_record[GYM_INDEX] = cur_time
                init_strength = air_conditioner_strength
                print("gym mode")
                mode = "gym"
                # SetMode("gym")
                print("gym:", gym_detect(
                    image, results.pose_landmarks, detect_times, mode))

            air_conditioner_direction = calculate_air_conditioner_direction(
                posX, posY)
            air_conditioner_strength = GYM_MODE_BASE_STRENGTH + (init_strength-GYM_MODE_BASE_STRENGTH)*math.exp(-(
                cur_time-time_record[GYM_INDEX])/air_conditioner_strength_time_constant)

        elif study_detect(results.pose_landmarks, chair_pos, chair_size):
            last_time = cur_time
            if mode != "study":
                print("study mode")
                # SetMode("study")
                mode = "study"

                time_record[STUDY_INDEX] = cur_time
                init_strength = air_conditioner_strength

            air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                posX, posY)

            if cur_time-time_record[STUDY_INDEX] < 10:
                air_conditioner_strength = init_strength + \
                    (cur_time-time_record[STUDY_INDEX])*(0.8-init_strength)/10
            else:
                air_conditioner_strength = 0.8+(STUDY_MODE_BASE_STRENGTH-0.8)*(1-math.exp(-(
                    cur_time-time_record[STUDY_INDEX]-10)/air_conditioner_strength_time_constant))

        else:
            if cur_time-last_time > buffer_time:
                if mode != "normal":
                    # SetMode("normal")
                    print("normal mode")
                    mode = "normal"

                    time_record[NORMAL_INDEX] = time.time()
                    init_strength = air_conditioner_strength

                air_conditioner_direction = calculate_air_conditioner_direction_inverse(
                    posX, posY)
                air_conditioner_strength = NORMAL_MODE_BASE_STRENGTH + (init_strength-NORMAL_MODE_BASE_STRENGTH)*math.exp(-(
                    cur_time-time_record[NORMAL_INDEX])/air_conditioner_strength_time_constant)
        theta_x, theta_y = get_fan_angle(
            air_conditioner_direction[0], air_conditioner_direction[1])
        # if frame % 40 == 0:
        #Set_Angle(theta_x, theta_y)
    else:
        results2 = objectron.process(image)

        if mode != "normal" and cur_time-last_time > buffer_time:
            # SetMode("normal")
            print("normal mode")
            mode = "normal"
            # SetMode(mode)
            # SetMode(mode)
            time_record[NORMAL_INDEX] = cur_time
            init_strength = air_conditioner_strength

        if mode == "normal":
            air_conditioner_strength = NORMAL_MODE_BASE_STRENGTH + (init_strength-NORMAL_MODE_BASE_STRENGTH)*math.exp(-(
                cur_time-time_record[NORMAL_INDEX])/air_conditioner_strength_time_constant)

        if results2.detected_objects:
            last_detect_chair_time = cur_time

            for detected_object in results2.detected_objects:
                mp_drawing.draw_landmarks(
                    image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                mp_drawing.draw_axis(image, detected_object.rotation,
                                     detected_object.translation)
                chair_pos = detected_object.landmarks_2d.landmark[0]

                chair_size = detected_object.scale
    # if frame % 40 == 0:
        # SetStrength(math.floor(air_conditioner_strength*5)+1)
    cv2.circle(
        image, (int(air_conditioner_direction[0]*w), int(air_conditioner_direction[1]*h)), 15, (255, 0, 0), -1)
    if results.pose_landmarks:
        cv2.circle(
            image, (int(get_body(results.pose_landmarks)[0]*w), int(get_body(results.pose_landmarks)[1]*h)), 15, (0, 255, 0), -1)
        text3 = str(air_conditioner_strength)
        cv2.putText(image, text3, (100, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow('MediaPipe Pose', image)

    background = cv2.imread("./img/background.jpg")
    draw_result(background, air_conditioner_direction, mode,
                math.floor(air_conditioner_strength*5)+1, warning)

    cv2.imshow('result', background)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
