import uuid

from django.db import models

class Users(models.Model):
    steamid = models.CharField(max_length=20 ,primary_key=True)
    personaname = models.CharField(max_length=255)
    avatar_url = models.CharField(max_length=255)

class Game(models.Model):
    appid = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    icon_url = models.URLField(blank=True)
    genre = models.CharField(max_length=100, blank=True)