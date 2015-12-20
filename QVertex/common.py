# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QVertex
                                 A QGIS plugin
 автоматизация землеустройства
                              -------------------
        begin                : 2015-12-20
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Филиппов Владислав
        email                : filippov70@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis._core import QgsGeometry

def getSelectedObject(mapCanvas, isMultipart = False):
    if mapCanvas().currentLayer().selectedFeatures() is not None:
        if not isMultiPart:
            return mapCanvas().currentLayer().selectedFeatures()[0]
        else:
            name = mapCanvas().currentLayer().selectedFeatures()[0].attribute(u'name')
            
            for obj in mapCanvas().currentLayer().features():

    else:
        return None

def getLayerByName(layers, layerName):
    for layer in layers:
        if layer.name() == layerName:
            return layer
    return None

def isMultiPart(self, feature):
    if feature.attribute(u'order') != NULL:
        return True
