from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
import csv
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from MainSite .models import Solar, Meter, Pyranometer, \
    Wind, EnphaseTotals, FroniusTotals, WindTotals, MeterTotals
import json
import datetime
# Create your views here.


def index(request):
    datetime = 0
    kandz = 0
    eppely = 0

    meter = Meter.objects.order_by('-time_stamp')[0]
    solar = Solar.objects.order_by('-time_stamp')[0]
    wind = Wind.objects.order_by('-time_stamp')[0]

    total_power = int(solar.fronius_power) + int(solar.enphase_power)

    context = {
        'enphasePower': solar.enphase_power,
        'froniusPower': solar.fronius_power,
        'selPower': meter.btc_power,
        'datetime': datetime,
        'kandz': kandz,
        'eppely': eppely,
        'windPower': wind.wind_power,
        'totalPower': total_power,
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

    dummydata = [ [ 1138683600000 , 7.2800122043237] , [ 1141102800000 , 7.1187787503354] , [ 1143781200000 , 8.351887016482] ]

    context = {
        'btc_power': dummydata
    }

    return render(request, 'MainSite/btc.html', context)


def solar(request):

    context = {
    }

    return render(request, 'MainSite/solar.html', context)


def wind(request):

    context = {
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

    if wind_daily_percent < 0:
        wind_daily_percent = 0

    weekly_total = float(wind_totals.weekly_total) + float(enphase_totals.weekly_total) + float(fronius_totals.weekly_total) + (float(grid_totals.weekly_total)*1000)
    wind_weekly_percent = (float(wind_totals.weekly_total)/weekly_total) * 100
    fronius_weekly_percent = (float(fronius_totals.weekly_total)/weekly_total) * 100
    enphase_weekly_percent = (float(enphase_totals.weekly_total)/weekly_total) * 100
    grid_weekly_percent = ((float(grid_totals.weekly_total)*1000)/weekly_total) * 100

    if wind_weekly_percent < 0:
        wind_weekly_percent = 0

    monthly_total = float(wind_totals.monthly_total) + float(enphase_totals.monthly_total) + float(fronius_totals.monthly_total) + (float(grid_totals.monthly_total)*1000)
    wind_monthly_percent = (float(wind_totals.monthly_total)/monthly_total) * 100
    enphase_monthly_percent = (float(enphase_totals.monthly_total)/monthly_total) * 100
    fronius_monthly_percent = (float(fronius_totals.monthly_total)/monthly_total) * 100
    grid_monthly_percent = ((float(grid_totals.monthly_total)*1000)/monthly_total) * 100

    if wind_monthly_percent < 0:
        wind_monthly_percent = 0

    yearly_total = float(wind_totals.yearly_total) + float(enphase_totals.yearly_total) + float(fronius_totals.yearly_total) + (float(grid_totals.yearly_total)*1000)
    wind_yearly_percent = (float(wind_totals.yearly_total)/yearly_total) * 100
    enphase_yearly_percent = (float(enphase_totals.yearly_total)/yearly_total) * 100
    fronius_yearly_percent = (float(fronius_totals.yearly_total)/yearly_total) * 100
    grid_yearly_percent = ((float(grid_totals.yearly_total)*1000)/yearly_total) * 100

    if wind_yearly_percent < 0:
        wind_yearly_percent = 0

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
