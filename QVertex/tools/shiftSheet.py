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
import math


class ShiftSheet(QDialog, Ui_Dialog):
    def __init__(self, iface, crs):
        QDialog.__init__(self, iface.mainWindow())
        self.crs = crs
        self.iface = iface
        self.setupUi(self)
        self.selection = iface.mapCanvas().currentLayer().selectedFeatures()

        self.connect(self.pushUp, QtCore.SIGNAL("clicked()"), self.moveUp)
        self.connect(self.pushDown, QtCore.SIGNAL("clicked()"), self.moveDown)
        self.connect(self.pushRight, QtCore.SIGNAL("clicked()"), self.moveRight)
        self.connect(self.pushLeft, QtCore.SIGNAL("clicked()"), self.moveLeft)

    def moveLeft(self):
        if self.selection is not None:
            for feature in self.selection:
                fid = feature.id()
                geom = feature.geometry()
                shift = int(self.spinValue.value())
                # 1 m ~ 0.00001
                shiftDegree = shift * 0.00001
                newgeom = self.changeGeometry(geom, -shiftDegree, 0)
                if newgeom is not None:
                    self.iface.mapCanvas().currentLayer().startEditing()
                    feature.setGeometry(newgeom)
                    if self.iface.mapCanvas().currentLayer().changeGeometry(fid, newgeom):
                        self.iface.mapCanvas().currentLayer().commitChanges()
                    else:
                        self.iface.mapCanvas().currentLayer().rollBack()

    def moveRight(self):
        if self.selection is not None:
            for feature in self.selection:
                fid = feature.id()
                geom = feature.geometry()
                shift = int(self.spinValue.value())
                # 1 m ~ 0.00001
                shiftDegree = shift * 0.00001
                newgeom = self.changeGeometry(geom, shiftDegree, 0)
                if newgeom is not None:
                    self.iface.mapCanvas().currentLayer().startEditing()
                    feature.setGeometry(newgeom)
                    if self.iface.mapCanvas().currentLayer().changeGeometry(fid, newgeom):
                        self.iface.mapCanvas().currentLayer().commitChanges()
                    else:
                        self.iface.mapCanvas().currentLayer().rollBack()
    def moveUp(self):
        if self.selection is not None:
            for feature in self.selection:
                fid = feature.id()
                geom = feature.geometry()
                shift = int(self.spinValue.value())
                # 1 m ~ 0.00001
                shiftDegree = shift * 0.00001
                newgeom = self.changeGeometry(geom, 0, shiftDegree)
                if newgeom is not None:
                    self.iface.mapCanvas().currentLayer().startEditing()
                    feature.setGeometry(newgeom)
                    if self.iface.mapCanvas().currentLayer().changeGeometry(fid, newgeom):
                        self.iface.mapCanvas().currentLayer().commitChanges()
                    else:
                        self.iface.mapCanvas().currentLayer().rollBack()

    def moveDown(self):
        if self.selection is not None:
            for feature in self.selection:
                fid = feature.id()
                geom = feature.geometry()
                shift = int(self.spinValue.value())
                # 1 m ~ 0.00001
                shiftDegree = shift * 0.00001
                newgeom = self.changeGeometry(geom, 0, -shiftDegree)
                if newgeom is not None:
                    self.iface.mapCanvas().currentLayer().startEditing()
                    feature.setGeometry(newgeom)
                    if self.iface.mapCanvas().currentLayer().changeGeometry(fid, newgeom):
                        self.iface.mapCanvas().currentLayer().commitChanges()
                    else:
                        self.iface.mapCanvas().currentLayer().rollBack()
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
                    geomNew = QgsGeometry.fromPolygon([points])
                    isFirstRing = False
                else:
                    geomNew.addRing(points)

            if geomNew.isGeosValid():
                return QgsGeometry.fromMultiPolygon([geomNew.asPolygon()])
            else:
                return None
        else:
            return None
