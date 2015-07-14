# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\filippov\.qgis2\python\plugins\QVertex\q_vertex_dialog_base.ui'
#
# Created: Tue Jul 14 15:50:46 2015
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

class Ui_QVertexDialogBase(object):
    def setupUi(self, QVertexDialogBase):
        QVertexDialogBase.setObjectName(_fromUtf8("QVertexDialogBase"))
        QVertexDialogBase.resize(398, 243)
        self.button_box = QtGui.QDialogButtonBox(QVertexDialogBase)
        self.button_box.setGeometry(QtCore.QRect(20, 210, 361, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.listCrs = QtGui.QListWidget(QVertexDialogBase)
        self.listCrs.setGeometry(QtCore.QRect(20, 10, 361, 192))
        self.listCrs.setObjectName(_fromUtf8("listCrs"))

        self.retranslateUi(QVertexDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), QVertexDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), QVertexDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(QVertexDialogBase)

    def retranslateUi(self, QVertexDialogBase):
        QVertexDialogBase.setWindowTitle(_translate("QVertexDialogBase", "qVertex", None))

