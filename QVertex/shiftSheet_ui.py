# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shiftSheet.ui'
#
# Created: Fri Dec 25 15:31:41 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setMinimumSize(QtCore.QSize(200, 100))
        Dialog.setMaximumSize(QtCore.QSize(200, 100))
        Dialog.setBaseSize(QtCore.QSize(200, 100))
        self.spinValue = QtGui.QSpinBox(Dialog)
        self.spinValue.setGeometry(QtCore.QRect(87, 10, 111, 33))
        self.spinValue.setMinimum(1)
        self.spinValue.setMaximum(1000)
        self.spinValue.setSingleStep(25)
        self.spinValue.setProperty("value", 50)
        self.spinValue.setObjectName(_fromUtf8("spinValue"))
        self.pushLeft = QtGui.QPushButton(Dialog)
        self.pushLeft.setGeometry(QtCore.QRect(0, 60, 61, 26))
        self.pushLeft.setIconSize(QtCore.QSize(24, 20))
        self.pushLeft.setFlat(False)
        self.pushLeft.setObjectName(_fromUtf8("pushLeft"))
        self.pushRight = QtGui.QPushButton(Dialog)
        self.pushRight.setGeometry(QtCore.QRect(140, 60, 61, 26))
        self.pushRight.setIconSize(QtCore.QSize(24, 20))
        self.pushRight.setObjectName(_fromUtf8("pushRight"))
        self.pushUp = QtGui.QPushButton(Dialog)
        self.pushUp.setGeometry(QtCore.QRect(70, 44, 61, 26))
        self.pushUp.setIconSize(QtCore.QSize(24, 20))
        self.pushUp.setObjectName(_fromUtf8("pushUp"))
        self.pushDown = QtGui.QPushButton(Dialog)
        self.pushDown.setGeometry(QtCore.QRect(70, 74, 61, 26))
        self.pushDown.setIconSize(QtCore.QSize(24, 20))
        self.pushDown.setObjectName(_fromUtf8("pushDown"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 10, 106, 35))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Сдвиг листа", None))
        self.pushLeft.setText(_translate("Dialog", "влево", None))
        self.pushRight.setText(_translate("Dialog", "вправо", None))
        self.pushUp.setText(_translate("Dialog", "вверх", None))
        self.pushDown.setText(_translate("Dialog", "вниз", None))
        self.label.setText(_translate("Dialog", "Шаг (метры):", None))
