from django.urls import path, include

from .views import GoGoal, OnGoal, Last

app_name = 'tresure'
urlpatterns = [
    path('go-goal/', GoGoal.as_view(), name='go-goal'),
    # pkはDifficultyの物
    path('<int:pk>/on-goal/', OnGoal.as_view(), name='on-goal'),
    path('last/', Last.as_view(), name='last'),
    path('hints/<int:hint_index>/', Hints.as_view(), name='hints'),
]
