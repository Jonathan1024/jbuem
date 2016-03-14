from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
from MainSite .models import Solar, Meter, Pyranometer, Wind
# Create your views here.


def index(request):
    sql = "SELECT * FROM data_temp ORDER BY datetime DESC LIMIT 1;"
    sql2 = "SELECT * FROM sel_data ORDER BY datetime DESC LIMIT 1;"
    sql3 = "SELECT * FROM wind_data ORDER BY time_stamp DESC LIMIT 1"

    var = []
    enphasePower = 0
    froniusPower = 0
    windPower = 0.0
    selPower = 0
    datetime = ''
    kandz = 0
    eppely = 0

    with connection.cursor() as cur:
        cur.execute(sql)
        var = cur.fetchone()

    datetime = var[0]
    enphasePower = var[1]
    froniusPower = var[2]
    kandz = var[3]
    eppely = var[4]

    totalPower = float(enphasePower) + float(froniusPower) + float(windPower)

    with connection.cursor() as cur:
        cur.execute(sql2)
        var = cur.fetchone()

    selPower = var[1]

    with connection.cursor() as cur:
        cur.execute(sql3)
        var = cur.fetchone()

    windPower = var[4]

    context = {
        'enphasePower': enphasePower,
        'froniusPower': froniusPower,
        'selPower': selPower,
        'datetime': datetime,
        'kandz': kandz,
        'eppely': eppely,
        'windPower': windPower,
        'totalPower': totalPower,
    }

    return render(request, 'MainSite/index.html', context)


def test(request):
    var = Wind.objects.all() # Show all in Wind

    var = Meter.objects.order_by('-time_stamp')[0]

    context = {
        'var':var.btc_power
    }
    return render(request, 'MainSite/test.html', context)
