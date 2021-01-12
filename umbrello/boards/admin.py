from django.contrib import admin
from .models import Board, List, Card, Log

# Register your models here.

class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order')

class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'description')

class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'board_id', 'username', 'description', 'term', 'order')

admin.site.register(Board, BoardAdmin)
admin.site.register(List,ListAdmin)
admin.site.register(Card,CardAdmin)
admin.site.register(Log,LogAdmin)