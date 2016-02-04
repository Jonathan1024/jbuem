from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def index(request):
    enphasePower = 10

    contex:{
        'enphasePower': enphasePower,
    }
    return render(request, 'MainSite/index.html', context)
