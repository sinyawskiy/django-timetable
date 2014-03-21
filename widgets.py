#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from helpers import week_day


class ScheduleWidget(forms.TextInput):
    def __init__(self, *args, **kw):
        super(ScheduleWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, field, value, *args, **kwargs):
        if value is None:
            value = u'0'*24*7

        days = []
        time_list_header = []
        for hour in xrange(24):
            for minutes in xrange(2):
                time_list_header.append({
                    'time': u'%02d:<br>%02d' % (hour, minutes*30),
                    'data_time': 'time_%d_' % hour,
                    'data_part': '%d' % minutes
                })

        for day in xrange(7):
            time_list = []
            for hour in xrange(24):
                hour_bin_str = paddTo(str(bin(int(value[day*24+hour], 16)))[2:],4)
                for part_minutes in xrange(4):
                    minutes_is_work = int(hour_bin_str[part_minutes])
                    time_minutes = 15*part_minutes
                    time_list.append({
                        'time': u'%02d:%02d' % (hour, time_minutes),
                        'data_time': 'time_%d_%d' % (hour, part_minutes),
                        'name': '%d_%d_%d' % (day, hour, part_minutes),
                        'is_checked': minutes_is_work
                    })
            days.append({
                'data_day': 'day_%d' % day,
                'name': week_day(day, 3),
                'number': day,
                'time_list': time_list,
            })

        template = get_template('schedule_admin_widget.html')
        html = self.inner_widget.render(field, value)
        html += template.render(Context({'days': days, 'time_list_header': time_list_header, 'divider': xrange(2)}))
        return mark_safe(html)