from django.db import models
from . import Quiz


class Quizzes(models.Model):
    quiz1 = models.ForeignKey(Quiz, related_name="quiz1", on_delete = models.CASCADE)
    quiz2 = models.ForeignKey(Quiz, related_name="quiz2", on_delete = models.CASCADE)
    quiz3 = models.ForeignKey(Quiz, related_name="quiz3", on_delete = models.CASCADE)
    quiz4 = models.ForeignKey(Quiz, related_name="quiz4", on_delete = models.CASCADE)

    def get_quiz(self, index):
        return [self.quiz1, self.quiz2, self.quiz3, self.quiz4][index]

    def get_all_quizzes(self):
        return [self.quiz1, self.quiz2, self.quiz3, self.quiz4]

    def set_quiz(self, index, quiz):
        if(index == 0):
            self.quiz1 = quiz
        elif(index == 1):
            self.quiz2 = quiz
        elif(index == 2):
            self.quiz3 = quiz
        elif(index == 3):
            self.quiz4 = quiz
        else:
            raise Exception('インデックスは0～3で指定してください')