import cv2
import mediapipe as mp
import numpy as np
import os
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
BG_COLOR = (192, 192, 192) # gray
dir = "./datas/sleep_with_quilt"
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
  for file in os.listdir(dir):
    
    image = cv2.imread(dir +'/'+ file)
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
      continue
    print(
        f'{file}: ('
        f'{results.pose_landmarks.landmark[23].x}, '
        f'{results.pose_landmarks.landmark[23].y}, '
        f'{results.pose_landmarks.landmark[23].visibility})'
    )
    print(results.segmentation_mask.shape)
    print(image_width, image_height)
    print(results.pose_landmarks.landmark[23].y)
    """
    print(
        results.segmentation_mask[int(results.pose_landmarks.landmark[23].y * image_height)][int(results.pose_landmarks.landmark[23].x * image_width)]
    )
    pos = (int(results.pose_landmarks.landmark[23].y * image_height), int(results.pose_landmarks.landmark[23].x * image_width))
    image = cv2.circle(image, pos, 100, (0,0,255), 0)
    """

    annotated_image = image.copy()
    # Draw segmentation on the image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    annotated_image = np.where(condition, annotated_image, bg_image)
    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite('./datas/results/' + file, annotated_image)
    # Plot pose world landmarks.
    """
    mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
    """