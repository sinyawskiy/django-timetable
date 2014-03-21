django-timetable
================

Widget расписание в django-admin
---------------------------------------

Данный виджет позволяет более ли менее удобно заполнять, хранить расписание работы с точностью до 15 минут (точность выбиралась из необходимости быстрого поиска организаций по времени работы и поэтому одна запись должна была укалдываться в 255 символов индекса) и выводить его в нормальном формате, текстовом или в html табличке:

Режим | Раб. время | Перерыв
------|------------|-------
суб., воск.|14:00 - 14:30|	-
пон., вт., ср., чет., пят.|7:45 - 19:45	|13:00 - 14:00

В Django admin табличка и control выглядит так:

![Example](https://raw.githubusercontent.com/sinyawskiy/django-timetable/master/img/example.png)


Определение модели
------------------

При определении класса в `models.py` нужно отнаследоваться от `ScheduleModel`

Внесем изменения в файл `models.py`:
```
#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime-widget.models import ScheduleModel


class InfoSchedule(ScheduleModel):
    pass
```

При это у класса появится поле `schedule` это обычный CharField, в котором будет храниться все недельное время работы в 16-ричном (HEX) формате, если перевести в двоичный получим 10001001...001001. Каждый 0 или 1 в этой последовательности означает 15 минут и является флагом для этого времени. Это основной момент реализации.

Использования в приложении Django admin
---------------------------------------
Для правильно отображения в приложении Django admin нужно в файле `admin.py` добавить статику путь к файлу
`schedule_admin_widget.js`. Также нужно указать класс формы в которой определен виджет:

Отредактируем файл `admin.py`:
```
#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from models import InfoSchedule
from forms import InfoScheduleAdminForm


class InfoScheduleAdmin(admin.ModelAdmin):
    model = InfoSchedule
    form = InfoScheduleAdminForm
    
    class Media:
        js = ('%sjs/schedule_admin_widget.js'%settings.STATIC_URL,)
    
admin.site.register(InfoSchedule, InfoScheduleAdmin)
```
Создадим форму `InfoScheduleAdminForm` в файле `forms.py`:
```
#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from datetime-widget.widgets import ScheduleWidget

class InfoScheduleAdminForm(forms.ModelForm):
    schedule = forms.CharField(widget=ScheduleWidget, label=u'Расписание на неделю', required=False)
```

Использоваение модели:
У абстрактного класса ScheduleModel определены статические методы:
```
    @staticmethod
    def get_text_schedule(text_schedule_list):
        ...

    @staticmethod
    get_html_table_schedule(text_schedule_list):
        ...
```
в эти методы в качестве аргумента необходимо передать список получаемый из метода `get_text_schedule_list()` объекта класса `ScheduleModel` в данном случае `InfoSchedule`
