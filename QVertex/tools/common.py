# -*- coding: utf-8 -*-
import os
from qgis.core import *
__author__ = 'filippov'


def get_defailt_path():
    try:
        #todo не работает! :)
        return QgsProject.instance().fileName()[:-4]
    except:
        return os.getcwd()