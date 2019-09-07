from django.urls import path, include

from .views import index, OnGoal, Last

app_name = 'tresure'
urlpatterns = [
    # pkはDifficultyの物
    path('<int:pk>/on-goal/', OnGoal.as_view(), name='on-goal'),
    path('last/', Last.as_view(), name='last'),
]
