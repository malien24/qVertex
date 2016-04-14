# -*- coding: utf-8 -*-
__author__ = 'filippov'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# import pydevd
#
# pydevd.settrace('localhost', port=53801, stdoutToServer=True, stderrToServer=True)

class CreatePoints():
    def __init__(self, iface):
        self.iface = iface
        self.is_new_point = True
        self.cadastreLayer = None
        self.existPointIndex = 0
        self.newPointIndex = 0

        if (self.iface.mapCanvas().currentLayer() is not None) \
                and (self.iface.mapCanvas().currentLayer().selectedFeatures() is not None):
            self.selection = self.iface.mapCanvas().currentLayer().selectedFeatures()
            self.layermap = QgsMapLayerRegistry.instance().mapLayers()
            for name, layer in self.layermap.iteritems():
                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == u"Точки":
                    if layer.isValid():
                        self.targetLayer = layer

                if layer.type() == QgsMapLayer.VectorLayer and layer.name() == u"Кадастр":
                    if layer.isValid():
                        self.cadastreLayer = layer

            if self.targetLayer is not None:
                self.Create()
        else:
            print('selection is None and targetLayer is None')

    def Create(self):
        self.targetLayer.startEditing()
        self.getLastPointIndexes()
        countExist = self.existPointIndex
        countNew = self.newPointIndex
        #print countNew, countExist
        for every in self.selection:
            geom = every.geometry()
            #if geom.isMultipart():
            polygons = geom.asMultiPolygon()
            for polygone in polygons:
                for ring in polygone:
                    count = 0
                    for i in ring:
                        if count < len(ring) - 1:
                            count += 1
                            #print 'counter ' + str(count)
                            # проверка на наличие существующей точки
                            if (self.checkExistPoint(i, True)) or (self.checkExistPoint(i, False)):
                                countExist += 1
                                self.createPointOnLayer(i, countExist, False)
                            else:
                                countNew += 1
                                self.createPointOnLayer(i, countNew, True)
            # else:
            #     print 'not Multipart geometry'
            #     rings = geom.asPolygon()
            #     for ring in rings:
            #         count = 0
            #         for i in ring:
            #             if count < len(ring) - 1:
            #                 count += 1
            #                 # проверка на наличие существующей точки в кадастре и на слое Точки
            #                 if (self.checkExistPoint(i, True)) or (self.checkExistPoint(i, False)):
            #                     countExist += 1
            #                     self.createPointOnLayer(i, countExist, False)
            #                 else:
            #                     countNew += 1
            #                     self.createPointOnLayer(i, countNew, True)

        self.targetLayer.commitChanges()
        self.targetLayer.triggerRepaint()

    def createPointOnLayer(self, point, name, isNew):
        feature = QgsFeature()
        feature.initAttributes(len(self.targetLayer.dataProvider().attributeIndexes()))
        feature.setGeometry(QgsGeometry.fromPoint(point))
        #print point.x(), point.y()
        if isNew:
            #TODO 'Сделать возможность настройки'
            numvalue = u'н' + str(name)
        else:
            numvalue = str(name)
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'name'), numvalue)
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'prec'), u'0.10')
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'isdel'), 0)
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'type'), 0)
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'hold'), u'Закрепление отсутствует')
        self.targetLayer.dataProvider().addFeatures([feature])

    # проверка на наличие существующих точек (вершин) на кадастровом слое и
    # на слое с ЗУ
    def checkExistPoint(self, point, cadastre):
        geom = QgsGeometry.fromPoint(point).buffer(0.00000002, 16)
        if cadastre:
            features = self.cadastreLayer.getFeatures()
        else:
            features = self.targetLayer.getFeatures()

        for feature in features:
            if feature.geometry().intersects(geom):
                return True
        return False

    def getLastPointIndexes(self):
        maxValue = 0
        valExist = 0
        valNew = 0
        featiter = self.targetLayer.getFeatures()
        for feature in featiter:
            idx = self.targetLayer.fieldNameIndex('name')
            val = feature.attributes()[idx]
            if val[:1] == u'н':
                valNew = int(val[1:])
            else:
                valExist = int(val)
            #print 'val' + str(val)
            if valExist > maxValue:
                maxValue = valExist
                if maxValue == 0:
                    maxValue = 1
            if valNew > maxValue:
                maxValue = valNew
                if maxValue == 0:
                    maxValue = 1
        self.existPointIndex = int(valExist)
        self.newPointIndex = int(valNew)

    # depricated
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
        #print 'get max'+str(maxValue)
        return maxValue
