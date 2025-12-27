from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    context = {
        'content': 'Hello World from context'
    }
    return render(request, 'index.html', context)