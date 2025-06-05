import os
import numpy as np
import dlib
import cv2

# 文件路径
FEATURE_CSV_FILE = "C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\feature_centers.csv"
FACE_NUMBER_TXT_FILE = "C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\face_numbers.txt"
FACE_NAME_TXT_FILE = "C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\face_names.txt"

FEATURE_DIM = 128

# 加载Dlib模型
MODEL_DIR = "C:\\Users\\86178\\Desktop\\Personal_Moments-master\\model"
dlib_face_detector = dlib.get_frontal_face_detector()
dlib_cnn_face_detector = dlib.cnn_face_detection_model_v1(os.path.join(MODEL_DIR, "mmod_human_face_detector.dat"))
dlib_landmark_predictor = dlib.shape_predictor(os.path.join(MODEL_DIR, "shape_predictor_5_face_landmarks.dat"))
dlib_face_recognizor = dlib.face_recognition_model_v1(os.path.join(MODEL_DIR, "dlib_face_recognition_resnet_model_v1.dat"))

def initialize_files():
    """ 初始化文件，如果文件为空则填充初始内容 """
    # 确保 feature_centers.csv 不为空
    if not os.path.exists(FEATURE_CSV_FILE) or os.path.getsize(FEATURE_CSV_FILE) == 0:
        print(f"{FEATURE_CSV_FILE} is empty or does not exist. Initializing feature centers.")
        feature_centers = np.zeros((1, FEATURE_DIM))  # 1行，128列的零矩阵
        np.savetxt(FEATURE_CSV_FILE, feature_centers, delimiter=",")

    # 确保 face_numbers.txt 不为空
    if not os.path.exists(FACE_NUMBER_TXT_FILE) or os.path.getsize(FACE_NUMBER_TXT_FILE) == 0:
        with open(FACE_NUMBER_TXT_FILE, "w") as f:
            f.write("-1\n")  # 初始化时只有一个人

    # 确保 face_names.txt 不为空
    if not os.path.exists(FACE_NAME_TXT_FILE) or os.path.getsize(FACE_NAME_TXT_FILE) == 0:
        with open(FACE_NAME_TXT_FILE, "w") as f:
            f.write("MrNobody\n")  # 初始化时只有一个默认名字

initialize_files()