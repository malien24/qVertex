# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tools/cadtoolssettings.ui'
#
# Created: Tue Feb  4 18:18:51 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CadToolsSettings(object):
    def setupUi(self, CadToolsSettings):
        CadToolsSettings.setObjectName(_fromUtf8("CadToolsSettings"))
        CadToolsSettings.resize(408, 284)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CadToolsSettings.sizePolicy().hasHeightForWidth())
        CadToolsSettings.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(CadToolsSettings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(CadToolsSettings)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(CadToolsSettings)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabCurves = QtGui.QWidget()
        self.tabCurves.setObjectName(_fromUtf8("tabCurves"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabCurves)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.tabCurves)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioFeaturePitch = QtGui.QRadioButton(self.groupBox)
        self.radioFeaturePitch.setChecked(True)
        self.radioFeaturePitch.setObjectName(_fromUtf8("radioFeaturePitch"))
        self.horizontalLayout.addWidget(self.radioFeaturePitch)
        self.spinBoxFeaturePitch = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxFeaturePitch.setEnabled(True)
        self.spinBoxFeaturePitch.setDecimals(1)
        self.spinBoxFeaturePitch.setMaximum(100.0)
        self.spinBoxFeaturePitch.setProperty("value", 2.0)
        self.spinBoxFeaturePitch.setObjectName(_fromUtf8("spinBoxFeaturePitch"))
        self.horizontalLayout.addWidget(self.spinBoxFeaturePitch)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.radioFeatureAngle = QtGui.QRadioButton(self.groupBox)
        self.radioFeatureAngle.setObjectName(_fromUtf8("radioFeatureAngle"))
        self.horizontalLayout_2.addWidget(self.radioFeatureAngle)
        self.spinBoxFeatureAngle = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinBoxFeatureAngle.setDecimals(1)
        self.spinBoxFeatureAngle.setProperty("value", 1.0)
        self.spinBoxFeatureAngle.setObjectName(_fromUtf8("spinBoxFeatureAngle"))
        self.horizontalLayout_2.addWidget(self.spinBoxFeatureAngle)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.tabCurves)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radioRubberAngle = QtGui.QRadioButton(self.groupBox_2)
        self.radioRubberAngle.setChecked(True)
        self.radioRubberAngle.setObjectName(_fromUtf8("radioRubberAngle"))
        self.horizontalLayout_3.addWidget(self.radioRubberAngle)
        self.spinBoxRubberAngle = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.spinBoxRubberAngle.setDecimals(1)
        self.spinBoxRubberAngle.setProperty("value", 5.0)
        self.spinBoxRubberAngle.setObjectName(_fromUtf8("spinBoxRubberAngle"))
        self.horizontalLayout_3.addWidget(self.spinBoxRubberAngle)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabCurves, _fromUtf8(""))
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName(_fromUtf8("tab2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelSplineTolerance = QtGui.QLabel(self.tab2)
        self.labelSplineTolerance.setObjectName(_fromUtf8("labelSplineTolerance"))
        self.horizontalLayout_4.addWidget(self.labelSplineTolerance)
        self.spinBoxSplineTolerance = QtGui.QDoubleSpinBox(self.tab2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSplineTolerance.sizePolicy().hasHeightForWidth())
        self.spinBoxSplineTolerance.setSizePolicy(sizePolicy)
        self.spinBoxSplineTolerance.setObjectName(_fromUtf8("spinBoxSplineTolerance"))
        self.horizontalLayout_4.addWidget(self.spinBoxSplineTolerance)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelSplineTightness = QtGui.QLabel(self.tab2)
        self.labelSplineTightness.setObjectName(_fromUtf8("labelSplineTightness"))
        self.horizontalLayout_5.addWidget(self.labelSplineTightness)
        self.spinBoxSplineTightness = QtGui.QDoubleSpinBox(self.tab2)
        self.spinBoxSplineTightness.setObjectName(_fromUtf8("spinBoxSplineTightness"))
        self.horizontalLayout_5.addWidget(self.spinBoxSplineTightness)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(CadToolsSettings)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CadToolsSettings.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CadToolsSettings.accept)
        QtCore.QMetaObject.connectSlotsByName(CadToolsSettings)

    def retranslateUi(self, CadToolsSettings):
        CadToolsSettings.setWindowTitle(QtGui.QApplication.translate("CadToolsSettings", "CadTools Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("CadToolsSettings", "Feature Segmentation", None, QtGui.QApplication.UnicodeUTF8))
        self.radioFeaturePitch.setText(QtGui.QApplication.translate("CadToolsSettings", "Pitch", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxFeaturePitch.setPrefix(QtGui.QApplication.translate("CadToolsSettings", "Millimeter(s) ", None, QtGui.QApplication.UnicodeUTF8))
        self.radioFeatureAngle.setText(QtGui.QApplication.translate("CadToolsSettings", "Angle", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxFeatureAngle.setPrefix(QtGui.QApplication.translate("CadToolsSettings", "Degree(s) ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("CadToolsSettings", "Rubberband Segmentation", None, QtGui.QApplication.UnicodeUTF8))
        self.radioRubberAngle.setText(QtGui.QApplication.translate("CadToolsSettings", "Angle", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxRubberAngle.setPrefix(QtGui.QApplication.translate("CadToolsSettings", "Degree(s) ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCurves), QtGui.QApplication.translate("CadToolsSettings", "Arcs", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSplineTolerance.setText(QtGui.QApplication.translate("CadToolsSettings", "Tolerance", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxSplineTolerance.setToolTip(QtGui.QApplication.translate("CadToolsSettings", "Polyline interpolation tolerance in map units.", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSplineTightness.setText(QtGui.QApplication.translate("CadToolsSettings", "Tightness", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QtGui.QApplication.translate("CadToolsSettings", "Spline", None, QtGui.QApplication.UnicodeUTF8))

