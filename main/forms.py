from django import forms
from . import models

class SteamUrlForm(forms.Form):
    profile_url = forms.URLField(
        label='',
        widget=forms.URLInput(attrs={
            'placeholder':'Введите ссылку на ваш Steam профиль',
            'class': 'bg-transparent w-full text-white text-lg placeholder-slate-500 focus:outline-none focus:ring-0'
        }),
    )