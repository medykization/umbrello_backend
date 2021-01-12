from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group


class Board(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE)
    members_id = models.ForeignKey(
        Group, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class List(models.Model):
    id = models.AutoField(primary_key=True)
    board_id = models.ForeignKey(Board,  on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    order = models.DecimalField(
        max_digits=30, decimal_places=15, blank=True, null=True)
    archived = models.BooleanField(default = False)
    def __str__(self):
        return self.name


class Card(models.Model):
    id = models.AutoField(primary_key=True)
    list_id = models.ForeignKey(List,  on_delete=models.CASCADE)
    members_id = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    name = models.CharField(max_length=30)
    archived = models.BooleanField(default=False)
    order = models.DecimalField(
        max_digits=30, decimal_places=15, blank=True, null=True)
    description = models.CharField(max_length=30, blank=True)
    term = models.DateField(null=True, blank=True, default=None) 

    def __str__(self):
        return self.name
    
class Log(models.Model):
    id = models.AutoField(primary_key=True)
    board_id = models.ForeignKey(Board,  on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank = True)
    term = models.DateField(auto_now_add=True) 
    order = models.DecimalField(max_digits=30, decimal_places=15)