# -*- coding: utf-8 -*-
from compiler.ast import Node
__name__ = 'coordcatalog'
__version__ = '0.1'
__author__ = 'Filippov Vladislav'

#from pydev import pydevd
#from QVertex.tools.svgwrite.drawing import Drawing
import os
from __builtin__ import round
import math
# Библиотека в site-packages
from svgwrite import drawing, text, path, shapes, mm
from qgis.core import *


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Измерение дирекционного угла (румба) и горизонтального проложения
class Measure():

    def __init__(self, point1, point2, is_rumb):
        self.point1 = point1
        self.point2 = point2
        self.ddx = self.point2.x - self.point1.x
        self.ddy = self.point2.y - self.point1.y
        self.ang = -1
        self.len = -1
        self.angle = ''
        self.lenght = ''
        self.rumb = u''
        self.calclenght()
        if is_rumb:
            self.calcrumb()
        else:
            self.calcangle()

    def calclenght(self):
        a = math.pow(self.ddx, 2)
        b = math.pow(self.ddy, 2)
        self.len = math.sqrt(a + b)
        self.lenght = u'{0:.2f}'.format(round(self.len, 2))

    def calcangle(self):
        if self.ddx == 0:
            if self.ddy < 0:
                self.angle = u'270°0\''
            else:
                self.angle = u'90°0\''
        else:
            alfa = math.fabs(math.atan(self.ddy / self.ddx) \
                             * (180 / math.pi))
            if (self.ddx > 0) and (self.ddy > 0):
                self.ang = alfa
                self.calcdegmin()
            elif (self.ddx < 0) and (self.ddy > 0):
                self.ang = 180 - alfa
                self.calcdegmin()
            elif (self.ddx < 0) and (self.ddy < 0):
                self.ang = 180 + alfa
                self.calcdegmin()
            elif (self.ddx > 0) and (self.ddy < 0):
                self.ang = 360 - alfa
                self.calcdegmin()
            elif (self.ddx > 0) and (self.ddy == 0):
                self.angle = u'0°0\''
            elif (self.ddx < 0) and (self.ddy == 0):
                self.angle = u'180°0\''

    def calcrumb(self):
        if self.ddx == 0:
            if self.ddy < 0:
                self.angle = u'З:0°0.0\''
            else:
                self.angle = u'В:0°0.0\''
        else:
            alfa = math.fabs(math.atan(self.ddy / self.ddx) * (180 / math.pi))
            #print(alfa)
            if (self.ddx > 0) and (self.ddy > 0):
                self.ang = alfa
                self.rumb = u'СВ:'
                self.calcdegmin()
            elif (self.ddx < 0) and (self.ddy > 0):
                self.ang = alfa
                self.rumb = u'ЮВ:'
                self.calcdegmin()
            elif (self.ddx < 0) and (self.ddy < 0):
                self.ang = alfa
                self.rumb = u'ЮЗ:'
                self.calcdegmin()
            elif (self.ddx > 0) and (self.ddy < 0):
                self.ang = alfa
                self.rumb = u'СЗ:'
                self.calcdegmin()
            elif (self.ddx > 0) and (self.ddy == 0):
                self.angle = u'С:0°0.0\''
            elif (self.ddx < 0) and (self.ddy == 0):
                self.angle = u'Ю:0°0.0\''

    def calcdegmin(self):
        a = int(self.ang)
        #print(a)
        minute = (self.ang - a) * 60
        if self.rumb != u'':
            self.angle = self.rumb + unicode(a) + u'°' + unicode('{0:.1f}'.format(minute)) + u'\''
            self.rumb = u''
        else:
            self.angle = unicode(a) + u'°' + unicode('{0:.1f}'.format(minute)) + u'\''


class CatalogData():

    def __init__(self, iface, is_rumb, is_onlyXY, font_size, crs):
        self.features = iface.mapCanvas().currentLayer().selectedFeatures()
        for clayer in iface.mapCanvas().layers():
            if clayer.name() == u'Точки':
                self.pointLayer = clayer
                break
            else:
                self.pointLayer = None

        self.fontsize = u'xx-small'
        if font_size == 2:
            self.fontsize = u'small'
        elif font_size == 3:
            self.fontsize = u'medium'
        elif font_size == 4:
            self.fontsize = u'large'

        self.zu_multi = []  # 1 (если полигон) или N конутуров мультполигона
        self.zu = []  # контуры текущего полигона
        self.catalog = u'<HEAD><meta http-equiv=\"Content-type\" ' \
                       u'content=\"text/html;charset=UTF-8\"><style>body table { font-size: '+self\
            .fontsize+u'; font-family: Arial;} </style><HEAD/>'
        self.geodataSVG = None
        self.geodataNewSVG = None
        self.pointDef = u'<!DOCTYPE HTML><HTML><HEAD><meta http-equiv=\"Content-type\" content=\"text/html;charset=UTF-8\"> \
                     <HEAD/><BODY><p>Нажмите \'Сохранить SVG\' для сохранения геоданных в файл.</p></br><p>Граница земельного участка проходит по поворотным точкам: '
        self.pointDefHole = u'</br>Внутренний обход {0}: '
        self.pointDefOuterRing = u'Контур {0}: '
        self.geodata_w = 420
        self.geodata_h = 297
        self.iface = iface
        self.multi = False
        self.area = []
        self.perimeter = []
        self.names = []
        self.is_rumb = is_rumb
        self.prepare_data()
        #print self.list_contours[0]
        if is_onlyXY:
            self.calculateOnlyXY()
        else:
            self.calculate()

    def isMultiPart(self, feature):
        if feature.attribute(u'order') != NULL:
            return True

    def convertCoordinate(self, point):
        #trpoint = self.transform.transform(point)
        return trpoint

    def prepare_data(self):
        # Создаётся на один объект
        nameidx = self.pointLayer.fieldNameIndex('name')
        if len(self.features) > 1:
            self.multi = True
            for feat in self.features:
                geom = feat.geometry()
                gt = QgsGeometry(geom)
                gt.transform(self.transform)
                self.names.append(feat.attributes()[nameidx])
                self.area.append(round(gt.area(), 0))
                self.perimeter.append(round(gt.length(), 2))
                #self.zu = []
                self.parse_polygon(geom.asMultiPolygon()[0])
        else:
            # #print(len(self.features))
            # geom = self.features[0].geometry()
            # self.names.append(self.features[0].attributes()[nameidx])
            # if self.isMultiPart(self.features[0]):
            #     self.multi = True
            #     multiGeom = geom.asMultiPolygon()
            #     for i in multiGeom:
            #         poly = QgsGeometry().fromPolygon(i)
            #         gt = QgsGeometry(poly)
            #         gt.transform(self.transform)
            #         #print str(poly.area())
            #         self.area.append(round(gt.area(), 0))
            #         self.perimeter.append(round(gt.length(), 2))
            #         self.zu = []
            #         #print poly
            #         self.parse_polygon(poly.asPolygon())
            # else:
            geom = self.features[0].geometry()
            gt = QgsGeometry(geom)
            self.area.append(round(gt.area(), 0))
            self.perimeter.append(round(gt.length(), 2))
            self.parse_polygon(geom.asMultiPolygon()[0])

    # полигон может содержать один внешний и от нуля до N внутренних контуров (дырок)
    def parse_polygon(self, polygon):
        zu = []
        print polygon
        for ring in polygon:
            list_ponts = []
            for node in ring:
                # Тут происходит переход к геодезической СК
                point = node
                x = round(point.y(), 2)
                y = round(point.x(), 2)
                name = u""
                for pointfeature in self.pointLayer.getFeatures():
                    if pointfeature.geometry().equals(QgsGeometry.fromPoint(QgsPoint(node.x(), node.y()))):
                        name += unicode(pointfeature.attribute(u'name'))
                list_ponts.append([x, y, name])
                print str(x) + ";" + str(y)
            zu.append(list_ponts)
        self.zu_multi.append(zu)

    def calculate(self):
        iter_contour = 0
        iter_ring = 0
        catalog_all_data = u''  # вся ведомость со всеми контурами
        for zu in self.zu_multi:
            contour_table = u''  # ведомость одного контура
            catalog_data = u''
            catalog_header = u''
            if self.multi and len(self.zu_multi) > 1:
                contour_header = u'<h3>Контур ' + unicode(iter_contour + 1) + u'</h3>'
                contour_table += contour_header
            contour_table += u'<TABLE CELLSPACING=\"0\" COLS=\"5\" BORDER=\"0\"><COLGROUP SPAN=\"5\" WIDTH=\"120\"></COLGROUP>{0}</TABLE>'
            empty = u'<TD STYLE=\"border-top: 1px solid #000000; border-bottom: 1px solid #000000; ' \
                    u'border-left: 1px solid #000000; border-right: 1px solid #000000\" HEIGHT=\"17\" ALIGN=\"CENTER\">{0}</TD>'
            catalog_header += empty.format(u'№')
            catalog_header += empty.format(u'X, м')
            catalog_header += empty.format(u'Y, м')
            if self.is_rumb:
                catalog_header += empty.format(u'Румб')
            else:
                catalog_header += empty.format(u'Дирекционный угол')
            catalog_header += empty.format(u'Расстояние, м')
            catalog_data += u'<TR>{0}</TR>'.format(catalog_header)

            for ring in zu:
                iter_node = 0
                for point in ring:
                    point_num = point[2]
                    #print point
                    if (iter_node >= 0) and (iter_node < len(ring) - 1):
                        point1 = Point(ring[iter_node][0],
                                       ring[iter_node][1])
                        point2 = Point(ring[iter_node + 1][0],
                                       ring[iter_node + 1][1])
                        measure = Measure(point1, point2, self.is_rumb)
                        catalog_data += self.decorate_value_html(
                            [point_num, ring[iter_node][0],
                             ring[iter_node][1], measure.angle,
                             measure.lenght])
                        self.zu_multi[iter_contour][iter_ring][iter_node].append(measure.angle)
                        self.zu_multi[iter_contour][iter_ring][iter_node].append(measure.lenght)

                    elif iter_node == len(ring) - 1:
                        point1 = Point(ring[iter_node - 1][0], ring[iter_node - 1][1])
                        point2 = Point(ring[0][0], ring[0][1])
                        measure = Measure(point1, point2, self.is_rumb)
                        self.zu_multi[iter_contour][iter_ring][iter_node].append(measure.angle)
                        self.zu_multi[iter_contour][iter_ring][iter_node].append(measure.lenght)
                        catalog_data += self.decorate_value_html(
                            [unicode(ring[0][2]), ring[0][0], ring[0][1], u'', u''], True)
                    iter_node += 1
                iter_ring += 1
                # Отделение 'дырки'
                if len(self.zu) > 1:
                    if iter_ring != len(self.zu):
                        catalog_data += empty.format(u'--')+empty.format(u'--')+\
                                        empty.format(u'--')+empty.format(u'--')+empty.format('--')
            catalog_all_data += catalog_data
            self.catalog += contour_table.format(catalog_data)
            self.catalog += u'<p>Площадь: {0} кв.м Периметр: {1} м</p>'.format(int(self.area[iter_contour]), self.perimeter[
                iter_contour])
            iter_contour += 1
            iter_ring = 0
        if self.multi:
            #print [iter_contour]
            self.catalog += u'<BR/><strong>Общая площадь: {0} кв.м Общий периметр: {1} м</strong>'.format(str(int(sum(self.area))),
                                                                                                 str(sum(self.perimeter)))

    def calculateOnlyXY(self):
        iter_contour = 0
        iter_ring = 0
        catalog_all_data = u''  # вся ведомость со всеми контурами

        if self.features[0].attributes()[self.features[0].fieldNameIndex('name')] <> None:
            name = self.features[0].attributes()[self.features[0].fieldNameIndex('name')]
            self.catalog += (u'<h4>Условный номер земельного участка ' + name + u'</h4>')

        if self.multi:
            self.catalog += u'<strong>Площадь земельного участка: {0} кв.м</strong>'.format(str(int(sum(self.area))))
        for zu in self.zu_multi:
            contour_table = u''  # ведомость одного контура
            catalog_data = u''
            catalog_header = u''
            if self.multi and len(self.zu_multi) > 1:
                contour_header = u'<p>Контур ' + unicode(iter_contour + 1) + u'</p>'
                contour_table += contour_header
                contour_table += u'<p>Площадь контура {0} кв.м</p>'.format(int(self.area[iter_contour]))
            else:
                contour_table += u'<p>Площадь земельного участка {0} кв.м</p>'.format(int(self.area[iter_contour]))
            contour_table += u'<TABLE CELLSPACING=\"0\" COLS=\"5\" BORDER=\"0\"><COLGROUP SPAN=\"5\" WIDTH=\"120\"></COLGROUP>{0}</TABLE>'
            empty = u'<TD STYLE=\"border-top: 1px solid #000000; border-bottom: 1px solid #000000; ' \
                    u'border-left: 1px solid #000000; border-right: 1px solid #000000\" HEIGHT=\"17\" ALIGN=\"CENTER\">{0}</TD>'

            # http://htmlbook.ru/samhtml/tablitsy/obedinenie-yacheek
            catalog_header += u'<tr><td rowspan=\"2\" style=\"border: 1px solid \">Обозначение характерных точек границ</td><td colspan=\"2\" align=center style=\"border: 1px solid; \">координаты, м</td></tr> \
            <tr><td align=center style=\"border: 1px solid \">X</td><td align=center style=\"border: 1px solid\">Y</td></tr>'
            catalog_data += (catalog_header)

            for ring in zu:
                iter_node = 0
                for point in ring:
                    point_num = point[2]
                    #print point
                    if (iter_node >= 0) and (iter_node < len(ring) - 1):
                        catalog_data += self.decorate_value_html([point_num, ring[iter_node][0], ring[iter_node][1]], False, True)
                    elif iter_node == len(ring) - 1:
                        catalog_data += self.decorate_value_html([unicode(ring[0][2]), ring[0][0], ring[0][1]], True, True)
                    iter_node += 1
                iter_ring += 1
                # Отделение 'дырки'
                if len(zu) > 1:
                    if iter_ring <> len(zu):
                        #print 'catch!'
                        catalog_data += empty.format(u'внутренний обход')+empty.format(u'')+empty.format(u'')
            catalog_all_data += catalog_data
            self.catalog += contour_table.format(catalog_data)

            iter_contour += 1
            iter_ring = 0

    def decorate_value_html(self, value, last=False, onlyXY=False):
        row1 = u'<TR>{0}</TR>'
        row2 = u'<TR>{0}</TR>'
        empty = u'<TD STYLE=\"border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: ' \
                u'1px solid #000000; border-right: 1px solid #000000\" HEIGHT=\"17\" ALIGN=\"CENTER\">{0}</TD>'
        emptyCoord = u'<TD STYLE=\"border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: ' \
                u'1px solid #000000; border-right: 1px solid #000000\" HEIGHT=\"17\" ALIGN=\"CENTER\">{:d}</TD>'
        # https://mkaz.com/2012/10/10/python-string-format/
        num = empty.format(value[0])
        #sx = '{:.2f}'.format(value[1])
        x = emptyCoord.format(int(math.ceil(value[1])))
        #sy = '{:.2f}'.format(value[2])
        y = emptyCoord.format(int(math.ceil(value[2])))
        if onlyXY:
            pass
        else:
            a = empty.format(value[3])
            l = empty.format(value[4])
        if onlyXY:
            data1 = num + x + y
            return row1.format(data1)
        else:
            data1 = num + x + y + empty.format('</BR>') + empty.format('</BR>')
            data2 = empty.format('</BR>') + empty.format('</BR>') + empty.format('</BR>') + a + l
            if not last:
                return row1.format(data1) + row2.format(data2)
            else:
                return row1.format(data1)

    def createSvgGeodata(self, path = os.path.abspath(os.path.dirname(__file__))):
        #self.geodataSVG = drawing.Drawing(path, profile='tiny')
        self.geodataNewSVG = drawing.Drawing(path + 'new', size=('210mm','297mm'), profile='full')
        #self.createTableSvg(self.geodataSVG)
        self.createNewTableSvg(self.geodataNewSVG)
        #self.geodataSVG.save()
        #print path

    # http://nullege.com/codes/search/svgwrite.Drawing.rect

    def createTableSvg(self, canvas):
        step = 3.5
        place = step
        limit = 200
        iter_point = 0
        iter_contour = 1
        if self.features[0].attributes()[self.features[0].fieldNameIndex('name')] <> None:
            name = self.features[0].attributes()[self.features[0].fieldNameIndex('name')]
            canvas.add(canvas.text(name, insert=(5 * mm, 5 * mm), fill='black',
                                   font_family='Arial', font_size='11'))
        for zu in self.zu_multi:
            if len(self.zu_multi) > 1:
                # наименование контура

                cntName = u'Контур ' + unicode(iter_contour)
                canvas.add(canvas.text(cntName, insert=(5 * mm, (8 + place) * mm), fill='black',
                                       font_family='Arial', font_size='11'))
                place += step
            # заголовок таблицы ЗУ
            canvas.add(canvas.rect(size=(15 * mm, 3.5 * mm), insert=(5 * mm, (5 + place) * mm), stroke='black',
                                fill='none', stroke_width=0.35 * mm))
            canvas.add(canvas.rect(size=(15 * mm, 3.5 * mm), insert=(20 * mm, (5 + place) * mm), stroke='black',
                                fill='none', stroke_width=0.35 * mm))
            canvas.add(canvas.rect(size=(15 * mm, 3.5 * mm), insert=(35 * mm, (5 + place) * mm), stroke='black',
                                fill='none', stroke_width=0.35 * mm))
            canvas.add(
                canvas.text(u'№ точки', insert=(5.3 * mm, (7.5 + place) * mm),
                            fill='black', font_family='Arial', font_size='9'))
            if self.is_rumb:
                ar = u'Румб'
            else:
                ar = u'Дир. угол'
            canvas.add(
                canvas.text(ar, insert=(20.3 * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                            font_size='9'))
            canvas.add(
                canvas.text(u'Расст, м', insert=(35.3 * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                            font_size='9'))
            place += step
            iter_ring = 0
            for ring in zu:
                if len(zu) > 1 and iter_ring > 0:
                    # строка-разделитель контуров
                    row_n = canvas.rect(size=(15 * mm, 3.5 * mm), insert=(5 * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_a = canvas.rect(size=(15 * mm, 3.5 * mm), insert=(20 * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_l = canvas.rect(size=(15 * mm, 3.5 * mm), insert=(35 * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    canvas.add(row_n)
                    canvas.add(row_a)
                    canvas.add(row_l)
                    canvas.add(
                        canvas.text('-', insert=(5.3 * mm, (7.5 + place) * mm),
                                    fill='black', font_family='Arial', font_size='9'))
                    canvas.add(
                        canvas.text('-', insert=(20.3 * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                                    font_size='9'))
                    canvas.add(
                        canvas.text('-', insert=(35.3 * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                                    font_size='9'))
                    place += step

                iter_point = 0
                for point in ring:
                    if iter_point == len(ring) - 1:
                        continue
                    # строки с данными
                    row_n = canvas.rect(size=(15 * mm, 3.5 * mm), insert=(5 * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_a = canvas.rect(size=(15 * mm, 3.5 * mm), insert=(20 * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_l = canvas.rect(size=(15 * mm, 3.5 * mm), insert=(35 * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    canvas.add(row_n)
                    canvas.add(row_a)
                    canvas.add(row_l)
                    canvas.add(
                        canvas.text(point[2] + '-' + ring[iter_point+1][2], insert=(5.3 * mm, (7.5 + place) * mm),
                                    fill='black', font_family='Arial', font_size='9'))
                    canvas.add(
                        canvas.text(point[3], insert=(20.3 * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                                    font_size='9'))
                    canvas.add(
                        canvas.text(point[4], insert=(35.3 * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                                    font_size='9'))
                    place += step
                    iter_point += 1
                iter_ring += 1
            canvas.add(canvas.text(u'Площадь земельного участка: '+str(int(self.area[iter_contour-1]))+u'кв.м', insert=(5.3 * mm, (7.5 + place) * mm),
                                   fill='black', font_family='Arial', font_size='9'))
            place += step
            iter_contour +=1

    # Для новой схемы расположения ЗУ
    def createNewTableSvg(self, canvas):
        step = 3.5 # шаг таблицы геоданных
        step_v = 77 # шаг нового столбца
        place = step # горизонтальное положение
        place_v = 0 # вертикальное положение
        limit = 260 # максимальный размер высоты страницы для геоданных
        iter_point = 0
        iter_contour = 1
        # print self.features[0].attributes()[self.features[0].fieldNameIndex('name')] == None
        if self.features[0].attributes()[self.features[0].fieldNameIndex('name')] <> None:
            name = self.features[0].attributes()[self.features[0].fieldNameIndex('name')]
            canvas.add(canvas.text(u'Условный номер земельного участка ' + name, insert=(5 * mm, 7.5 * mm), fill='black',
                                   font_family='Arial', font_size='11'))
            place += step
        canvas.add(canvas.text(u'Площадь земельного участка  ' + str(int(sum(self.area))).encode('utf-8') + u' кв.м', insert=(5 * mm, (place + 7.5) * mm), fill='black',
                                   font_family='Arial', font_size='11'))
        place += step
        for zu in self.zu_multi:
            if len(self.zu_multi) > 1:
                # Описание границ
                self.pointDef += ('</br>' + self.pointDefOuterRing.format(iter_contour))

                cntName = u'Контур ' + unicode(iter_contour)
                canvas.add(canvas.text(cntName, insert=(5 * mm, (8 + place) * mm), fill='black',
                                       font_family='Arial', font_size='11'))
                place += step
                canvas.add(canvas.text(u'Площадь контура '+str(int(self.area[iter_contour-1]))+u' кв.м', insert=((5.3 + place_v) * mm, (7.5 + place) * mm),
                                   fill='black', font_family='Arial', font_size='9'))
                place += step
            # заголовок таблицы ЗУ
            canvas.add(canvas.rect(size=(25 * mm, 7 * mm), insert=(5 * mm, (5 + place) * mm), stroke='black',
                                fill='none', stroke_width=0.35 * mm))
            canvas.add(canvas.rect(size=(50 * mm, 3.5 * mm), insert=(30 * mm, (5 + place) * mm), stroke='black',
                                fill='none', stroke_width=0.35 * mm))
            canvas.add(canvas.rect(size=(25 * mm, 3.5 * mm), insert=(30 * mm, (8.5 + place) * mm), stroke='black',
                                fill='none', stroke_width=0.35 * mm))
            canvas.add(canvas.rect(size=(25 * mm, 3.5 * mm), insert=(55 * mm, (8.5 + place) * mm), stroke='black',
                                fill='none', stroke_width=0.35 * mm))
            canvas.add(
                canvas.text(u'Обозначение харак-', insert=(5.3 * mm, (7.5 + place) * mm),
                            fill='black', font_family='Arial', font_size='9'))
            canvas.add(
                canvas.text(u'терных точек границ', insert=(5.3 * mm, (10+ place) * mm),
                            fill='black', font_family='Arial', font_size='9'))

            canvas.add(
                canvas.text(u'координаты, м', insert=(45 * mm, (7 + place) * mm),
                            fill='black', font_family='Arial', font_size='9'))

            canvas.add(
                canvas.text(u'X', insert=(40 * mm, (11 + place) * mm), fill='black', font_family='Arial',
                            font_size='9'))
            canvas.add(
                canvas.text(u'Y', insert=(65.3 * mm, (11 + place) * mm), fill='black', font_family='Arial',
                            font_size='9'))
            place += step
            place += step
            iter_ring = 0
            for ring in zu:
                if(place >= limit):
                    place = step
                    place_v += step_v

                if len(zu) > 1 and iter_ring > 0:
                    # Описание границ
                    self.pointDef += self.pointDefHole.format(iter_ring)

                    # строка-разделитель контуров
                    row_n = canvas.rect(size=(25 * mm, 3.5 * mm), insert=((5 + place_v) * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_x = canvas.rect(size=(25 * mm, 3.5 * mm), insert=((30 + place_v) * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_y = canvas.rect(size=(25 * mm, 3.5 * mm), insert=((55 + place_v) * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    canvas.add(row_n)
                    canvas.add(row_x)
                    canvas.add(row_y)
                    canvas.add(canvas.text(u'внутренний обход', insert=((place_v + 6) * mm, (7.5 + place) * mm),
                                    fill='black', font_family='Arial', font_size='9'))
                    place += step

                iter_point = 0
                for point in ring:

                    if iter_point == len(ring) - 1:
                        # Описание границ
                        self.pointDef += point[2]
                        #continue
                    else:
                        self.pointDef += point[2] + u', '
                    # строки с данными
                    if(place >= limit):
                        place = step
                        place_v += step_v
                    row_n = canvas.rect(size=(25 * mm, 3.5 * mm), insert=((5 + place_v) * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_x = canvas.rect(size=(25 * mm, 3.5 * mm), insert=((30 + place_v) * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    row_y = canvas.rect(size=(25 * mm, 3.5 * mm), insert=((55 + place_v) * mm, (5 + place) * mm), stroke='black',
                                        fill='none', stroke_width=0.35 * mm)
                    canvas.add(row_n)
                    canvas.add(row_x)
                    canvas.add(row_y)
                    canvas.add(
                        canvas.text(point[2], insert=((place_v + 6) * mm, (7.5 + place) * mm),
                                    fill='black', font_family='Arial', font_size='9'))
                    canvas.add(
                        canvas.text(str(int(math.ceil(point[0]))), insert=((30.3 + place_v) * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                                    font_size='9'))
                    canvas.add(
                        canvas.text(str(int(math.ceil(point[1]))), insert=((55.3 + place_v) * mm, (7.5 + place) * mm), fill='black', font_family='Arial',
                                    font_size='9'))

                    place += step
                    iter_point += 1
                iter_ring += 1

            place += step
            iter_contour +=1
        #self.pointDef += '</p></BODY></HTML>'
