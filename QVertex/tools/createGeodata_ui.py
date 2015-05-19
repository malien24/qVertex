# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createGeodata.ui'
#
# Created: Tue Oct 28 23:27:53 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_CoordGeodata(object):
    def setupUi(self, CoordGeodata):
        CoordGeodata.setObjectName(_fromUtf8("CoordGeodata"))
        CoordGeodata.resize(624, 682)
        self.verticalLayout = QtGui.QVBoxLayout(CoordGeodata)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textEdit = QtWebKit.QWebView(CoordGeodata)
        self.textEdit.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.radioBtnRumb = QtGui.QCheckBox(CoordGeodata)
        self.radioBtnRumb.setObjectName(_fromUtf8("radioBtnRumb"))
        self.verticalLayout.addWidget(self.radioBtnRumb)
        self.line_3 = QtGui.QFrame(CoordGeodata)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout.addWidget(self.line_3)
        self.line_2 = QtGui.QFrame(CoordGeodata)
        self.line_2.setLineWidth(4)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.btnGeodata = QtGui.QPushButton(CoordGeodata)
        self.btnGeodata.setObjectName(_fromUtf8("btnGeodata"))
        self.verticalLayout.addWidget(self.btnGeodata)
        self.line = QtGui.QFrame(CoordGeodata)
        self.line.setLineWidth(4)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.btnSave = QtGui.QPushButton(CoordGeodata)
        self.btnSave.setEnabled(False)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.verticalLayout.addWidget(self.btnSave)
        self.buttonBox = QtGui.QDialogButtonBox(CoordGeodata)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CoordGeodata)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CoordGeodata.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CoordGeodata.reject)
        QtCore.QMetaObject.connectSlotsByName(CoordGeodata)

    def retranslateUi(self, CoordGeodata):
        CoordGeodata.setWindowTitle(_translate("CoordGeodata", "Ведомость, геоданные и описание границ", None))
        self.radioBtnRumb.setText(_translate("CoordGeodata", "Румбы (для геоданных)", None))
        self.btnGeodata.setText(_translate("CoordGeodata", "Создать ведомость, геоданные и описание границ", None))
        self.btnSave.setText(_translate("CoordGeodata", "Сохранить ведомость и геоданные в SVG", None))

from PyQt4 import QtWebKit
