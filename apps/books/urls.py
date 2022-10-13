from django.urls import path
from .views import ListBooks

urlpatterns = [
    path('',ListBooks.as_view(),name='listBooks'),
    path('<int:pk>/',ListBooks.as_view(),name='listBooksRetrieve')
]