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
from PyQt4.QtGui import QAction, QIcon, QMenu, QFileDialog
# Initialize Qt resources from file resources.py
from _codecs import encode
from qgis._core import QgsGeometry
import resources_rc
# Import the code for the dialog
from q_vertex_dialog_base import QVertexDialogBase
from qgis.core import *
import os.path, sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import QgsMessageBar
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools'))
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools/svgwrite'))
from createpoints import CreatePoints
from tools.createCoordCatalog import CreateCoordCatalog
from tools.createGeodata import CreateGeodata
from shiftSheet import ShiftSheet
import shutil
import math

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
        # /home/filippov/work/test.qgs -> /home/filippov/work/test

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

        self.dlg_coordcatalog = None
        self.dlg_geodata = None

        # Declare instance attributes
        self.actions = []
        #self.menu = self.tr(u'&qVertex')
        # TODO: We are going to let the user set this up in a future iteration
        #self.toolbar = self.iface.addToolBar(u'QVertex')
        #self.toolbar.setObjectName(u'QVertex')

        # Настройки http://gis-lab.info/docs/qgis/cookbook/settings.html
        #print self.plugin_dir
        self.settings = QSettings(self.plugin_dir + os.sep + 'config.ini', QSettings.IniFormat)

        if sys.platform.startswith('win'):
            self.lastDir = self.settings.value('last_dir', self.plugin_dir)
        else:
            self.lastDir = self.settings.value('last_dir', self.plugin_dir)

        msk = self.settings.value('current_crs')
        self.current_crs = self.settings.value(msk, '+proj=longlat +datum=WGS84 +no_defs')
        # self.iface.messageBar().pushMessage(u'Используется '+msk, QgsMessageBar.INFO, 15)

        #msk_names = self.settings.value('msk_names')
        self.dlg = None#QVertexDialogBase(self.iface, msk_names)
        self.dlgShiftSheet = None
        #self.showSettings()

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
        #add_to_toolbar=True,
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
        self.menu.setTitle(u"QVertex")

        self.qvertex_createProject = QAction(u"Создать проект", self.iface.mainWindow())
        self.qvertex_createProject.setEnabled(True)
        # self.qvertex_createProject.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.menu.addAction(self.qvertex_createProject)

        # self.qvertex_showSettings = QAction(u"Настройка МСК", self.iface.mainWindow())
        # self.qvertex_showSettings.setEnabled(True)
        # # self.qvertex_showSettings.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        # self.menu.addAction(self.qvertex_showSettings)


        self.pointMenu = QMenu()
        self.pointMenu.setTitle(u"Точки")

        self.qvertex_createVertex = QAction(u"Создать примыкающие вершины", self.iface.mainWindow())
        self.qvertex_createVertex.setEnabled(True)
        # self.qvertex_createVertex.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))

        self.qvertex_createPoint = QAction(u"Создать характерные точки", self.iface.mainWindow())
        self.qvertex_createPoint.setEnabled(True)
        #self.qvertex_createPoint.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))

        #self.qvertex_createNewPoint.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.pointMenu.addActions([self.qvertex_createVertex, self.qvertex_createPoint])
        self.menu.addMenu(self.pointMenu)

        self.qvertex_createBoundPart = QAction(u"Создать части границ", self.iface.mainWindow())
        self.qvertex_createBoundPart.setEnabled(True)
        # self.qvertex_createProject.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.menu.addAction(self.qvertex_createBoundPart)


        self.reportMenu = QMenu()
        self.reportMenu.setTitle(u"Отчёты")

        self.qvertex_createCtalog = QAction(u"HTML-ведомость координат", self.iface.mainWindow())
        self.qvertex_createCtalog.setEnabled(True)

        self.qvertex_createMapPlan = QAction(u"HTML-ведомость карта(план)", self.iface.mainWindow())
        self.qvertex_createMapPlan.setEnabled(True)

        self.qvertex_createGeodata = QAction(u"SVG-ведомость и описание границ", self.iface.mainWindow())
        self.qvertex_createGeodata.setEnabled(True)
        # self.qvertex_createGeodata.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.reportMenu.addActions([self.qvertex_createCtalog, self.qvertex_createMapPlan, self.qvertex_createGeodata])
        self.menu.addMenu(self.reportMenu)

        self.qvertex_shiftSheet = QAction(u"Сдвинуть листы", self.iface.mainWindow())
        self.qvertex_shiftSheet.setEnabled(True)
        # self.qvertex_shiftSheet.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.menu.addAction(self.qvertex_shiftSheet)

        self.qvertex_exportTechno = QAction(u"Экспорт в Технокад", self.iface.mainWindow())
        self.qvertex_exportTechno.setEnabled(True)
        # self.qvertex_exportTechno.setIcon(QIcon(":/plugins/QVertex/icons/importkk.png"))
        self.menu.addAction(self.qvertex_exportTechno)

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
        QObject.connect(self.qvertex_createCtalog, SIGNAL("triggered()"), self.doCreateCoordcatalog)
        QObject.connect(self.qvertex_createMapPlan, SIGNAL("triggered()"), self.doCatalogMapPlan)
        QObject.connect(self.qvertex_createGeodata, SIGNAL("triggered()"), self.doCreateGeodata)
        QObject.connect(self.qvertex_createBoundPart, SIGNAL("triggered()"), self.createBoundPart)
        QObject.connect(self.qvertex_exportTechno, SIGNAL("triggered()"), self.exportTechno)
        QObject.connect(self.qvertex_shiftSheet, SIGNAL("triggered()"), self.doShiftSheet)

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
        if self.iface.mapCanvas().layers() > 0 and self.iface.mapCanvas().currentLayer() is not None:
            if self.iface.mapCanvas().currentLayer().selectedFeatures() is not None:
                return True
            else:
                return False
        else:
            return False

    def getLayerByName(self, layerName):
        for layer in self.iface.mapCanvas().layers():
            if layer.name() == layerName:
                return layer

    def isMultiPart(self, feature):
        if feature.attribute(u'order') != NULL:
            return True

    def doCreatePublicVertexes(self):
        for clayer in self.iface.mapCanvas().layers():
            if clayer.name() == u'ЗУ':
                pointLayer = clayer
                break
            else:
                pointLayer = None
        if self.isObjectsSelected() and pointLayer is not None:
            pointLayer.startEditing()
            try:
                for feat in self.iface.mapCanvas().currentLayer().selectedFeatures():
                    geom = feat.geometry()
                    if geom.isMultipart():
                        polygons = geom.asMultiPolygon()
                        for polygone in polygons:
                            print 'parse multipolygon part'
                            for ring in polygone:
                                print 'parse multipolygon part ring'
                                for point in ring:
                                    succ = pointLayer.addTopologicalPoints(point)
                                    self.iface.messageBar().pushMessage(u'Добавлены ' + str(succ).encode('UTF-8') + u' примыкающие вершины',
                                                                   QgsMessageBar.INFO, 5)
                                    #print 'inserted result ', str(succ)
                    else:
                        for ring in geom.asPolygon():
                            for point in ring:
                                succ = pointLayer.addTopologicalPoints(point)
                                self.iface.messageBar().pushMessage(u'Добавлены ' + str(succ).encode('UTF-8') + u' примыкающие вершины',
                                                                   QgsMessageBar.INFO, 5)
            except Exception as err:
                self.iface.messageBar().pushMessage(u'Ошибка при добавлении примыкающих вершин! ' + err.encode('UTF-8'),
                                                                   QgsMessageBar.ERROR, 5)
                print 'error in doCreatePublicVertexes!', err
            finally:
                print 'commit'
                pointLayer.commitChanges()

    # копирование шаблонных шейпов и прочего составляющего проект
    def doCreateProject(self):
        curr_path = self.lastDir
        if curr_path == u'':
            curr_path = os.getcwd()
        work_dir_name = QFileDialog.getExistingDirectory(None, u'Выберите папку для нового проекта', curr_path)
        #print type(work_dir_name)
        if work_dir_name != u'':
            if sys.platform.startswith('win'):
                current_path = work_dir_name.encode('cp1251')
            else:
                current_path = work_dir_name
            try:
                shutil.copytree(self.plugin_dir+ os.sep + 'start', current_path + os.sep + 'qvertex')
                #print 'shutil.copytree'

                proj = QgsProject.instance()
                print current_path + os.sep + 'qvertex'+ os.sep + 'landplan.qgs'
                proj.read(QFileInfo(current_path + os.sep + 'qvertex'+ os.sep + 'landplan.qgs'))
                self.settings.setValue('last_dir', current_path + os.sep + 'qvertex')
                #self.showSettings()
            except shutil.Error as ex:
                self.iface.messageBar().pushMessage(ex.message, QgsMessageBar.ERROR, 1)
            finally:
                pass
        else:
            print 'cancelled'

    def showSettings(self):
        msk_names = self.settings.value('msk_names')
        if self.dlg is None:
            self.dlg = QVertexDialogBase(self.iface, msk_names)
            self.dlg.setWindowModality(Qt.WindowModal)
        if self.dlg.exec_() == 1:
            msk = self.dlg.listCrs.currentItem().text()
            #print msk
            self.settings.setValue('current_crs', msk)
            self.current_crs = self.settings.value(msk, '+proj=longlat +datum=WGS84 +no_defs')
            self.iface.messageBar().pushMessage(u'Используется '+msk, QgsMessageBar.INFO, 1)

    def doCreatepoint(self):
        if self.isObjectsSelected():
            CreatePoints(self.iface)

    def doCreateCoordcatalog(self):
        if self.dlg_coordcatalog is None:
            self.dlg_coordcatalog = CreateCoordCatalog(self.iface, self.current_crs)
            self.dlg_coordcatalog.setWindowModality(Qt.NonModal)
        self.dlg_coordcatalog.show()

    def doCreateGeodata(self):
        if self.dlg_geodata is None:
            self.dlg_geodata = CreateGeodata(self.iface, self.current_crs)
            self.dlg_geodata.setWindowModality(Qt.NonModal)
        self.dlg_geodata.show()

    def createPart(self, layer, ring):
        c = len(ring)
        curr = 1
        pointLayer = self.getLayerByName(u'Точки')
        if pointLayer is None:
            idx = -1
        else:
            idx = pointLayer.fieldNameIndex('name')
        cadastreLayer = self.getLayerByName(u'Кадастр')
        for point in ring:
            if curr < c:
                point1 = point
                point2 = ring[curr]
                isEqual = False
                pt1stst = False
                pt2stst = False
                curr += 1
                #print point1, point2
                line_geometry=QgsGeometry.fromPolyline([QgsPoint(point1.x(), point1.y()),
                                                       QgsPoint(point2.x(), point2.y())])
                # find point
                for pointfeature in pointLayer.getFeatures():
                    if pointfeature.geometry().equals(QgsGeometry.fromPoint(QgsPoint(point1.x(), point1.y()))):
                        name = unicode(pointfeature.attribute(u'name'))
                        if name[0] == u'н':
                            pt1stst = True
                    if pointfeature.geometry().equals(QgsGeometry.fromPoint(QgsPoint(point2.x(), point2.y()))):
                        name = unicode(pointfeature.attribute(u'name'))
                        if name[0] == u'н':
                            pt2stst = True
                # check for identity
                features = layer.getFeatures()
                for f in features:
                    if line_geometry.equals(f.geometry()):
                        self.iface.messageBar().pushMessage(u'Найдена дублирующая часть границы, пропущена', level=QgsMessageBar.INFO)
                        isEqual = True
                        break
                #check for cadastre
                if not pt1stst and not pt2stst:
                    findInCadastre = False
                    print 'cadastre check'
                    if cadastreLayer is not None and not findInCadastre:
                        cadObjs = cadastreLayer.getFeatures()
                        for cadObj in cadObjs:
                            #print 'cadastre check iteration'
                            if cadObj.geometry().isMultipart():
                                for cpoly in cadObj.geometry().asMultiPolygon():
                                    if not findInCadastre:
                                        for cring in cpoly:
                                            cadCurr = 1
                                            if not findInCadastre:
                                                cc = len(cring)
                                                for cpoint in cring:
                                                    if cadCurr < cc:
                                                        cpoint1 = cpoint
                                                        cpoint2 = cring[cadCurr]
                                                        cadCurr += 1
                                                    cadLine=QgsGeometry.fromPolyline([QgsPoint(cpoint1.x(), cpoint1.y()), QgsPoint(cpoint2.x(), cpoint2.y())])
                                                    #print 'checking line'
                                                    if line_geometry.within(cadLine.buffer(0.000001, 16)):
                                                        print 'find in cadastre'
                                                        findInCadastre = True
                                                        break
                                                    else:
                                                        findInCadastre = False
                            else:
                                if not findInCadastre:
                                    for cring in cadObj.geometry().asPolygon():
                                        cadCurr = 1
                                        if not findInCadastre:
                                            cc = len(cring)
                                            for cpoint in cring:
                                                if cadCurr < cc:
                                                    cpoint1 = cpoint
                                                    cpoint2 = cring[cadCurr]
                                                    cadCurr += 1
                                                cadLine=QgsGeometry.fromPolyline([QgsPoint(cpoint1.x(), cpoint1.y()), QgsPoint(cpoint2.x(), cpoint2.y())])
                                                #print 'checking line'
                                                if  line_geometry.within(cadLine.buffer(0.000001, 16)):
                                                    print 'finded in cadastre'
                                                    findInCadastre = True
                                                    break
                                                else:
                                                    findInCadastre = False
                    if not findInCadastre:
                        pt2stst = True
                if not isEqual:
                    feat = QgsFeature()
                    feat.setGeometry(line_geometry)
                    typeidx = layer.fieldNameIndex('type')
                    feat.initAttributes(2)
                    if pt1stst or pt2stst:
                        feat.setAttribute(typeidx, 2)
                    else:
                        feat.setAttribute(typeidx, 0)
                    layer.dataProvider().addFeatures([feat])

    def createBoundPart(self):
        partLayer = self.getLayerByName(u'Части границ')
        if partLayer is not None:
            partLayer.startEditing()
            try:
                for feat in self.iface.mapCanvas().currentLayer().selectedFeatures():
                    geom = feat.geometry()
                    polygone = geom.asMultiPolygon()[0]
                    for ring in polygone:
                        self.createPart(partLayer, ring)
            except Exception as err:
                #self.iface.messageBar().pushMessage(err, QgsMessageBar.ERROR, 5)
                print 'error in createBoundPart!', err
            finally:
                partLayer.commitChanges()
                self.iface.messageBar().pushMessage(u'Создание частей границ завершено',
                                                    level=QgsMessageBar.INFO)

    def doCatalogMapPlan(self):
        pointLayer = self.getLayerByName(u'Точки')
        file_name = QFileDialog.getSaveFileName(None, u'Сохраните ведомость координат для карта(план)', self.lastDir, u'HTML файлы(*.html *.HTML)')
        if not file_name == u'':
            htmldata_start = u'<html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns:m="http://schemas.microsoft.com/office/2004/12/omml" xmlns="http://www.w3.org/TR/REC-html40"><head><meta http-equiv=Content-Type content="text/html; charset=windows-1251"><meta name=ProgId content=Word.Document><meta name=Generator content="Microsoft Word 15"><meta name=Originator content="Microsoft Word 15"></head><body lang=RU link=blue vlink=purple style=\'tab-interval:35.4pt\'><table class=MsoTableGrid border=1 cellspacing=0 cellpadding=0 width=756 style=\'width:567.05pt;margin-left:-15.9pt;border-collapse:collapse;border: none;mso-border-alt:solid windowtext .5pt;mso-yfti-tbllook:1184;mso-padding-alt: 0cm 5.4pt 0cm 5.4pt\'>'
            htmldata_row = u'<tr style=\'mso-yfti-irow:0;mso-yfti-firstrow:yes\'>  <td width=95 style=\'width:70.95pt;border:solid windowtext 1.0pt;mso-border-alt:  solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt\'>  <p class=MsoNormal align=centerstyle=\'text-align:center\'><span  style=\'font-size:10.0pt;color:black\'>{0}<o:p></o:p></span></p>  </td>  <td width=123 valign=top style=\'width:92.1pt;border:solid windowtext 1.0pt;  border-left:none;mso-border-left-alt:solid windowtext .5pt;mso-border-alt:  solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt\'>  <p class=MsoNormal align=center style=\'text-align:center\'>{1}</p>  </td>  <td width=113 valign=top style=\'width:3.0cm;border:solid windowtext 1.0pt;  border-left:none;mso-border-left-alt:solid windowtext .5pt;mso-border-alt:  solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt\'>  <p class=MsoNormal align=center style=\'text-align:center\'>{2}</p>  </td>  <td width=227 valign=top style=\'width:6.0cm;border:solid windowtext 1.0pt;  border-left:none;mso-border-left-alt:solid windowtext .5pt;mso-border-alt:  solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt\'>  <p class=MsoNormal align=center style=\'text-align:center\'><span  style=\'font-size:10.0pt;color:black\'>{4}<o:p></o:p></span></p>  </td>  <td width=198 valign=top style=\'width:148.85pt;border:solid windowtext 1.0pt;  border-left:none;mso-border-left-alt:solid windowtext .5pt;mso-border-alt:  solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt\'>  <p class=MsoNormal align=center style=\'text-align:center\'><b  style=\'mso-bidi-font-weight:normal\'><sub><span style=\'font-size:10.0pt\'>{3}</span></sub></b><span  style=\'font-size:10.0pt\'><o:p></o:p></span></p>  </td> </tr>'
            htmldata_end = u'</table></body></html>'

            exportData = htmldata_start
            for feat in self.iface.mapCanvas().currentLayer().selectedFeatures():
                polygone = feat.geometry().asMultiPolygon()[0]
                ringq = 0
                for ring in polygone:
                    for pt in ring:
                        for pointfeature in pointLayer.getFeatures():
                            if pointfeature.geometry().equals(QgsGeometry.fromPoint(QgsPoint(pt.x(), pt.y()))):
                                fullname = unicode(pointfeature.attribute(u'name'))
                                if fullname[0] == u'н':
                                    name = fullname[1:]+u';'
                                    prefix = u'н;'
                                else:
                                    name = fullname + u';'
                                    prefix = u';'

                                x = round(QgsGeometry.fromPoint(pt).asPoint().y(), 2)
                                sx = unicode('{:.2f}'.format(x))
                                y = round(QgsGeometry.fromPoint(pt).asPoint().x(), 2)
                                sy = unicode('{:.2f}'.format(y))
                                exportData += htmldata_row.format(fullname, sx, sy, u'–––––––', u'картометрический')
                                # pref = unicode(pointfeature.attribute(u'prec'))+u';'
                                # hold = unicode(pointfeature.attribute(u'hold'))

                    if len(polygone) >= ringq+2:
                        exportData += htmldata_row.format(u'', u'', u'', u'', u'')
                    ringq += 1
            exportData += htmldata_end
            try:
                ccf = open(file_name, 'w') # + u'.csv'
                ccf.write(exportData.encode('cp1251'))
            except Exception as err:
                print err
            finally:
                ccf.close()

    def exportTechno(self):
        pointLayer = None
        for clayer in self.iface.mapCanvas().layers():
            if clayer.name() == u'Точки': # TODO
                pointLayer = clayer
                break
            else:
                return

        file_name = QFileDialog.getSaveFileName(None, u'Сохраните данные для Технокада', self.lastDir, u'CSV файлы(*.csv *.CSV)')
        #print file_name
        if not file_name == u'':
            csvdata = u'Контур;Префикс номера;Номер;Старый X;Старый Y;Новый X;Новый Y;Метод определения;Формула;Радиус;Погрешность;Описание закрепления\n;;;;;;;;;;;\n'
            #delimLine = u';;;;;;;;;;;\n'

            # crsSrc = QgsCoordinateReferenceSystem(4326)
            # crsDest = QgsCoordinateReferenceSystem()
            # crsDest.createFromProj4(self.current_crs)
            # transform = QgsCoordinateTransform(crsSrc, crsDest)

            contour = 1
            for feat in self.iface.mapCanvas().currentLayer().selectedFeatures():
                geom = feat.geometry()
                if self.isMultiPart(feat):
                    # gt = QgsGeometry(geom)
                    # gt.transform(transform)
                    csvdata += self.prepareExportPoint(pointLayer, geom.asMultiPolygon()[0], 1)
                    if len(self.iface.mapCanvas().currentLayer().selectedFeatures()) > contour:
                        csvdata += u';;;;;;;;;;;\n'
                    contour += 1
                else:
                    # gt = QgsGeometry(geom)
                    # gt.transform(transform)
                    csvdata += self.prepareExportPoint(pointLayer, geom.asMultiPolygon()[0], 1)
            try:
                ccf = open(file_name, 'w') # + u'.csv'
                ccf.write(csvdata.encode('cp1251'))
            except Exception as err:
                print err
                #self.iface.messageBar().pushMessage(u'Ошибка при экспорте в Технокад! ' + err.encode('UTF-8'),
                                                                  # QgsMessageBar.ERROR, 5)
            finally:
                ccf.close()


    def doShiftSheet(self):
        print 'dlgShiftSheet'
        if self.dlgShiftSheet is None:
            print 'dlgShiftSheet is None'
            self.dlgShiftSheet = ShiftSheet(self.iface, self.current_crs)
            print 'dlgShiftSheet created'
            self.dlgShiftSheet.setWindowModality(Qt.NonModal)
        self.dlgShiftSheet.show()
        print 'dlgShiftSheet show'

    def prepareExportPoint(self, pointLayer, polygon, contour, transform):
        ringq = 0
        csvdata = u''
        for ring in polygon:
            for pt in ring:
                for pointfeature in pointLayer.getFeatures():
                    if pointfeature.geometry().equals(QgsGeometry.fromPoint(QgsPoint(pt.x(), pt.y()))):
                        fullname = unicode(pointfeature.attribute(u'name'))
                        if fullname[0] == u'н':
                            name = fullname[1:]+u';'
                            prefix = u'Н;'
                        else:
                            name = fullname + u';'
                            prefix = u';'

                        x = round(QgsGeometry.fromPoint(pt).asPoint().y(), 2)
                        sx = unicode('{:.2f}'.format(x))+u';'
                        y = round(QgsGeometry.fromPoint(pt).asPoint().x(), 2)
                        sy = unicode('{:.2f}'.format(y))+u';'
                        pref = unicode(pointfeature.attribute(u'prec'))+u';'
                        hold = unicode(pointfeature.attribute(u'hold'))
                        if ringq > 0:
                            cnt = u'['+unicode(str(contour))+u'.'+unicode(str(ringq))+u'];'
                        else:
                            cnt = u'['+unicode(str(contour))+u'];'
                        csvdata += cnt+prefix+name+u';;'+sx+sy+u';;;'+pref+hold+u'\n'

            if len(polygon) >= ringq+2:
                csvdata +=u';;;;;;;;;;;\n'
            ringq += 1

        return csvdata

    # Упорядочить точки (первая на северо-западе)
    def doChangePointPos(self):
        try:
            for feat in self.iface.mapCanvas().currentLayer().selectedFeatures():
                findPointIdx = 0
                #newgeomarr = []
                #newgeom = null
                geom = feat.geometry()
                if self.isMultiPart(feat):
                    polygons = geom.asMultiPolygon()[0]
                    for polygone in polygons:
                        print 'parse multipolygon part'
                        for ring in polygone:
                            findPointIdx = findNorthWestPoint(ring)
                            changeGeometryPointOrder(ring, findPointIdx)
                else:
                    for ring in geom.asMultiPolygon()[0]:
                        findPointIdx = findNorthWestPoint(ring)
                        changeGeometryPointOrder(ring, findPointIdx)
        except:
            print 'error in doChangePointPos'
        finally:
            feat.setGeometry(newgeom)
            print 'change geometry'
        pass

    def findNorthWestPoint(self, ring):
        maxYX = 10000000
        iter = 0
        idx = 0
        for point in ring:
            if iter < len(ring)-1:
                x = point.x()
                y = point.y()
                if (x - y) < maxYX:
                    maxYX = (x - y)
                    idx = iter
                iter += 1
        return iter

    def changeGeometryPointOrder(self, ring, newPointIdx):
        if newPointIdx == 0:
            return ring

        after = ring[newPointIdx:]
        del after[-1]
        firstPoint = after[0]
        before = ring[:newPointIdx]
        after.extend(before)
        after.append(firstPoint)
        ring = after
