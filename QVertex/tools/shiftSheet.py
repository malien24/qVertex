# -*- coding: utf-8 -*-
__name__ = 'shiftSheet'
__version__ = '0.1'
__author__ = 'Filippov Vladislav'

from PyQt4 import QtCore, QtGui
#import os.path
#import platform
import sys
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog
from QVertex.tools.shiftSheet_ui import Ui_Dialog
from qgis.core import *
from qgis._core import *


class ShiftSheet(QDialog, Ui_Dialog):
    def __init__(self, iface, crs):
        QDialog.__init__(self, iface.mainWindow())
        self.crs = crs
        self.iface = iface
        self.setupUi(self)
        self.selection = iface.mapCanvas().currentLayer().selectedFeatures()

        self.connect(self.pushUp, QtCore.SIGNAL("clicked()"), self.moveUp)

    def moveUp(self):
        if self.selection is not None:
            for feature in self.selection:
                geom = feature.geometry()
                newgeom = self.changeGeometry(geom, 0.01, 0)
                if newgeom is not None:
                    feature.setGeometry(newgeom)

    def changeGeometry(self, geom, dx, dy):
        if geom.isGeosValid():
            isFirstRing = True
            # лист это мультиполигон с одним контуром
            rings = None
            geomNew = None
            if geom.isMultipart():
                rings = geom.asMultiPolygon()[0]
            else:
                rings = geom.asPolygon()

            for ring in rings:
                points = []
                for i in ring:
                    newX = i.x()+dx
                    newY = i.y()+dy
                    point = QgsGeometry.fromPoint(QgsPoint(newX, newY))
                    points.append(point.asPoint())
                if isFirstRing:
                    geomNew = QgsGeometry().fromPolygon([points])
                    isFirstRing = False
                else:
                    geomNew.addRing(points)

            if geomNew.isGeosValid():
                return geomNew
            else:
                return None
        else:
            return None
