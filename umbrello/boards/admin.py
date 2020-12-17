from django.contrib import admin
from .models import Board, List, Card

# Register your models here.

class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order')

class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'description')

admin.site.register(Board, BoardAdmin)
admin.site.register(List,ListAdmin)
admin.site.register(Card,CardAdmin)