from django.contrib import admin
from models import Wind, Solar
from django.http import HttpResponse
from django.utils.encoding import smart_str
import csv


def solar_data_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = solar_data.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u'ID'),
        smart_str(u'time_stamp'),
        smart_str(u'enphase_power'),
        smart_str(u'fronius_power')
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.id),
            smart_str(obj.time_stamp),
            smart_str(obj.enphase_power),
            smart_str(obj.fronius_power)
        ])
    return response


def wind_data_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename = wind_data.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u'ID'),
        smart_str(u'time_stamp'),
        smart_str(u'wind_speed'),
        smart_str(u'wind_direction'),
        smart_str(u'humidity'),
        smart_str(u'temperature'),
        smart_str(u'wind_power')
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.id),
            smart_str(obj.time_stamp),
            smart_str(obj.wind_speed),
            smart_str(obj.wind_direction),
            smart_str(obj.humidity),
            smart_str(obj.temperature),
            smart_str(obj.wind_power)
        ])
    return response


wind_data_csv.short_description = u'Wind Data CSV Download'
solar_data_csv.short_description = u'Solar Data CSV Download'


class ModelAdmin(admin.ModelAdmin):
    actions = [wind_data_csv, solar_data_csv]


# Register your models here.
#admin.site.register(Wind, ModelAdmin)
#admin.site.register(Solar, ModelAdmin)

