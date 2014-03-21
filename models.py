#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.db import models
from django.template import Context
from django.template.loader import get_template_from_string
from helpers import week_day, padd_to


class WeekScheduleField(models.CharField):
    pass


class ScheduleModel(models.Model):
    schedule = WeekScheduleField(u'режим работы', default=u'F'*24*7, max_length=24*7, validators=[RegexValidator(regex='^.{%d}$'%(24*7), message='Length has to be %d'%(24*7), code='invalid')], null=True, blank=True)

    def __unicode__(self):
        return u'; '.join(u'%s %s %s' % (element[0], element[1], (u'пер. %s' % u', '.join(u'%s' % rest_time for rest_time in element[2])) if len(element[2]) else u'') for element in self.get_text_schedule_list())

    def get_day_schedule(self, day_str):
        len_day_str = len(day_str)
        if len_day_str != 24:
            raise BaseException('Wrong length of day string %d' % len_day_str)

        previous = None
        rest_intervals = []
        rest_interval = []
        begin_work = None
        end_work = None

        for hour in xrange(24):
            hour_bin_str = padd_to(str(bin(int(day_str[hour], 16)))[2:], 4)
            for part_minutes in xrange(4):
                minutes_is_work = int(hour_bin_str[part_minutes])
                time_minutes = 15*part_minutes

                if previous is None and minutes_is_work:
                    begin_work = [0, time_minutes]

                if previous is not None and previous and not minutes_is_work: #10
                    end_work = [hour, time_minutes]
                    rest_interval.append([hour, 0])

                elif previous is not None and not previous and minutes_is_work: #01
                    if begin_work is None:
                        begin_work = [hour, time_minutes]
                    if len(rest_interval):
                        rest_interval.append([hour, time_minutes])
                        rest_intervals.append(rest_interval)
                        rest_interval = []

                elif previous is not None and previous and minutes_is_work:
                    end_work = [hour+1, 0] if part_minutes == 3 else [hour, time_minutes]

                previous = minutes_is_work

        return [begin_work, end_work, rest_intervals]

    def get_week_schedule(self):
        result = []
        if self.schedule is not None:
            len_week_str = len(self.schedule)
            if len_week_str != 7*24:
                raise BaseException('Wrong length of week string %d' % len_week_str)

            result = []
            for day in xrange(7):
                result.append([day, self.get_day_schedule(self.schedule[day*24:(day+1)*24])])

        return result

    def get_text_schedule_list(self):
        result = []
        group_days_list = []
        for day in self.get_week_schedule():
            exist_in_group = False
            for group_day in group_days_list:
                if day[1] == group_day[1]:
                    group_day[0].append(day[0])
                    exist_in_group = True
                    break
            if not exist_in_group:
                group_days_list.append([[day[0]], day[1]])

        for group_days in group_days_list:
            days = u', '.join(u'%s' % week_day(day, 3) for day in group_days[0])
            rest_day = False
            rest_times_list = []
            if group_days[1][0] is not None and group_days[1][1] is not None:
                work_time = u'%d:%02d - %d:%02d' % (group_days[1][0][0], group_days[1][0][1], group_days[1][1][0], group_days[1][1][1])
                len_rest_times = len(group_days[1][2])
                if len_rest_times:
                    rest_times_list = [u'%d:%02d - %d:%02d' % (rest_time[0][0], rest_time[0][1], rest_time[1][0], rest_time[1][1]) for rest_time in group_days[1][2]]
            else:
                work_time = u'выходной'
                rest_day = True

            result.append([days, work_time, rest_times_list, rest_day])

            result.sort(key=lambda item: item[3])
        return result

    @staticmethod
    def get_text_schedule(text_schedule_list):
        if len(text_schedule_list):
            return u'; '.join(u'%s %s %s' % (element[0], element[1], (u'пер. %s' % u', '.join(u'%s' % rest_time for rest_time in element[2])) if len(element[2]) else u'') for element in text_schedule_list)
        else:
            return u''

    @staticmethod
    def get_html_table_schedule(text_schedule_list):
        if len(text_schedule_list):
            html_template = u'<div class="schedule"><table cellpadding="0" cellspacing="0" border="0"><tr class="header"><td>Режим</td><td>Раб. время</td><td>Перерыв</td></tr>{% for day in days %}<tr {% if day.3 %}class="rest"{% endif %}><td class="header">{{ day.0 }}</td><td>{{ day.1 }}</td><td>{% if day.2|length %}{% for rest_time in day.2 %}{{ rest_time }}{% if not forloop.last %}<br>{% endif %}{% endfor %}{% else %}-{% endif %}</td></tr>{% endfor %}</table></div>'
            template = get_template_from_string(html_template)
            html = template.render(Context({'days': text_schedule_list}))
            return html
        else:
            return u''

    class Meta:
        abstract = True