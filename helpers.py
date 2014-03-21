#!/usr/bin/python
# -*- coding: utf-8 -*-

def padd_to(input_str, pad_len, filler=u'0'):
    str_len = len(input_str)
    if str_len < pad_len:
        input_str = u'%s%s' % (filler*(pad_len-str_len), input_str)
    return input_str


def week_day(day=0, form=0):
    if not isinstance(day, int) or not isinstance(form, int):
        raise StandardError(u'day or form is not integer value')
    days = (
        (u'субботу', u'прошлую субботу', u'пр. суб.', u'суб.', u'суббота'),
        (u'воскресенье', u'прошлое воскресенье', u'пр. воск.', u'воск.', u'воскресенье'),
        (u'понедельник', u'прошлый понедельник', u'пр. пон.', u'пон.', u'понедельник'),
        (u'вторник', u'прошлый вторник', u'пр. вт.', u'вт.', u'вторник'),
        (u'среду', u'прошлую среду', u'пр. ср.', u'ср.', u'среда'),
        (u'четверг', u'прошлый четверг', u'пр. чет.', u'чет.', u'четверг'),
        (u'пятницу', u'прошлую пятницу', u'пр. пят.', u'пят.', u'пятница'),
        (u'неизвестный день', u'неизвестный день', u'н.д.', u'н.д.', u'неизвестный день')
    )
    return days[day][form]
