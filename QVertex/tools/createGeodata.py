# -*- coding: utf-8 -*-
import platform
import sys

__name__ = 'createGeodata'
__version__ = '0.1'
__author__ = 'Filippov Vladislav'

from PyQt4 import QtCore, QtGui
import os.path
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog
from QVertex.tools.createGeodata_ui import Ui_CoordGeodata
from QVertex.tools.coordcatalog import CatalogData
from qgis.core import *


# Геоданные создаются на один ЗУ с любым количеством контуров
class CreateGeodata(QDialog, Ui_CoordGeodata):
    def __init__(self, iface):
        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        self.setupUi(self)
        self.curr_path = QgsProject.instance().fileName()[:-4]#get_defailt_path()
        #print self.curr_path
        self.btnSave.setEnabled(False)
        self.svg = None
        self.newSvg = None
        self.connect(self.btnGeodata, QtCore.SIGNAL("clicked()"), self.calculate)
        self.connect(self.btnSave, QtCore.SIGNAL("clicked()"), self.save_catalog)

    def calculate(self):
        if (self.iface.mapCanvas().currentLayer() is not None) \
            and (self.iface.mapCanvas().currentLayer().selectedFeatures() is not None):
            #for feature in self.iface.mapCanvas().currentLayer().selectedFeatures():
            ved = CatalogData(self.iface, self.radioBtnRumb.isChecked(), True, 1)
            #data = ved.geodata
            ved.createSvgGeodata(self.curr_path)
            #self.svg = ved.geodataSVG
            self.newSvg = ved.geodataNewSVG
            #print self.newSvg
            self.textEdit.setHtml(ved.pointDef)
            self.btnSave.setEnabled(True)

        #QMessageBox.warning(self.iface.mainWindow(), 'end', \
        #                    data, QtGui.QMessageBox.Ok, \
        #                    QtGui.QMessageBox.Ok)

    def save_catalog(self):
        file_name = QFileDialog.getSaveFileName(self, u'Сохраните Ведомость и Геоданные в SVG', self.curr_path, u'SVG файлы(*.svg *.SVG)')
        #abs_dir_name = QFileDialog.getExistingDirectory(self, u'Выберите папку', self.curr_path)
        if not file_name is None or not file_name == u'':
            if sys.platform.startswith('win'):
                current_path = file_name.encode('cp1251')
            else:
                current_path = file_name
            #print current_path
            self.curr_path = current_path
            #self.svg.saveas(current_path + '-geodata.svg')
            self.newSvg.saveas(current_path + '-vedomost.svg')
            self.textEdit.setHtml(u'Сохранение завершено')
            self.btnSave.setEnabled(False)
            self.svg = None
            self.newSvg = None
