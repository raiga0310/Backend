from django.urls import path , include

from . import views

app_name = 'tresure'
urlpatterns = [
    path('' , views.index , name ='index')
]
