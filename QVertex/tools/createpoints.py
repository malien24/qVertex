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
        self.is_new_point = bool(isnewpoint)

        if (self.iface.mapCanvas().currentLayer() is not None) \
                and (self.iface.mapCanvas().currentLayer().selectedFeatures() is not None):
            self.selection = self.iface.mapCanvas().currentLayer().selectedFeatures()
            self.layermap = QgsMapLayerRegistry.instance().mapLayers()
            for name, layer in self.layermap.iteritems():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == u"Точки":
                    if layer.isValid():
                        self.targetLayer = layer
                        self.Create()
                    else:
                        self.selection = None
        else:
            print('selection is None and targetLayer is None')

    def Create(self):
        self.targetLayer.startEditing()
        numPoint = int(self.getLastPointName())
        #print u'номер последней точки ' + str(numPoint)

        for every in self.selection:
            count = 0
            geom = every.geometry()
            if geom.isMultipart():
                print 'Multipart geometry'
                polygons = geom.asMultiPolygon()
                for polygone in polygons:
                    for ring in polygone:
                        count = 0
                        for i in ring:
                            if count < len(ring) - 1:
                                count += 1
                                numPoint += 1
                                if not self.checkExistPoint(i):
                                    self.createPointOnLayer(i, numPoint)

            else:
                rings = geom.asPolygon()
                for ring in rings:
                    count = 0
                    for i in ring:
                        if count < len(ring) - 1:
                            count += 1
                            numPoint += 1
                            if not self.checkExistPoint(i):
                                self.createPointOnLayer(i, numPoint)

        self.targetLayer.commitChanges()
        self.targetLayer.triggerRepaint()

    def createPointOnLayer(self, point, name):
        feature = QgsFeature()
        feature.initAttributes(len(self.targetLayer.dataProvider().attributeIndexes()))
        feature.setGeometry(QgsGeometry.fromPoint(point))
        if self.is_new_point:
            numvalue = u'н' + str(name)
        else:
            numvalue = str(name)
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'name'), numvalue)
        self.targetLayer.dataProvider().addFeatures([feature])
        del feature
        return True

    def checkExistPoint(self, point):
        geom = QgsGeometry.fromPoint(point)
        features = self.targetLayer.getFeatures()
        for feature in features:
            if feature.geometry().intersects(geom):
                return True

    def getLastPointName(self):
        maxValue = 0
        featiter = self.targetLayer.getFeatures()
        for feature in featiter:
            idx = self.targetLayer.fieldNameIndex('name')
            val = feature.attributes()[idx]
            if val[:1] == u'н':
                val = int(val[1:])
            else:
                val = int(val)
            #print 'val' + str(val)

            if val > maxValue:
                maxValue = val
                if maxValue == 0:
                    maxValue = 1
                #print 'max'+str(maxValue)
        return maxValue