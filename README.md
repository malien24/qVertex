# qVertex

Плагин для QGIS автоматизирующий некторые рутинные операции при землеустроительнм проектировании и кадастровых работах.

![Внешний вид](/screen.png)

Чтобы начать использовать плагин, скачайте архив ZIP с этой страницы, разархивируйте его и скопируйте папку QVertex из него в папку с плагинами QGIS. Перезапустите QGIS и вы увидите плагин в списке установленных.

Плагин состоит из кода на языке python и шаблонных проектов QGIS (пока проект один - landplan.qgs).

Проекты находятся в папке /start. Содержимое всей этой папки копируется в указанную пользователем папку при использования инструмента **Создать проект**. Вы можете изменять шаблонный проект, добавляя или удаляя нужные вам слои, менять систему координат, создавать, изменять и удалять Макеты QGIS.

В проекте обязательно должны присутствовать:
* Точечный слой "Точки"
* Линейный слой "Части границ"
* Полигональный слои "ЗУ"
* Полигональный слои "Кадастр"

Без них невозможна работа большинства инструментов плагина.

В папке /start/data находятся SpatiaLite-база, таблицы из которой включены в проект QGIS. Все таблицы в WGS-84.

На данный момент модуль позволяет:
* Автоматически создавать характерные точки, с автоматическим определением новые или они или нет, при наличии объектов на слое "Кадастр"
* Автоматически создавать части границ, с автоматическим определением новые или они или нет, при наличии объектов на слое "Кадастр" и "Точки"
* Вставлять узлы в земельные участи, в местах примыкания частей земельных участков
* Создавать ведомость координат в форматах HTML и SVG для схемы расположения ЗУ по 762 приказу
* Создавать CSV-файл для Технокад-Экспресс. В таком файле пережаётся намного больше информации чем в MID/MIF
