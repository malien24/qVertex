# -*- coding: utf-8 -*-

__name__ = 'q_vertex_dialog_base'
__version__ = '0.1'
__author__ = 'Filippov Vladislav'

from PyQt4 import QtCore
import os.path
from PyQt4.QtGui import QDialog, QFileDialog
from QVertex.q_vertex_dialog_base_ui import Ui_QVertexDialogBase


class QVertexDialogBase (QDialog, Ui_QVertexDialogBase):
    def __init__(self, iface, msks):
        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        self.setupUi(self)
        self.listCrs.addItems(msks)