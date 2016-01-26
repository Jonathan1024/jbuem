from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def index(request):
    message = 'Hello Harrison!'
    amount = 100
    context = {
        'message':message,
        'amount':amount,
    }
    return render(request, 'MainSite/index.html', context)
