import mediapipe as mp
mp_pose = mp.solutions.pose
import cv2

LIGHT_THRESHOLD = 200

def get_body(pose_landmarks):
    x = pose_landmarks[mp_pose.PoseLandmark.LEFT_HIP].x + pose_landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x
    y = pose_landmarks[mp_pose.PoseLandmark.LEFT_HIP].y + pose_landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y
    return (x,y)

def night_detect(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lightness = hsv_image[:,:,2].mean()
    if lightness < LIGHT_THRESHOLD:
        return True
    return False