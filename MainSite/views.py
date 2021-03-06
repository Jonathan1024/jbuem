from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
import csv
from django.http import StreamingHttpResponse
from MainSite .models import Solar, Meter, Pyranometer, \
    Wind, EnphaseTotals, FroniusTotals, WindTotals, MeterTotals
import json
import datetime
import time
# Create your views here.


def index(request):
    kandz = 0
    eppely = 0
    test1 = [[1138683600000, 7.2800122043237], [1141102800000, 7.1187787503354], [1143781200000, 8.351887016482]]

    meter = Meter.objects.order_by('-time_stamp')[0]
    solar = Solar.objects.order_by('-time_stamp')[0]
    wind = Wind.objects.order_by('-time_stamp')[0]

    solar_today = Solar.objects.order_by('-time_stamp')[0:5760]
    meter_today = Meter.objects.order_by('-time_stamp')[0:5760]

    moder = 10

    enphase_today_array = []
    counter = 0
    for i in solar_today:
        counter = counter + 1
        if counter % moder == 0:
            enphase_today_array.append([int(time.mktime(i.time_stamp.timetuple()))*1000, float(i.enphase_power)])

    fronius_today_array = []
    counter = 0
    for i in solar_today:
        counter = counter + 1
        if counter % moder == 0:
            fronius_today_array.append([int(time.mktime(i.time_stamp.timetuple()))*1000, float(i.fronius_power)])

    meter_today_array = []
    counter = 0
    for i in meter_today:
        counter = counter + 1
        if counter % moder == 0:
            meter_today_array.append([int(time.mktime(i.time_stamp.timetuple()))*1000, float(i.btc_power)*1000])



    total_power = int(solar.fronius_power) + int(solar.enphase_power)

    context = {
        'enphasePower': solar.enphase_power,
        'froniusPower': solar.fronius_power,
        'selPower': meter.btc_power,
        'kandz': kandz,
        'eppely': eppely,
        'windPower': wind.wind_power,
        'totalPower': total_power,
        'test': test1,
        'enphase_array':enphase_today_array,
        'fronius_array':fronius_today_array,
        'meter_array':meter_today_array,
    }

    return render(request, 'MainSite/index.html', context)


def test(request):
    var = Wind.objects.all() # Show all in Wind

    today_data = Meter.order_by('-time_stamp').filter(time_stamp__lte=datetime.date.today())
    today_meter = []
    for i in today_data:
        today_meter.append(i.btc_power)

    var = Meter.objects.order_by('-time_stamp')[0]

    context = {
        'test': today_meter
    }
    return render(request, 'MainSite/test.html', context)


def btc(request):

    meter = Meter.objects.order_by('-time_stamp')[0]
    btc_power = meter.btc_power

    context = {
        'btc_power': btc_power,
    }

    return render(request, 'MainSite/btc.html', context)


def solar(request):

    solar = Solar.objects.order_by('-time_stamp')[0]

    enphase_power = solar.enphase_power
    fronius_power = solar.fronius_power

    context = {
        'enphase_power': enphase_power,
        'fronius_power': fronius_power,
    }

    return render(request, 'MainSite/solar.html', context)


def wind(request):

    wind_today = Wind.objects.order_by('-time_stamp')[0:17280]

    wind_current = wind_today[0].wind_power
    wind_speed = wind_today[0].wind_speed
    current_temperature = wind_today[0].temperature
    wind_direction = wind_today[0].wind_direction

    moder = 10

    wind_today_array = []
    counter = 0
    for i in wind_today:
        counter = counter + 1
        if counter % moder == 0:
            wind_today_array.append([int(time.mktime(i.time_stamp.timetuple()))*1000, float(i.wind_power)])


    context = {
        'wind_today': wind_today_array,
        'wind_current_power': wind_current,
        'wind_speed': wind_speed,
        'current_temperature': current_temperature,
        'wind_direction': wind_direction,
    }

    return render(request, 'MainSite/wind.html', context)


def dashboard1(request):

    meter = Meter.objects.order_by('-time_stamp')[0]
    solar = Solar.objects.order_by('-time_stamp')[0]
    wind = Wind.objects.order_by('-time_stamp')[0]
    enphase_totals = EnphaseTotals.objects.order_by('-time_stamp')[0]
    fronius_totals = FroniusTotals.objects.order_by('-time_stamp')[0]
    grid_totals = MeterTotals.objects.order_by('-time_stamp')[0]
    wind_totals = WindTotals.objects.order_by('-time_stamp')[0]

    daily_total = float(wind_totals.daily_total) + float(enphase_totals.daily_total) + float(fronius_totals.daily_total) + (float(grid_totals.daily_total) * 1000)
    wind_daily_percent = (float(wind_totals.daily_total)/daily_total) * 100
    fronius_daily_percent = (float(fronius_totals.daily_total)/daily_total) * 100
    enphase_daily_percent = (float(enphase_totals.daily_total)/daily_total) * 100
    grid_daily_percent = ((float(grid_totals.daily_total) * 1000)/daily_total) * 100

    total_daily_percent = wind_daily_percent + fronius_daily_percent + enphase_daily_percent + grid_daily_percent

    if wind_daily_percent < 0:
        wind_daily_percent = 0

    if total_daily_percent > 99.9:
        diff = total_daily_percent - 99.9
        grid_daily_percent = grid_daily_percent - diff

    weekly_total = float(wind_totals.weekly_total) + float(enphase_totals.weekly_total) + float(fronius_totals.weekly_total) + (float(grid_totals.weekly_total)*1000)
    wind_weekly_percent = (float(wind_totals.weekly_total)/weekly_total) * 100
    fronius_weekly_percent = (float(fronius_totals.weekly_total)/weekly_total) * 100
    enphase_weekly_percent = (float(enphase_totals.weekly_total)/weekly_total) * 100
    grid_weekly_percent = ((float(grid_totals.weekly_total)*1000)/weekly_total) * 100

    total_weekly_percent = wind_weekly_percent + fronius_weekly_percent + enphase_weekly_percent + grid_weekly_percent

    if wind_weekly_percent < 0:
        wind_weekly_percent = 0

    if total_weekly_percent > 99.9:
        diff = total_weekly_percent - 99.9
        grid_weekly_percent = grid_weekly_percent - diff

    monthly_total = float(wind_totals.monthly_total) + float(enphase_totals.monthly_total) + float(fronius_totals.monthly_total) + (float(grid_totals.monthly_total)*1000)
    wind_monthly_percent = (float(wind_totals.monthly_total)/monthly_total) * 100
    enphase_monthly_percent = (float(enphase_totals.monthly_total)/monthly_total) * 100
    fronius_monthly_percent = (float(fronius_totals.monthly_total)/monthly_total) * 100
    grid_monthly_percent = ((float(grid_totals.monthly_total)*1000)/monthly_total) * 100

    total_monthly_percent = wind_monthly_percent + fronius_monthly_percent + enphase_monthly_percent + grid_monthly_percent

    if wind_monthly_percent < 0:
        wind_monthly_percent = 0

    if total_monthly_percent > 99.9:
        diff = total_monthly_percent - 99.9
        grid_monthly_percent = grid_monthly_percent - diff

    yearly_total = float(wind_totals.yearly_total) + float(enphase_totals.yearly_total) + float(fronius_totals.yearly_total) + (float(grid_totals.yearly_total)*1000)
    wind_yearly_percent = (float(wind_totals.yearly_total)/yearly_total) * 100
    enphase_yearly_percent = (float(enphase_totals.yearly_total)/yearly_total) * 100
    fronius_yearly_percent = (float(fronius_totals.yearly_total)/yearly_total) * 100
    grid_yearly_percent = ((float(grid_totals.yearly_total)*1000)/yearly_total) * 100

    total_yearly_percent = wind_yearly_percent + fronius_yearly_percent + enphase_yearly_percent + grid_yearly_percent

    if wind_yearly_percent < 0:
        wind_yearly_percent = 0

    if total_yearly_percent > 99.9:
        diff = total_yearly_percent - 99.9
        grid_yearly_percent = grid_yearly_percent - diff

    context = {
        'current_solar_enphase': solar.enphase_power,
        'current_solar_fronius': solar.fronius_power,
        'current_wind': wind.wind_power,
        'current_grid': meter.btc_power,
        'daily_enphase':enphase_totals.daily_total,
        'weekly_enphase': enphase_totals.weekly_total,
        'monthly_enphase': enphase_totals.monthly_total,
        'yearly_enphase': enphase_totals.yearly_total,
        'daily_fronius':fronius_totals.daily_total,
        'weekly_fronius': fronius_totals.weekly_total,
        'monthly_fronius': fronius_totals.monthly_total,
        'yearly_fronius': fronius_totals.yearly_total,
        'daily_grid':grid_totals.daily_total,
        'weekly_grid': grid_totals.weekly_total,
        'monthly_grid': grid_totals.monthly_total,
        'yearly_grid': grid_totals.yearly_total,
        'daily_wind': wind_totals.daily_total,
        'weekly_wind': wind_totals.weekly_total,
        'monthly_wind': wind_totals.monthly_total,
        'yearly_wind': wind_totals.yearly_total,
        'wind_daily_percent': wind_daily_percent,
        'fronius_daily_percent': fronius_daily_percent,
        'enphase_daily_percent': enphase_daily_percent,
        'grid_daily_percent': grid_daily_percent,
        'wind_weekly_percent': wind_weekly_percent,
        'fronius_weekly_percent': fronius_weekly_percent,
        'enphase_weekly_percent': enphase_weekly_percent,
        'grid_weekly_percent': grid_weekly_percent,
        'wind_monthly_percent': wind_monthly_percent,
        'fronius_monthly_percent': fronius_monthly_percent,
        'enphase_monthly_percent': enphase_monthly_percent,
        'grid_monthly_percent': grid_monthly_percent,
        'wind_yearly_percent': wind_yearly_percent,
        'fronius_yearly_percent': fronius_yearly_percent,
        'enphase_yearly_percent': enphase_yearly_percent,
        'grid_yearly_percent': grid_yearly_percent,
    }

    return render(request, 'MainSite/dashboard1.html', context)
