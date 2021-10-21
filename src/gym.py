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


def detectPose(image, pose, display=True):
    '''
    This function performs pose detection on an image.
    Args:
        image: The input image with a prominent person whose pose landmarks needs to be detected.
        pose: The pose setup function required to perform the pose detection.
        display: A boolean value that is if set to true the function displays the original input image, the resultant image, 
                 and the pose landmarks in 3D plot and returns nothing.
    Returns:
        output_image: The input image with the detected pose landmarks drawn.
        landmarks: A list of detected landmarks converted into their original scale.
    '''

    # Create a copy of the input image.
    output_image = image.copy()

    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform the Pose Detection.
    results = pose.process(imageRGB)

    # Retrieve the height and width of the input image.
    height, width, _ = image.shape

    # Initialize a list to store the detected landmarks.
    landmarks = []

    # Check if any landmarks are detected.
    if results.pose_landmarks:

        # Draw Pose landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)

        # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:

            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                              (landmark.z * width)))

    # Check if the original input image and the resultant image are specified to be displayed.
    if display:

        # Display the original input image and the resultant image.
        plt.figure(figsize=[22, 22])
        plt.subplot(121)
        plt.imshow(image[:, :, ::-1])
        plt.title("Original Image")
        plt.axis('off')
        plt.subplot(122)
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')

        # Also Plot the Pose landmarks in 3D.
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    # Otherwise
    else:
        return output_image, landmarks


def calculateAngle(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

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


def classifyPose(landmarks, output_image, display=False):
    '''
    This function classifies yoga poses depending upon the angles of various body joints.
    Args:
        landmarks: A list of detected landmarks of the person whose pose needs to be classified.
        output_image: A image of the person with the detected pose landmarks drawn.
        display: A boolean value that is if set to true the function displays the resultant image with the pose label 
        written on it and returns nothing.
    Returns:
        output_image: The image with the detected pose landmarks drawn and pose label written.
        label: The classified pose label of the person in the output_image.

    '''

    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)

    # Calculate the required angles.
    # ----------------------------------------------------------------------------------------------------------------

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

    if left_elbow_angle > 155 and left_shoulder_angle < 30 and right_elbow_angle > 155 and right_shoulder_angle < 30:
        label = 'hands-down'

    if (left_elbow_angle < 90 or right_elbow_angle < 90) and (left_shoulder_angle < 30 and right_shoulder_angle < 30):
        label = 'hands-curl'

    '''print("left shoulder:", left_shoulder_angle)
    print("right shoulder:", right_shoulder_angle)
    print("left elbow", left_elbow_angle)
    print("right elbow", right_elbow_angle)'''

    return label


def gym_detect(landmarks, detect_times):
    # detect_times:
    # [0]: detect hands-curl
    # [1]: detect hands-down
    # [2]: detect push-up-up
    # [3]: detect push-up-down
    if landmarks:
        label = classifyPose(landmarks, display=True)
        if(label == "hands-curl"):
            detect_times[0] = time.time()
        if(label == "hands-down"):
            detect_times[1] = time.time()
        if(abs(detect_times[0]-detect_times[1]) < 5):
            dumbbell = True
        if(time.time()-detect_times[0] > 5 or time.time()-detect_times[1] > 5):
            dumbbell = False

        label = classifyPose(landmarks, display=True)
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


"""
# time detecting the action(dumbbell)
detect_time1 = time.time()
detect_time2 = 0
# boolean value detecting the gym actions
dumbbell = False

# time detecting the action
detect_time3 = time.time()
detect_time4 = 0
# boolean value detecting the gym actions
pushups = False


cap = cv2.VideoCapture(0)
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
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
        '''end = time.time()
        print(1/(end-start))'''

        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break

        output_image, landmarks = detectPose(image, pose, display=False)
        if landmarks:
            label = classifyPose(landmarks, output_image, display=True)
            if(label == "hands-curl"):
                detect_time1 = time.time()
            if(label == "hands-down"):
                detect_time2 = time.time()
            if(abs(detect_time2-detect_time1) < 5):
                dumbbell = True
            if(time.time()-detect_time1 > 5 or time.time()-detect_time2 > 5):
                dumbbell = False

            label = classifyPose(landmarks, output_image, display=True)
            if(label == "push-up-up"):
                detect_time3 = time.time()
            if(label == "push-up-down"):
                detect_time4 = time.time()
            if(abs(detect_time4-detect_time3) < 10):
                pushups = True
            if(time.time()-detect_time1 > 15 or time.time()-detect_time2 > 15):
                pushups = False

        if(pushups):
            print("push-up")
        elif(dumbbell):
            print("dumbbell")
        else:
            print("no detection")

cap.release()
"""
