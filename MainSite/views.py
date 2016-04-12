from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
import csv
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from MainSite .models import Solar, Meter, Pyranometer, Wind
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

    context = {
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


def historical(request):

    context = {
    }

    return render(request, 'MainSite/historical.html', context)


def about(request):

    context = {
    }

    return render(request, 'MainSite/about.html', context)
