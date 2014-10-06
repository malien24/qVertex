# -*- coding: utf-8 -*-
__author__ = 'filippov'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# import pydevd
#
# pydevd.settrace('localhost', port=53801, stdoutToServer=True, stderrToServer=True)

class CreatePoints():
    def __init__(self, iface, isnewpoint):
        self.iface = iface
        self.is_new_point = isnewpoint

        if (self.iface.mapCanvas().currentLayer() is not None) \
                and (self.iface.mapCanvas().currentLayer().selectedFeatures() is not None):
            self.selection = self.iface.mapCanvas().currentLayer().selectedFeatures()
        else:
            QMessageBox.warning(self.iface.mainWindow(), 'Нет выбранных объектов', QMessageBox.Ok, QMessageBox.Ok)
            return False

        self.layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in self.layermap.iteritems():
            #QMessageBox.information(self.iface.mainWindow(), layer.name(), str())
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == u"Точки":
                if layer.isValid():
                    self.targetLayer = layer
                else:
                    self.selection = None

    def Create(self):
        if (self.selection is None):
            return False
        self.targetLayer.startEditing()
        numPoint = self.getLastPointName()
        iter = 0
        for every in self.selection:
            geom = every.geometry()
            if geom.isMultipart():
                polygons = geom.asMultiPolygon()
                for polygone in polygons:
                    self.numberRing = 0
                    for ring in polygone:
                        iter = 0
                        self.numberRing += 1
                        for i in ring:
                            if iter < len(ring)-1:
                                numPoint += 1
                                self.createPointOnLayer(i, numPoint)
                            iter += 1

            else:
                self.numberRing = 0
                rings = geom.asPolygon()
                for ring in rings:
                    iter = 0
                    self.numberRing += 1
                    for i in ring:
                        if iter < len(ring)-1:
                            numPoint += 1
                            self.createPointOnLayer(i, numPoint)
                        iter += 1

        self.targetLayer.commitChanges()

    def createPointOnLayer(self, point, name):
        feature = QgsFeature()
        feature.initAttributes(len(self.targetLayer.dataProvider().attributeIndexes()))
        feature.setGeometry(QgsGeometry.fromPoint(point))
        if (self.is_new_point):
            numvalue = u'н' + str(name)
        else:
            numvalue = str(name)
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'name'), u'н' + str(name))
        self.targetLayer.dataProvider().addFeatures([feature])
        del feature
        return True


    def getLastPointName(self):
        maxValue = 0
        iter = self.targetLayer.getFeatures()
        for feature in iter:
            idx = self.targetLayer.fieldNameIndex('name')
            val = feature.attributes()[idx]
            if (val[:1] == u'н'):
                val = val[1:]
            if val > maxValue:
                maxValue = val
                print maxValue
        return maxValue