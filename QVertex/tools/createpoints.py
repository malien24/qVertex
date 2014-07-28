# -*- coding: utf-8 -*-
__author__ = 'filippov'

#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class CreatePoints():
    def __init__(self, iface):
        self.iface = iface

        if (self.iface.mapCanvas().currentLayer() is not None) \
                and (self.iface.mapCanvas().currentLayer().selectedFeatures() is not None):
            self.selection = self.iface.mapCanvas().currentLayer().selectedFeatures()
        else:
            QMessageBox.warning(self.iface.mainWindow(), 'Нет выбранных объектов',QMessageBox.Ok, QMessageBox.Ok)
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

        for every in self.selection:
            geom = every.geometry()
            if geom.isMultipart():
                polygons = geom.asMultiPolygon()
                for polygone in polygons:
                    self.numberRing = 0
                    for ring in polygone:
                        self.numberRing += 1
                        for i in ring:
                            self.createPointOnLayer(i, None)

            else:
                self.numberRing = 0
                rings = geom.asPolygon()
                for ring in rings:
                    self.numberRing += 1
                    for i in ring:
                        self.createPointOnLayer(i, None)

    def createPointOnLayer(self, point, name):
        feature = QgsFeature()
        feature.initAttributes(len(self.targetLayer.dataProvider().attributeIndexes()))
        feature.setGeometry(QgsGeometry.fromPoint(point))
        self.targetLayer.dataProvider().addFeatures([feature])
        del feature
        return True