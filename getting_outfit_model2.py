import numpy as np
import matplotlib.pyplot as plt
import json
import os
import cv2
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import roboflow
from ultralytics import YOLO
from roboflow import Roboflow
import torch





def get_labels_probability(paths: List[str]) -> dict:

  """
  Get labels and their associated probabilities from model predictions for a list of images.

  :param path: list of paths to images for which predictions are to be made.
  :return: a dictionary with probability, class names and path to correspending images.
  """

  labels_from_images = []
  detected_objects = dict()

  for image in paths:

    labels = model.predict(image)
    results = labels[0]
    boxes = results.boxes

    if boxes is not None:
      probabilities = boxes.conf
      class_ids = boxes.cls
      names = results.names

      detected_objects[image] = {}

      for i in range(len(probabilities)):

        prob = probabilities[i].item()
        class_id = int(class_ids[i].item())
        class_name = names[class_id]

        if (not detected_objects[image]) or (prob > detected_objects[image].get('prob', 0)):
          detected_objects[image]['prob'] = prob
          detected_objects[image]['class_name'] = class_name
          detected_objects[image]['class_id'] = class_id

    return detected_objects

def preprocess_image(image_path: str, target_size: tuple =(640, 640), apply_preprocessing: bool=True) -> torch.tensor:

  """
  Preprocess an image for model input.

  :param image_path: path to the image file to preprocess.
  :param target_size: the desired size to which the image will be resized (default is (640, 640)).
  :param apply_preprocessing: a boolean indicating whether to pply CLAHE preprocessing.
  :return: a tensor representation of the preprocessed image.
  """

  image = cv2.imread(image_path)

  if image is None:
    raise ValueError(f"Error: Could not read image from path: {image_path}")

  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  if not apply_preprocessing:
    input_tensor = torch.tensor(image_rgb).permute(2, 0, 1).float() / 255.0

  height, width = image_rgb.shape[:2]
  new_width = (width // 32 + 1) * 32
  new_height = (height // 32 + 1) * 32
  resized_image = cv2.resize(image_rgb, (new_width, new_height))

  lab_image = cv2.cvtColor(resized_image, cv2.COLOR_RGB2LAB)
  l_channel, a_channel, b_channel = cv2.split(lab_image)

  clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(3,3))
  l_channel = clahe.apply(l_channel)

  enhanced_lab_image = cv2.merge((l_channel, a_channel, b_channel))
  clahe_image = cv2.cvtColor(enhanced_lab_image, cv2.COLOR_LAB2RGB)

  input_tensor = torch.tensor(clahe_image).permute(2, 0, 1).float() / 255.0

  return input_tensor.unsqueeze(0)

def get_best_detection(boxes: Optional[Any], names: List[str]) -> Optional[Dict[str, Any]:

    """
    Finds the best detection from a list of bounding boxes based on confidence scores.

    param boxes : a set of bounding boxes with associated data.
           This have to be an object like the 'boxes' attribute from a YOLO result.
           It can also be None if no detections are present.
    param names: a list of class names corresponding to the class IDs.
    return: a dictionary containing the best detection information
        (probability, class name, class ID) if detections are available.
        If no detections are found, returns None.
    """

  if boxes is None or len(boxes) == 0:

    return None

  probabilities = boxes.conf
  class_ids = boxes.cls
  best_detection = None
  max_prob = -1

  for i in range(len(probabilities)):

    prob = probabilities[i].item()

    if prob > max_prob:
      max_prob = prob
      class_id = int(class_ids[i].item())
      class_name = names[class_id]
      best_detection = {'prob': prob, 'class_name': class_name, 'class_id': class_id}

  return best_detection

def process_and_compare(image_path: str) -> dict:

  """
  Processes an image using preprocessing and without preprocessing
  and returns the best detection based on confidence scores.


  param image_path: the path to the image to be processed.

  return: a dictionary containing the information of the best
  detection after comparing results with preprocessing and without it.
  Returns None if no detections are found in both cases.
  """

  preprocessed_image = preprocess_image(image_path)

  results_processed = model.predict(source=preprocessed_image, save=True)
  results_unprocessed = model.predict(source=image_path)

  processed_boxes = results_processed[0].boxes if len(results_processed) > 0 else None
  unprocessed_boxes = results_unprocessed[0].boxes if len(results_unprocessed) > 0 else None

  names = results_processed[0].names if len(results_processed) > 0 else (results_unprocessed[0].names if len(results_unprocessed) > 0 else [])

  best_processed = get_best_detection(processed_boxes, names)
  best_unprocessed = get_best_detection(unprocessed_boxes, names)

  if best_processed is None and best_unprocessed is None:
      return None
  elif best_processed is None:
      return best_unprocessed
  elif best_unprocessed is None:
      return best_processed
  elif best_processed['prob'] > best_unprocessed['prob']:
      return best_processed
  else:
      return best_unprocessed

if __name__ == '__main__':

    images = ['/content/test2.jpg', '/content/test_2.jpg', '/content/test_3.jpg', '/content/test_4.jpg']

    detected_objects = []

    for img in images:
        result = process_and_compare(img)
        detected_objects.append(result)

    print(detected_objects)
