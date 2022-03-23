from django.urls import path
from .views import (
    indexView, 
)

app_name = 'frontend'
urlpatterns = [
    path('', indexView, name='index'),
]