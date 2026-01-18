from django.urls import path
from . import views


urlpatterns = [

    path('', views.list_books, name='list_books'),
    path('', views.library_detail, name='library_detail'),
] 