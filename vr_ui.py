# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\OneDrive\Documents\workspace\python\video-flip\vr_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(536, 373)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.inputGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.inputGroup.setObjectName("inputGroup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.inputGroup)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.input_filePath = QtWidgets.QLineEdit(self.inputGroup)
        self.input_filePath.setMinimumSize(QtCore.QSize(200, 0))
        self.input_filePath.setObjectName("input_filePath")
        self.gridLayout_3.addWidget(self.input_filePath, 0, 1, 1, 1)
        self.input_ud_180 = QtWidgets.QRadioButton(self.inputGroup)
        self.input_ud_180.setObjectName("input_ud_180")
        self.gridLayout_3.addWidget(self.input_ud_180, 3, 1, 1, 1)
        self.input_lr_fisheye = QtWidgets.QRadioButton(self.inputGroup)
        self.input_lr_fisheye.setObjectName("input_lr_fisheye")
        self.gridLayout_3.addWidget(self.input_lr_fisheye, 4, 1, 1, 1)
        self.input_lr_180 = QtWidgets.QRadioButton(self.inputGroup)
        self.input_lr_180.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.input_lr_180.setChecked(True)
        self.input_lr_180.setAutoExclusive(True)
        self.input_lr_180.setObjectName("input_lr_180")
        self.gridLayout_3.addWidget(self.input_lr_180, 2, 1, 1, 1)
        self.input_ud_360 = QtWidgets.QRadioButton(self.inputGroup)
        self.input_ud_360.setObjectName("input_ud_360")
        self.gridLayout_3.addWidget(self.input_ud_360, 3, 2, 1, 1)
        self.input_lr_360 = QtWidgets.QRadioButton(self.inputGroup)
        self.input_lr_360.setObjectName("input_lr_360")
        self.gridLayout_3.addWidget(self.input_lr_360, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.inputGroup)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.browseBtn = QtWidgets.QPushButton(self.inputGroup)
        self.browseBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.browseBtn.setObjectName("browseBtn")
        self.gridLayout_3.addWidget(self.browseBtn, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.inputGroup)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)
        self.input_flat_flat = QtWidgets.QRadioButton(self.inputGroup)
        self.input_flat_flat.setObjectName("input_flat_flat")
        self.gridLayout_3.addWidget(self.input_flat_flat, 5, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.inputGroup)
        self.label_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.input_fov = QtWidgets.QSpinBox(self.inputGroup)
        self.input_fov.setEnabled(False)
        self.input_fov.setMinimumSize(QtCore.QSize(60, 0))
        self.input_fov.setMaximumSize(QtCore.QSize(80, 16777215))
        self.input_fov.setMaximum(360)
        self.input_fov.setProperty("value", 180)
        self.input_fov.setObjectName("input_fov")
        self.horizontalLayout.addWidget(self.input_fov)
        self.label_7 = QtWidgets.QLabel(self.inputGroup)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.gridLayout_3.addLayout(self.horizontalLayout, 5, 2, 1, 1)
        self.input_ud_fisheye = QtWidgets.QRadioButton(self.inputGroup)
        self.input_ud_fisheye.setObjectName("input_ud_fisheye")
        self.gridLayout_3.addWidget(self.input_ud_fisheye, 4, 2, 1, 1)
        self.gridLayout_2.addWidget(self.inputGroup, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.labelTimer = QtWidgets.QLabel(self.centralwidget)
        self.labelTimer.setText("")
        self.labelTimer.setObjectName("labelTimer")
        self.horizontalLayout_3.addWidget(self.labelTimer)
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.startBtn.setObjectName("startBtn")
        self.horizontalLayout_3.addWidget(self.startBtn)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 6, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem5, 2, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 1, 2, 1, 1)
        self.outputGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.outputGroup.setObjectName("outputGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.outputGroup)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.outputGroup)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.outputGroup)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.output_lr_360 = QtWidgets.QRadioButton(self.outputGroup)
        self.output_lr_360.setObjectName("output_lr_360")
        self.gridLayout.addWidget(self.output_lr_360, 0, 2, 1, 1)
        self.output_lr_180 = QtWidgets.QRadioButton(self.outputGroup)
        self.output_lr_180.setChecked(True)
        self.output_lr_180.setObjectName("output_lr_180")
        self.gridLayout.addWidget(self.output_lr_180, 0, 1, 1, 1)
        self.output_ud_360 = QtWidgets.QRadioButton(self.outputGroup)
        self.output_ud_360.setObjectName("output_ud_360")
        self.gridLayout.addWidget(self.output_ud_360, 1, 2, 1, 1)
        self.output_ud_180 = QtWidgets.QRadioButton(self.outputGroup)
        self.output_ud_180.setObjectName("output_ud_180")
        self.gridLayout.addWidget(self.output_ud_180, 1, 1, 1, 1)
        self.output_filePath = QtWidgets.QLineEdit(self.outputGroup)
        self.output_filePath.setMinimumSize(QtCore.QSize(200, 0))
        self.output_filePath.setObjectName("output_filePath")
        self.gridLayout.addWidget(self.output_filePath, 5, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 4, 1, 1, 1)
        self.output_lr_fisheye = QtWidgets.QRadioButton(self.outputGroup)
        self.output_lr_fisheye.setObjectName("output_lr_fisheye")
        self.gridLayout.addWidget(self.output_lr_fisheye, 2, 1, 1, 1)
        self.output_flat_flat = QtWidgets.QRadioButton(self.outputGroup)
        self.output_flat_flat.setObjectName("output_flat_flat")
        self.gridLayout.addWidget(self.output_flat_flat, 3, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.outputGroup)
        self.label_4.setEnabled(True)
        self.label_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.output_fov = QtWidgets.QSpinBox(self.outputGroup)
        self.output_fov.setEnabled(False)
        self.output_fov.setMinimumSize(QtCore.QSize(60, 0))
        self.output_fov.setMaximumSize(QtCore.QSize(80, 16777215))
        self.output_fov.setMaximum(360)
        self.output_fov.setProperty("value", 180)
        self.output_fov.setObjectName("output_fov")
        self.horizontalLayout_2.addWidget(self.output_fov)
        self.label_8 = QtWidgets.QLabel(self.outputGroup)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_2.addWidget(self.label_8)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 2, 1, 1)
        self.output_ud_fisheye = QtWidgets.QRadioButton(self.outputGroup)
        self.output_ud_fisheye.setObjectName("output_ud_fisheye")
        self.gridLayout.addWidget(self.output_ud_fisheye, 2, 2, 1, 1)
        self.gridLayout_2.addWidget(self.outputGroup, 3, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VR影片格式轉換"))
        self.input_ud_180.setText(_translate("MainWindow", "上下 VR180°"))
        self.input_lr_fisheye.setText(_translate("MainWindow", "左右 魚眼 fisheye"))
        self.input_lr_180.setText(_translate("MainWindow", "左右 VR180°"))
        self.input_ud_360.setText(_translate("MainWindow", "上下 VR360°"))
        self.input_lr_360.setText(_translate("MainWindow", "左右 VR360°"))
        self.label.setText(_translate("MainWindow", "檔案位置:"))
        self.browseBtn.setText(_translate("MainWindow", "瀏覽"))
        self.label_5.setText(_translate("MainWindow", "輸入格式:"))
        self.input_flat_flat.setText(_translate("MainWindow", "平面(無左右/上下差別)(test)"))
        self.label_2.setText(_translate("MainWindow", "魚眼FOV:"))
        self.label_7.setText(_translate("MainWindow", "°"))
        self.input_ud_fisheye.setText(_translate("MainWindow", "上下 魚眼 fisheye"))
        self.startBtn.setText(_translate("MainWindow", "開始"))
        self.label_3.setText(_translate("MainWindow", "輸出格式:"))
        self.label_6.setText(_translate("MainWindow", "輸出位置:"))
        self.output_lr_360.setText(_translate("MainWindow", "左右 VR360°"))
        self.output_lr_180.setText(_translate("MainWindow", "左右 VR180°"))
        self.output_ud_360.setText(_translate("MainWindow", "上下 VR360°"))
        self.output_ud_180.setText(_translate("MainWindow", "上下 VR180°"))
        self.output_lr_fisheye.setText(_translate("MainWindow", "左右 魚眼 fisheye"))
        self.output_flat_flat.setText(_translate("MainWindow", "平面(無左右/上下差別)(test)"))
        self.label_4.setText(_translate("MainWindow", "魚眼FOV:"))
        self.label_8.setText(_translate("MainWindow", "°"))
        self.output_ud_fisheye.setText(_translate("MainWindow", "上下 魚眼 fisheye"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
