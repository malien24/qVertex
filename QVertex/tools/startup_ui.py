# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\home\src\qVertex\QVertex\tools\startup.ui'
#
# Created: Mon Apr 06 14:59:01 2015
#      by: PyQt4 UI code generator 4.10.2
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
        Dialog.resize(400, 301)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 260, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.listViewPrjType = QtGui.QListView(Dialog)
        self.listViewPrjType.setGeometry(QtCore.QRect(20, 60, 361, 191))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listViewPrjType.sizePolicy().hasHeightForWidth())
        self.listViewPrjType.setSizePolicy(sizePolicy)
        self.listViewPrjType.setFrameShape(QtGui.QFrame.StyledPanel)
        self.listViewPrjType.setSizeAdjustPolicy(QtGui.QAbstractScrollArea.AdjustIgnored)
        self.listViewPrjType.setObjectName(_fromUtf8("listViewPrjType"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 20, 361, 25))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEditFolder = QtGui.QLineEdit(self.widget)
        self.lineEditFolder.setObjectName(_fromUtf8("lineEditFolder"))
        self.horizontalLayout.addWidget(self.lineEditFolder)
        self.pushBtnSelectFolder = QtGui.QPushButton(self.widget)
        self.pushBtnSelectFolder.setObjectName(_fromUtf8("pushBtnSelectFolder"))
        self.horizontalLayout.addWidget(self.pushBtnSelectFolder)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushBtnSelectFolder.setText(_translate("Dialog", "Выбрать папку", None))

