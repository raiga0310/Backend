from django.db import models
from . import Difficulty, Quizzes


class Player(models.Model):
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    quizzes = models.ForeignKey(Quizzes, on_delete=models.CASCADE, null=True)
