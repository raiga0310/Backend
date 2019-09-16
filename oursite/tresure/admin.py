from django.contrib import admin
from .models import Difficulty, Player, Quiz, Goal, Quizzes
# Register your models here.
admin.site.register(Difficulty)
admin.site.register(Player)
admin.site.register(Quiz)
admin.site.register(Goal)
admin.site.register(Quizzes)
