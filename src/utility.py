import cv2
import mediapipe as mp
import math
import time
mp_pose = mp.solutions.pose

LIGHT_THRESHOLD = 100
OBSERVE_DISTANCE_TO_IMAGE = 0.5

# calculate the fan's angle according to the positions
# obtained from the demo.py.


def get_fan_angle(posX, posY):
    return int(math.atan((posX-0.5)/OBSERVE_DISTANCE_TO_IMAGE)*180/math.pi+90), int(math.atan((posY-0.5)/OBSERVE_DISTANCE_TO_IMAGE)*180/math.pi+90)


def get_body(pose_landmarks):

    x = (pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x +
         pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x +
         pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x +
         pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x) / 4
    y = (pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y +
         pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y +
         pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y +
         pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y) / 4
    return (x, y)


def night_detect(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lightness = hsv_image[:, :, 2].mean()
    if lightness < LIGHT_THRESHOLD:
        return True
    return False


def study_detect(pose_landmarks, chair_pos, chair_size):
    if chair_pos == 0:
        return False
    posX, posY = get_body(pose_landmarks)
    #print(posX, posY)
    #print(chair_pos, chair_size)
    if chair_pos.x-(chair_size[0]) < posX and posX < chair_pos.x+(chair_size[0]):
        if chair_pos.y - (chair_size[1]) < posY and posY < chair_pos.y+(chair_size[1]):
            # print("study")
            return True
    return False

# air conditioner direction not on people


def calculate_air_conditioner_direction_inverse(posX, posY):
    distance = math.sqrt(math.pow((0.5-posX), 2)+math.pow((0.5-posY), 2))
    distance = 0.5-distance
    norm_vector_x = (0.5-posX)/(0.5-distance)
    norm_vector_y = (0.5-posY)/(0.5-distance)
    return 0.5+norm_vector_x*distance, 0.5+norm_vector_y*distance

# air conditioner direction on people


def calculate_air_conditioner_direction(posX, posY):
    return posX, posY


def record_dangerous_sleeping():
    sleepHistory = open("./data/SleepHistory.txt", "a")
    sleepHistory.write(time.time())
    sleepHistory.close()
