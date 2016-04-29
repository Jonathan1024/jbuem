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

    var = Meter.objects.order_by('-time_stamp')[0]

    context = {
        'var':var.btc_power
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
    # wind_totals = WindTotals.objects.order_by('-time_stamp')[0]



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
    }

    return render(request, 'MainSite/dashboard1.html', context)
