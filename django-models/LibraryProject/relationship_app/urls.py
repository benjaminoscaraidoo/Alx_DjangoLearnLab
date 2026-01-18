from django.urls import path
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [

    path('', views.list_books, name='list_books'),
    path('', views.LibraryDetailView, name='library_detail'),
] 