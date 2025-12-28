from django.shortcuts import render
from . import forms
# Create your views here.
from django.http import HttpResponse


def index(request):
    if request.method == 'POST':
        print('Данные формы', request.POST)
        form = forms.SteamUrlForm(request.POST)
    else:
        form = forms.SteamUrlForm()
    context = {
        'content': 'Hello World from context',
        'form': form,
    }
    return render(request, 'index.html', context)
