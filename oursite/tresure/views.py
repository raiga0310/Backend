from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Player, Difficulty, Goal, Quiz
from random import shuffle
from .utility import ConversionTableResolver


class GoGoal(TemplateView):
    template_name = "tresure/go_goal.html"

    def get(self, request, *args, **kwargs):
        player = get_object_or_404(Player, pk=request.session.get('player_pk'))
        diff_pk = player.difficulty.pk
        kwargs['diff_pk'] = diff_pk
        if(diff_pk == 1):
            kwargs['goal'] = player.difficulty.goal.name
        else:
            kwargs['quizzes'] = player.quizzes.all()
            kwargs['change'] = ('10' if (diff_pk == 2) else '16') + '進数'
            table = ConversionTableResolver.createTable(diff_pk)
            kwargs['corresponds'] = table.data
        return super().get(request, *args, **kwargs)

class Hints(TemplateView):
    template_name = 'tresure/hints.html'
    keyword = {1:player.quiz1.keyword , 2:player.quiz2.keyword ,
              3:player.quiz3.keyword , 4:player.quiz4.keyword}
    page = 1

    def get(self, request, **kwargs):
        player = get_object_or_404(Player,
                                   pk=request.session.get('player_pk', -1))
        return super().get(request, **kwargs)

    def post(self, request, **kwargs):
        if self.request.POST.get('number', None):
            if keyword[page] == self.request.POST.get('number', None)):
                #正解と送信
                if page == 4:
                    #ゴール誘導ページへ
                else:
                    page++
                    #pageページを表示
            else:
                #不正解と送信
                #pageページを表示


class OnGoal(TemplateView):
    template_name = 'tresure/on_goal.html'

    def get(self, request, **kwargs):
        player = get_object_or_404(Player,
                                   pk=request.session.get('player_pk', -1))
        if kwargs['pk'] == player.difficulty.pk:
            return HttpResponseRedirect(reverse('tresure:last'))
        return super().get(request, **kwargs)


class Last(TemplateView):
    template_name = 'tresure/last.html'

    def get(self, request, **kwargs):
        player = get_object_or_404(Player,
                                   pk=request.session.get('player_pk', -1))
        kwargs['dif'] = player.difficulty
        return super().get(request, **kwargs)
