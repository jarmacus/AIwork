import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout, QWidget
from PIL import Image
import sqlite3

from classification import classify_image
from predict import predictting
from utils.date_utils import get_time_stamp
from utils.gps_utils import get_gps_info, get_address_from_gps
from utils.face_utils import get_face_features, load_face_names, save_feature_centers, save_face_numbers, \
    save_face_names, load_feature_centers, load_face_numbers

# 定义人脸特征的维度
FEATURE_DIM = 128  # 例如，dlib 提取的人脸特征是128维的

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1003, 534)

        # 布局设置
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 11, 981, 511))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 导入说明文本（HTML）
        self.textBrowser_import_intro = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_import_intro.setObjectName("textBrowser_import_intro")
        self.textBrowser_import_intro.setMaximumHeight(250)
        self.verticalLayout.addWidget(self.textBrowser_import_intro)

        # 设置 HTML 内容
        self.textBrowser_import_intro.setHtml("""
        <html><head><meta name="qrichtext" content="1" /><style type="text/css">
        p, li { white-space: pre-wrap; }
        </style></head><body style=" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;">
        <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
        <span style=" font-size:18pt; font-weight:600;">如何使用</span></p>
        <p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">
        <span style=" font-size:12pt;">在浏览照片之前，你需要首先导入照片并对其进行处理。等待照片处理任务完成后，重启应用，你就可以随意所欲的浏览和查找照片了。</span></p>
        </body></html>""")

        # 按钮布局
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_import = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_import.setObjectName("pushButton_import")
        self.horizontalLayout.addWidget(self.pushButton_import)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_process = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_process.setObjectName("pushButton_process")
        self.horizontalLayout.addWidget(self.pushButton_process)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # 地址展示区
        self.address_label = QLabel(self.layoutWidget)
        self.address_label.setObjectName("address_label")
        self.verticalLayout.addWidget(self.address_label)

        # 进度条
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 绑定事件
        self.pushButton_import.clicked.connect(self.import_photos)  # 导入照片
        self.pushButton_process.clicked.connect(self.process_photos)  # 处理照片

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_import.setText(_translate("Form", "Import"))
        self.pushButton_process.setText(_translate("Form", "Process"))

    def import_photos(self):
        # 选择文件夹
        folder = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder:
            print(f"Selected folder: {folder}")
            self.process_photos_and_save_to_db(folder)
        else:
            print("No folder selected!")

    def process_photos(self):
        print("Processing photos...")
        self.progressBar.setValue(0)  # 设置进度条初始值

    def process_photos_and_save_to_db(self, input_dir, db_file="C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\info.db"):
        print("Processing photos...")
        """
        处理照片并将提取的信息存入数据库。

        :param input_dir: 图像文件夹路径
        :param db_file: 数据库文件路径
        """
        # 连接数据库
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # 获取所有图片
        image_list = self.get_all_images(input_dir)
        total_images = len(image_list)

        # 用于展示的地址信息
        address_info = []

        #获取人脸特征矩阵和人脸名称
        feature_centers = load_feature_centers() if os.path.exists(
            "C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\feature_centers.csv") else np.zeros((0, FEATURE_DIM))
        print("1:",np.shape(feature_centers))
        face_numbers = load_face_numbers() if os.path.exists(
            "C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\face_numbers.txt") else []

        face_names = load_face_names() if os.path.exists(
            "C:\\Users\\86178\\Desktop\\Personal_Moments-master\\record\\face_names.txt") else []

        # 遍历图片，提取信息并保存到数据库
        for idx, image_file in enumerate(image_list):
            try:
                #查重
                from imagededup.methods import PHash
                from imagededup.utils import plot_duplicates

                # 初始化PHash方法
                phasher = PHash()

                # 生成所有图像的编码
                encodings = phasher.encode_images(image_dir=input_dir)

                # 查找重复图像
                duplicates = phasher.find_duplicates(encoding_map=encodings)
                print("原始重复字典：", duplicates)

                if duplicates:
                    # 创建一个新的字典来存储最终去重后的重复项
                    deduplicated = {}

                    # 遍历原始重复字典
                    for key, duplicate_list in list(duplicates.items()):
                        if key not in deduplicated:
                            # 如果key没有出现在去重字典中，保留当前key和对应的重复项
                            deduplicated[key] = duplicate_list
                        else:
                            # 如果key已经在去重字典中，直接跳过这个重复的key
                            continue

                    # 输出去重后的字典
                    print("去重后的duplicates字典：", deduplicated)

                    # 使用一个list存储所有需要删除的图片
                    keys_to_delete = []

                    # 删除重复文件并更新字典
                    for key, duplicate_list in list(deduplicated.items()):
                        # 对于每个key及其重复项
                        for duplicate in duplicate_list:
                            # 拼接正确的路径
                            duplicate_path = os.path.join(input_dir, duplicate)

                            # 确保文件存在
                            if os.path.exists(duplicate_path):
                                try:
                                    # 删除文件
                                    os.remove(duplicate_path)
                                    print(f"删除重复文件: {duplicate_path}")

                                    # 删除文件后，标记重复项已删除
                                    if duplicate in deduplicated[key]:
                                        deduplicated[key].remove(duplicate)
                                        print("更新后的deduplicated字典:", deduplicated)

                                    # 如果当前key的重复项为空，删除该key
                                    if not deduplicated[key]:
                                        keys_to_delete.append(key)

                                except Exception as e:
                                    print(f"无法删除文件 {duplicate_path}，错误：{e}")
                    # 删除需要删除的key
                    for key in keys_to_delete:
                        del deduplicated[key]

                    # 输出最终去重后的字典
                    print("最终去重后的deduplicated字典：", deduplicated)
                #
                # 证件识别
                # top5 = predictting(image_file)
                # print("top5",top5)
                top5 = ""
                # 1. 提取日期
                print("1")
                date = get_time_stamp(image_file)
                # 2. 提取GPS信息
                gps_info = get_gps_info(image_file)
                # print(gps_info)
                if gps_info:
                    address = get_address_from_gps(gps_info, api_key="P45BZ-BDOLB-BHZUL-J5HNR-ARGTQ-M3BOP", secret_key="MeJhLJviXGWE94LKewZtVtpoiFeLRlNW")
                    province, city, district = address.get('province', 'Unknown'), address.get('city', 'Unknown'), address.get('district', 'Unknown')
                else:
                    province, city, district = 'Unknown', 'Unknown', 'Unknown'

                # 3. 提取人脸信息
                method = "dlib"  # 或 "dlib_cnn" 使用CNN检测更精确但速度慢
                face_features = get_face_features(image_file, method=method)
                people = None
                if face_features:
                    # 假设每张图片只有一个人脸，添加人脸名称
                    people = f"Person_{len(face_names)+1}"  # 这里确保 len(face_features[1]) 获取到特征的数量
                    print(f"Detected face(s) in {image_file}: {people}")

                    # 更新人脸特征矩阵，人数和名称
                    for feature in face_features[1]:  # face_features[1] 包含所有的人脸特征
                        feature = feature.reshape(1, -1)
                        print("feature:",np.shape(feature))
                        if feature_centers is None or feature_centers.shape[0] == 0:
                            # 如果 feature_centers 是空的，则直接设置它
                            print("No existing feature centers. Adding the first feature.")
                            feature_centers = np.array([feature])
                        else:
                            # 更新特征矩阵、人数和名称
                            print("feature_centers:",np.shape(feature_centers))
                            feature_centers, face_numbers, face_names = self.update_feature_data(feature_centers,
                                                                                                 face_numbers,
                                                                                                 face_names, feature)

                    # 保存到csv和txt文件
                    print("Saving feature centers, face numbers, and names.")
                    save_feature_centers(feature_centers)
                    save_face_numbers(face_numbers)
                    save_face_names(face_names)

                #图像识别
                image_name_thing = classify_image(input_dir,image_file)

                # 4. 将提取的地址信息保存到数据库
                self.insert_data_to_db(cursor, image_file, date, province, city, district, people,image_name_thing,top5)

                # 添加地址信息
                address_info.append(f"{image_file}: {province}, {city}, {district}")

                # 更新进度条
                progress = (idx + 1) * 100 // total_images
                self.progressBar.setValue(progress)

            except Exception as e:
                print(f"Error processing {image_file}: {e}")

        # 提交更改并关闭连接
        conn.commit()
        conn.close()

        # 显示地址信息
        self.display_address(address_info)

    def insert_data_to_db(self, cursor, image_file, date, province, city, district, people,image_name_thing,top5):
        """
        将提取的数据插入到数据库中的相应表格。

        :param cursor: sqlite3 cursor 对象
        :param image_file: 图像文件路径
        :param date: 图像创建日期
        :param province: 省份
        :param city: 城市
        :param district: 区县
        :param people: 识别出的人物（如果有）
        """
        cursor.execute("INSERT OR IGNORE INTO Date (image_file) VALUES (?)", (image_file,))
        cursor.execute("INSERT OR IGNORE INTO Place (image_file) VALUES (?)", (image_file,))
        cursor.execute("INSERT OR IGNORE INTO Thing (image_file) VALUES (?)", (image_file,))
        cursor.execute("INSERT OR IGNORE INTO Top5 (image_file) VALUES (?)", (image_file,))
        # 如果识别到人物信息，将人物数据插入 People 表
        if people:
            cursor.execute("INSERT OR IGNORE INTO People (image_file) VALUES (?)", (image_file,))
            print(people)

        cursor.execute(
            "INSERT OR REPLACE INTO Summary (image_file, create_date, province, city, district, person,image_name_thing,top5) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (image_file, date, province, city, district, people, image_name_thing, top5))

        cursor.connection.commit()

    def display_address(self, address_info):
        """将地址信息显示到界面上"""
        if address_info:
            self.address_label.setText("\n".join(address_info))
        else:
            self.address_label.setText("No addresses found.")

    def get_all_images(self, input_dir):
        """
        遍历获取输入文件夹内的所有图像文件。
        Traverse specific directory to get all images in it.

        :param input_dir: str, input directory
        :return image_list: list, image list
        """
        image_list = []
        results = os.walk(input_dir)
        for result in results:
            dir_path, _, image_files = result
            for image_file in image_files:
                try:
                    # 使用Pillow检查是否为图像文件
                    with Image.open(os.path.join(dir_path, image_file)) as img:
                        image_list.append(os.path.join(dir_path, image_file))
                except:
                    continue
        return image_list

    def update_feature_data(self, feature_centers, face_numbers, face_names, feature):
        """
        更新特征矩阵、人数和名称的函数。
        :param feature_centers: 人脸特征矩阵
        :param face_numbers: 每张人脸对应的数量
        :param face_names: 人脸名称列表
        :param feature: 当前图片的人脸特征
        :return: 更新后的特征矩阵、人数和名称
        """
        distance_threshold = 0.2
        found = False
        # 确保 feature 是二维数组，形状为 (1, FEATURE_DIM)
        # feature = feature.reshape(1, -1)  # 确保 feature 维度是 (1, FEATURE_DIM)
        print(np.shape(feature_centers))
        # 对比现有的所有人脸特征矩阵
        for i, center in enumerate(feature_centers):
            center = center.reshape(-1, 128)
            print(f"Comparing {i}-th center with feature:", center.shape, feature.shape)
            dist = np.sum((center - feature) ** 2)  # 计算欧氏距离
            print("Distance:", dist)
            if dist < distance_threshold:
                # 如果距离小于阈值，则认为是同一个人
                face_numbers[i] += 1
                found = True
                break

        if not found:
            # 如果没有找到相似的人脸，则添加新的人脸特征
            print("No matching faces found. Adding a new face.")
            feature_centers = np.append(feature_centers, feature, axis=0)  # 将新的人脸特征添加到矩阵
            face_numbers.append(1)
            face_names.append(f"Person_{len(face_names) + 1}")

        return feature_centers, face_numbers, face_names


