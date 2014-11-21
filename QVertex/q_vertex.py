# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QVertex
                                 A QGIS plugin
 автоматизация землеустройства
                              -------------------
        begin                : 2014-07-24
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QMenu
# Initialize Qt resources from file resources.py
from _codecs import encode
from qgis._core import QgsGeometry
import resources_rc
# Import the code for the dialog
from q_vertex_dialog import QVertexDialog
from qgis.core import *
import os.path, sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qgis.utils
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools'))
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools/svgwrite'))
from tools.createpoints import CreatePoints
from tools.createCoordCatalog import CreateCoordCatalog
from tools.createGeodata import CreateGeodata
import shutil

class QVertex:
    """QGIS Plugin Implementation."""
    def __init__(self, iface):
        """Constructor.
		print os.path.abspath(os.path.dirname(__file__) + '/svgwrite'
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QVertex_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = QVertexDialog()
        self.dlg_coordcatalog = None
        self.dlg_geodata = None
        # Declare instance attributes
        self.actions = []
        #self.menu = self.tr(u'&qVertex')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'QVertex')
        self.toolbar.setObjectName(u'QVertex')

        # Настройки http://gis-lab.info/docs/qgis/cookbook/settings.html
        self.settings = QSettings(self.plugin_dir, 'config.ini')
        if sys.platform.startswith('win'):
            self.lastDir = self.settings.value('last_dir', self.plugin_dir)
        else:
            self.lastDir = self.settings.value('last_dir', self.plugin_dir)

    # noinspection PyMethodMayBeStatic
    # def tr(self, message):
    #     """Get the translation for a string using Qt translation API.
    #
    #     We implement this ourselves since we do not inherit QObject.
    #
    #     :param message: String for translation.
    #     :type message: str, QString
    #
    #     :returns: Translated version of message.
    #     :rtype: QString
    #     """
    #     # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
    #     return QCoreApplication.translate('QVertex', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.menu = QMenu()
        self.menu.setTitle(u"Землеустройство")

        self.qvertex_createProject = QAction(u"Создать проект", self.iface.mainWindow())
        self.qvertex_createProject.setEnabled(True)
        # self.qvertex_createProject.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.menu.addAction(self.qvertex_createProject)

        self.pointMenu = QMenu()
        self.pointMenu.setTitle(u"Точки")

        self.qvertex_createVertex = QAction(u"Создать общие вершины для ЗУ", self.iface.mainWindow())
        self.qvertex_createVertex.setEnabled(True)
        # self.qvertex_createVertex.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))

        self.qvertex_createPoint = QAction(u"Создать характерные точки", self.iface.mainWindow())
        self.qvertex_createPoint.setEnabled(True)
        #self.qvertex_createPoint.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))

        self.qvertex_createNewPoint = QAction(u"Создать новые характерные точки", self.iface.mainWindow())
        self.qvertex_createNewPoint.setEnabled(True)
        #self.qvertex_createNewPoint.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.pointMenu.addActions([self.qvertex_createVertex, self.qvertex_createPoint, self.qvertex_createNewPoint])
        self.menu.addMenu(self.pointMenu)

        self.reportMenu = QMenu()
        self.reportMenu.setTitle(u"Отчёты")

        self.qvertex_createCtalog = QAction(u"Создать ведомость координат", self.iface.mainWindow())
        self.qvertex_createCtalog.setEnabled(True)
        # self.qvertex_createCtalog.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))

        self.qvertex_createGeodata = QAction(u"Создать выноску геоданных", self.iface.mainWindow())
        self.qvertex_createGeodata.setEnabled(True)
        # self.qvertex_createGeodata.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.reportMenu.addActions([self.qvertex_createCtalog, self.qvertex_createGeodata])
        self.menu.addMenu(self.reportMenu)

        #self.menu.addActions([self.qvertex_createCtalog, self.qvertex_createGeodata])


        menu_bar = self.iface.mainWindow().menuBar()
        actions = menu_bar.actions()
        lastAction = actions[len(actions) - 1]
        menu_bar.insertMenu(lastAction, self.menu)
        #icon_path = ':/plugins/QVertex/icon.png'
        # self.add_action(
        #     icon_path,
        #     text=self.tr(u'Землеустройство'),
        #     callback=self.run,
        #     parent=self.iface.mainWindow())

        QObject.connect(self.qvertex_createProject, SIGNAL("triggered()"), self.doCreateProject)
        QObject.connect(self.qvertex_createVertex, SIGNAL("triggered()"), self.doCreatePublicVertexes)
        QObject.connect(self.qvertex_createPoint, SIGNAL("triggered()"), self.doCreatepoint)
        QObject.connect(self.qvertex_createNewPoint, SIGNAL("triggered()"), self.doCreateNewpoint)
        QObject.connect(self.qvertex_createCtalog, SIGNAL("triggered()"), self.doCreateCoordcatalog)
        QObject.connect(self.qvertex_createGeodata, SIGNAL("triggered()"), self.doCreateGeodata)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&qVertex'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def isObjectsSelected(self):
        if self.iface.mapCanvas().currentLayer().selectedFeatures() is not None:
            return True
        else:
            return False

    def doCreatePublicVertexes(self):
        for clayer in self.iface.mapCanvas().layers():
            if clayer.name() == u'ЗУ':
                pointLayer = clayer
                break
            else:
                pointLayer = None
        if self.isObjectsSelected() and pointLayer is not None:
            pointLayer.startEditing()
            print 'edit'
            try:
                for feat in self.iface.mapCanvas().currentLayer().selectedFeatures():
                    geom = feat.geometry()
                    for ring in geom.asPolygon():
                        for point in ring:
                            # pt = QgsGeometry.fromPoint(point)
                            # print point
                            succ = pointLayer.addTopologicalPoints(point)
                            print str(succ)
            except:
                pass
            finally:
                print 'commit'
                pointLayer.commitChanges()

    # копирование шаблонных шейпов и прочего составляющего проект
    def doCreateProject(self):
        curr_path = self.lastDir
        if curr_path == u'':
            curr_path = os.getcwd()
        work_dir_name = QFileDialog.getExistingDirectory(None, u'Выберите папку для нового проекта', curr_path)

        if not work_dir_name is None or not work_dir_name == u'':
            if sys.platform.startswith('win'):
                current_path = work_dir_name.encode('cp1251')
            else:
                current_path = work_dir_name
            try:
                shutil.copytree(self.plugin_dir+ os.sep + 'start', current_path + os.sep + 'qvertex')
                #print 'shutil.copytree'
                self.settings.setValue('last_dir', current_path + os.sep + 'qvertex')
                proj = QgsProject.instance()
                proj.read(QFileInfo(current_path + os.sep + 'qvertex'+ os.sep + 'defproj.qgs'))
            except shutil.Error as ex:
                print ex.message
            finally:
                pass

    def doCreatepoint(self):
        f = CreatePoints(self.iface, False)
        f.Create()

    def doCreateNewpoint(self):
        f = CreatePoints(self.iface, True)
        f.Create()

    def doCreateCoordcatalog(self):
        if self.dlg_coordcatalog is None:
            self.dlg_coordcatalog = CreateCoordCatalog(self.iface)
            self.dlg_coordcatalog.setWindowModality(Qt.NonModal)
        self.dlg_coordcatalog.show()

    def doCreateGeodata(self):
        if self.dlg_geodata is None:
            self.dlg_geodata = CreateGeodata(self.iface)
            self.dlg_geodata.setWindowModality(Qt.NonModal)
        self.dlg_geodata.show()