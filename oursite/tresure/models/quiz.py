from django.db import models


class Quiz(models.Model):
    hint = models.CharField()
    keyword = models.CharField()
