from django.urls import path
from boards.views import BoardView, BoardAdd, BoardNameUpdate, BoardAddUser, ListView, ListAdd, CardArchived, CardAdd, CardView, ListNameUpdate, ListChangeOrder, ListArchive, CardArchive, ListDelete, CardDelete, CardValuesUpdate, BoardLogs


app_name = "boards"

urlpatterns = [
    path('', BoardView.as_view()),
    path('add', BoardAdd.as_view()),
    path('add/user', BoardAddUser.as_view()),
    path('update', BoardNameUpdate.as_view()),
    path('lists', ListView.as_view()),
    path('add/list', ListAdd.as_view()),
    path('update/list', ListNameUpdate.as_view()),
    path('change/list', ListChangeOrder.as_view()),
    path('archive/list', ListArchive.as_view()),
    path('delete/list', ListDelete.as_view()),
    path('cards', CardView.as_view()),
    path('add/card', CardAdd.as_view()),
    path('update/card', CardValuesUpdate.as_view()),
    path('archive/card', CardArchive.as_view()),
    path('archived/cards', CardArchived.as_view()),
    path('delete/card', CardDelete.as_view()),
    path('logs', BoardLogs.as_view()),
]