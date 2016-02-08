from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.db import connection
# Create your views here.


def index(request):
    sql = "SELECT * FROM data_temp ORDER BY datetime DESC LIMIT 1;"
    sql2 = "SELECT * FROM sel_data ORDER BY datetime DESC LIMIT 1;"
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

    with connection.cursor() as cur:
        cur.execute(sql2)
        var = cur.fetchone()
    selPower = var[1]


    context = {
        'enphasePower': enphasePower,
        'froniusPower': froniusPower,
        'selPower': selPower,
        'datetime': datetime,
        'kandz': kandz,
        'eppely': eppely,
        'windPower': windPower,
    }
    return render(request, 'MainSite/index.html', context)
