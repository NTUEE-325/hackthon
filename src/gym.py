import math
import cv2
import numpy as np
import time
import mediapipe as mp
import matplotlib.pyplot as plt
mp_drawing_styles = mp.solutions.drawing_styles

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose

# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True,
                    min_detection_confidence=0.3, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils


def calculateAngle(landmark1, landmark2, landmark3):

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))

    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360

    if angle > 180:
        angle = 360-angle
    # Return the calculated angle.
    return angle


def classifyPose(landmarks, landmarks_visibility):
    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)

    # Calculate the required angles.
    # ----------------------------------------------------------------------------------------------------------------
    # print(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].visibility)
    # Get the angle between the left shoulder, elbow and wrist points.
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    # Get the angle between the right shoulder, elbow and wrist points.
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

    # Get the angle between the left elbow, shoulder and hip points.
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points.
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points.
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    # first check whether the body is in the scope.

    enable_detection_dumbbell = (landmarks_visibility[mp_pose.PoseLandmark.LEFT_SHOULDER.value] > 0.8 and landmarks_visibility[mp_pose.PoseLandmark.LEFT_ELBOW.value] > 0.8) or (
        landmarks_visibility[mp_pose.PoseLandmark.RIGHT_SHOULDER.value] > 0.8 and landmarks_visibility[mp_pose.PoseLandmark.RIGHT_ELBOW.value] > 0.8)
    enable_detection_pushup = (landmarks_visibility[mp_pose.PoseLandmark.LEFT_SHOULDER.value] > 0.8 and landmarks_visibility[mp_pose.PoseLandmark.LEFT_ELBOW.value] > 0.8) or (
        landmarks_visibility[mp_pose.PoseLandmark.RIGHT_SHOULDER.value] > 0.8 and landmarks_visibility[mp_pose.PoseLandmark.RIGHT_ELBOW.value] > 0.8) and (
        landmarks_visibility[mp_pose.PoseLandmark.RIGHT_HIP.value] > 0.8 and landmarks_visibility[mp_pose.PoseLandmark.LEFT_HIP.value] > 0.8) and (
        landmarks_visibility[mp_pose.PoseLandmark.RIGHT_KNEE.value] > 0.8 and landmarks_visibility[mp_pose.PoseLandmark.LEFT_KNEE.value] > 0.8)

    if enable_detection_pushup:
        if left_elbow_angle < 40 and right_elbow_angle < 40:
            if left_shoulder_angle < 30 and right_shoulder_angle < 30:
                if left_knee_angle > 155 and right_knee_angle > 155:
                    if left_hip_angle > 155 and right_hip_angle > 155:
                        label = 'push-up-down'

        if left_elbow_angle > 150 and right_elbow_angle > 150:
            if left_shoulder_angle > 70 and right_shoulder_angle > 70:
                if left_knee_angle > 155 and right_knee_angle > 155:
                    if left_hip_angle > 155 and right_hip_angle > 155:
                        label = 'push-up-up'

    if enable_detection_dumbbell:
        if left_elbow_angle > 155 and left_shoulder_angle < 30 and right_elbow_angle > 155 and right_shoulder_angle < 30:
            label = 'hands-down'

        if (left_elbow_angle < 70 or right_elbow_angle < 70) and (left_shoulder_angle < 30 and right_shoulder_angle < 30):
            label = 'hands-curl'

        if (left_elbow_angle < 70 and right_elbow_angle < 70) and (left_shoulder_angle < 30 and right_shoulder_angle < 30):
            label = 'hands-double-curl'
    return label


def gym_detect(image, results_pose_landmarks, detect_times):
    # detect_times:
    # [0]: detect hands-curl
    # [1]: detect hands-down
    # [2]: detect push-up-up
    # [3]: detect push-up-down
    # [4]: detect hands-double-curl: the mode dumbbell should start by the curl with both hands pose

    # unnormalized

    height, width, _ = image.shape
    landmarks = []

    landmarks_visibility = []

    if results_pose_landmarks:
        for landmark in results_pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                              (landmark.z * width)))
            landmarks_visibility.append(landmark.visibility)

    if landmarks:
        label = classifyPose(landmarks, landmarks_visibility)
        if(label == "hands-curl"):
            detect_times[0] = time.time()
        if(label == "hands-down"):
            detect_times[1] = time.time()
        if(label == "hands-double-curl"):
            detect_times[4] = time.time()
        if(abs(detect_times[4]-detect_times[1]) < 5):
            dumbbell = True
        if(time.time()-detect_times[0] > 5 or time.time()-detect_times[1] > 5 or time.time()-detect_times[4] > 5):
            dumbbell = False

        label = classifyPose(landmarks, landmarks_visibility)
        if(label == "push-up-up"):
            detect_times[2] = time.time()
        if(label == "push-up-down"):
            detect_times[3] = time.time()
        if(abs(detect_times[3]-detect_times[2]) < 10):
            pushups = True
        if(time.time()-detect_times[2] > 15 or time.time()-detect_times[3] > 15):
            pushups = False

        if(pushups):
            return "push-up"
        elif(dumbbell):
            return "dumbbell"
        else:
            return False
    return False
