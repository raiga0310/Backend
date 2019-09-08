from django.urls import path, include

from .views import GoGoal, OnGoal, Last

app_name = 'tresure'
urlpatterns = [
    # pkはDifficultyの物
    path('go-goal/', GoGoal.as_view(), name='go-goal'),
    path('<int:pk>/on-goal/', OnGoal.as_view(), name='on-goal'),
    path('last/', Last.as_view(), name='last'),
]
