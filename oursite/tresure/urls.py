from django.urls import path , include

from .views import index , OnGoal , Last

app_name = 'tresure'
urlpatterns = [
    path('' , index , name ='index'),#廃棄予定
    path('<int:pk>/on-goal/' , OnGoal.as_view() , name ='on-goal'),#pkはDifficultyの物
    path('last/' , Last.as_view() , name ='last'),
]
