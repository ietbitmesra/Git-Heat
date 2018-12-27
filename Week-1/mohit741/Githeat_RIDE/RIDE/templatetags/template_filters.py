""" This module is used to create custom template tags to display tables using JSON data
    It really simplifies the process of creating tables using dicts """

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# To make stations table
@register.simple_tag
def make_table(stations):
    res = ''
    for key in stations['Arrives'].keys():
        res += '<tr>'
        for value in stations:
            res = res + '<td>' + str(stations[value][key]) + '</td>'
        res += '</tr>'

    return mark_safe(res)


# To make fares table
@register.simple_tag
def make_fare_table(fares):
    res = '<thead><tr>'
    for key in fares.keys():
        if key == '0':
            res += '<th>Type</th>'
        else:
            res += '<th>' + str(fares[key]['0']) + '</th>'
    res += '</tr></thead><tbody>'
    for i in range(1, 7):
        res += '<tr>'
        for key in fares.keys():
            if str(fares[key][str(i)]) == 'None':
                res = res + '<td>' + '-' + '</td>'
            else:
                res = res + '<td>' + str(fares[key][str(i)]) + '</td>'
        res += '</tr>'
    res += '<tbody>'

    return mark_safe(res)
