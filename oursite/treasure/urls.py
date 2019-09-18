from django.urls import path, include
from .views import Opening, DifSel, OnGoal, GoGoal, Last, Hints, ProgressError

app_name = 'treasure'
urlpatterns = [
    path('go-goal/', GoGoal.as_view(), name='go-goal'),
    path('opening/', Opening.as_view(), name='opening'),
    path('dif-sel/', DifSel.as_view(), name='dif-sel'),
    path('<int:pk>/on-goal/', OnGoal.as_view(), name='on-goal'),
    path('last/', Last.as_view(), name='last'),
    path('<int:hint_index>/hints/', Hints.as_view(), name='hints'),
    path('progress-error/', ProgressError.as_view(), name='progress-error'),
]
