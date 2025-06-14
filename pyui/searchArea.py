from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(978, 284)
        Form.setToolTip("")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 904, 106))
        self.widget.setObjectName("widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        self.label_date = QtWidgets.QLabel(self.widget)
        self.label_date.setAlignment(QtCore.Qt.AlignCenter)
        self.label_date.setObjectName("label_date")
        self.verticalLayout_1.addWidget(self.label_date)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dateEdit_end = QtWidgets.QDateEdit(self.widget)
        self.dateEdit_end.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.dateEdit_end.setCalendarPopup(True)
        self.dateEdit_end.setObjectName("dateEdit_end")
        self.gridLayout_2.addWidget(self.dateEdit_end, 1, 1, 1, 1)
        self.label_end = QtWidgets.QLabel(self.widget)
        self.label_end.setAlignment(QtCore.Qt.AlignCenter)
        self.label_end.setObjectName("label_end")
        self.gridLayout_2.addWidget(self.label_end, 0, 1, 1, 1)
        self.dateEdit_start = QtWidgets.QDateEdit(self.widget)
        self.dateEdit_start.setToolTip("")
        self.dateEdit_start.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.dateEdit_start.setCalendarPopup(True)
        self.dateEdit_start.setObjectName("dateEdit_start")
        self.gridLayout_2.addWidget(self.dateEdit_start, 1, 0, 1, 1)
        self.label_start = QtWidgets.QLabel(self.widget)
        self.label_start.setAlignment(QtCore.Qt.AlignCenter)
        self.label_start.setObjectName("label_start")
        self.gridLayout_2.addWidget(self.label_start, 0, 0, 1, 1)
        self.verticalLayout_1.addLayout(self.gridLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout_1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_place = QtWidgets.QLabel(self.widget)
        self.label_place.setAlignment(QtCore.Qt.AlignCenter)
        self.label_place.setObjectName("label_place")
        self.verticalLayout_2.addWidget(self.label_place)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_province = QtWidgets.QLabel(self.widget)
        self.label_province.setAlignment(QtCore.Qt.AlignCenter)
        self.label_province.setObjectName("label_province")
        self.gridLayout_3.addWidget(self.label_province, 0, 0, 1, 1)
        self.label_city = QtWidgets.QLabel(self.widget)
        self.label_city.setAlignment(QtCore.Qt.AlignCenter)
        self.label_city.setObjectName("label_city")
        self.gridLayout_3.addWidget(self.label_city, 0, 1, 1, 1)
        self.label_district = QtWidgets.QLabel(self.widget)
        self.label_district.setAlignment(QtCore.Qt.AlignCenter)
        self.label_district.setObjectName("label_district")
        self.gridLayout_3.addWidget(self.label_district, 0, 2, 1, 1)
        self.comboBox_province = QtWidgets.QComboBox(self.widget)
        self.comboBox_province.setObjectName("comboBox_province")
        self.gridLayout_3.addWidget(self.comboBox_province, 1, 0, 1, 1)
        self.comboBox_city = QtWidgets.QComboBox(self.widget)
        self.comboBox_city.setObjectName("comboBox_city")
        self.gridLayout_3.addWidget(self.comboBox_city, 1, 1, 1, 1)
        self.comboBox_district = QtWidgets.QComboBox(self.widget)
        self.comboBox_district.setObjectName("comboBox_district")
        self.gridLayout_3.addWidget(self.comboBox_district, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_people = QtWidgets.QLabel(self.widget)
        self.label_people.setEnabled(True)
        self.label_people.setAlignment(QtCore.Qt.AlignCenter)
        self.label_people.setObjectName("label_people")
        self.verticalLayout_3.addWidget(self.label_people)
        self.label_m1 = QtWidgets.QLabel(self.widget)
        self.label_m1.setEnabled(False)
        self.label_m1.setText("")
        self.label_m1.setObjectName("label_m1")
        self.verticalLayout_3.addWidget(self.label_m1)
        self.lineEdit_people = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_people.setObjectName("lineEdit_people")
        self.verticalLayout_3.addWidget(self.lineEdit_people)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_thing = QtWidgets.QLabel(self.widget)
        self.label_thing.setAlignment(QtCore.Qt.AlignCenter)
        self.label_thing.setObjectName("label_thing")
        self.verticalLayout_4.addWidget(self.label_thing)
        self.label_m2 = QtWidgets.QLabel(self.widget)
        self.label_m2.setEnabled(False)
        self.label_m2.setText("")
        self.label_m2.setObjectName("label_m2")
        self.verticalLayout_4.addWidget(self.label_m2)
        self.lineEdit_thing = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_thing.setEnabled(True)
        self.lineEdit_thing.setObjectName("lineEdit_thing")
        self.verticalLayout_4.addWidget(self.lineEdit_thing)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.pushButton_search = QtWidgets.QPushButton(self.widget)
        self.pushButton_search.setObjectName("pushButton_search")
        self.horizontalLayout.addWidget(self.pushButton_search)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.image_area = QtWidgets.QWidget(self.widget)
        self.image_area.setObjectName("image_area")
        self.verticalLayout_6.addWidget(self.image_area)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.dateEdit_start, self.dateEdit_end)
        Form.setTabOrder(self.dateEdit_end, self.comboBox_province)
        Form.setTabOrder(self.comboBox_province, self.comboBox_city)
        Form.setTabOrder(self.comboBox_city, self.comboBox_district)
        Form.setTabOrder(self.comboBox_district, self.lineEdit_people)
        Form.setTabOrder(self.lineEdit_people, self.lineEdit_thing)
        Form.setTabOrder(self.lineEdit_thing, self.pushButton_search)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_date.setText(_translate("Form", "Date"))
        self.label_end.setText(_translate("Form", "End Date"))
        self.label_start.setText(_translate("Form", "Start Date"))
        self.label_place.setText(_translate("Form", "Place"))
        self.label_province.setText(_translate("Form", "Province"))
        self.label_city.setText(_translate("Form", "City"))
        self.label_district.setText(_translate("Form", "District"))
        self.label_people.setText(_translate("Form", "People"))
        self.lineEdit_people.setPlaceholderText(_translate("Form", "Enter person name"))
        self.label_thing.setText(_translate("Form", "Thing"))
        self.lineEdit_thing.setPlaceholderText(_translate("Form", "Enter thing name"))
        self.pushButton_search.setText(_translate("Form", "Search"))


