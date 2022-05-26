from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import  models
# Create your views here.
def index(request):
    return render(request, 'index.html')