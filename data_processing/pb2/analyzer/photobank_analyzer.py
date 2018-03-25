#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import sys

import cv2
import numpy as np

class PhotobankAnalyzer:
    _FACE_DETECTION_MODEL_FILENAME = 'haarcascade_frontalface_default.xml'
    _FACE_DETECTION_MODEL_HOME = os.path.join(
        os.path.expanduser('~'), '.pb2_analyzer'        
    )
    _FACE_DETECTION_MODEL_URL = (
        'https://github.com/opencv/opencv/raw/master/data/haarcascades/' +
        _FACE_DETECTION_MODEL_FILENAME
    )
    _IMAGE_SCALE_FACTOR = 1.3
    _MIN_NEIGHBORS = 5
    
    @staticmethod
    def _download_model(filename):
        response = requests.get(
            PhotobankAnalyzer._FACE_DETECTION_MODEL_URL, stream = True
        )
        
        sys.stdout.write(
            'Downloading %s to %s... ' % (
                os.path.basename(filename), os.path.dirname(filename)
            )
        )
        
        with open(filename, 'wb') as o:
            for received_data in response.iter_content(chunk_size = 4096):
                o.write(received_data)
        
        sys.stdout.write('OK\n')
        sys.stdout.flush()
    
    def __init__(self):
        output_filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            PhotobankAnalyzer._FACE_DETECTION_MODEL_FILENAME
        )
        if os.path.isfile(output_filename):
            self._face_detector = cv2.CascadeClassifier(output_filename)
            return
        
        home_output_filename = os.path.join(
            PhotobankAnalyzer._FACE_DETECTION_MODEL_HOME,
            PhotobankAnalyzer._FACE_DETECTION_MODEL_FILENAME
        )
        if os.path.isfile(home_output_filename):
            self._face_detector = cv2.CascadeClassifier(home_output_filename)
            return
        
        try:
            PhotobankAnalyzer._download_model(output_filename)
            self._face_detector = cv2.CascadeClassifier(output_filename)
            return
        except PermissionError:
            pass
        
        base_dir = PhotobankAnalyzer._FACE_DETECTION_MODEL_HOME
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        elif not os.path.isdir(PhotobankAnalyzer._FACE_DETECTION_MODEL_HOME):
            raise FileExistsError(
                'Path %s is existing file' %
                (PhotobankAnalyzer._FACE_DETECTION_MODEL_HOME)
            )
        PhotobankAnalyzer._download_model(home_output_filename)
        self._face_detector = cv2.CascadeClassifier(home_output_filename)
    
    def analyze(self, rgb_image):
        rgb_array = np.array(rgb_image)
        if len(rgb_array.shape) > 2:
            grayscale_array = cv2.cvtColor(rgb_array, cv2.COLOR_BGR2GRAY)
        else:
            grayscale_array = rgb_array
        
        report_dict = {
            'height': grayscale_array.shape[0],
            'width': grayscale_array.shape[1],
            'faces': []
        }
        faces = self._face_detector.detectMultiScale(
            grayscale_array, PhotobankAnalyzer._IMAGE_SCALE_FACTOR,
            PhotobankAnalyzer._MIN_NEIGHBORS
        )
        if not isinstance(faces, tuple):
            report_dict['faces'] = faces.tolist()
        
        return report_dict
