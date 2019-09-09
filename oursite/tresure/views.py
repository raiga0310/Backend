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
    #簡略化
    hint = {1:player.quiz1.hint , 2:player.quiz2.hint , 3:player.quiz3.hint , 4:player.quiz4.hint}
    keyword= {1:player.quiz1.keyword , 2:player.quiz2.keyword , 3:player.quiz3.keyword , 4:player.quiz4.keyword}

    def get(self, request, *args, **kwargs):
        player = get_object_or_404(Player,pk=request.session.get('player_pk')) #セッションからplayerの情報を取得
        kwargs['hint'] = hint[kwargs['hint_index']] #現在のページに対応したヒントを送信
        return super().get(request , *args , **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('number', None): #キーワードを受け取ったなら
            if keyword[kwargs['hint_index']] == self.request.POST.get('number', None): #受け取ったキーワードが現在のページの答えと等しいなら
                kwargs['result'] = '正解' #正解と送信
                if kwargs['hint_index'] == 4: #現在が４ページ目なら
                    HttpResponceRedirect(django.shortcuts.reverse('go-goal')) #ゴール誘導ページへ
                else:
                    HttpResponceRedirect(django.shortcuts.reverse('treasure/hints' , args = (kwargs['hint_index']+1))) #次のページへ
            else:
                kwargs['result'] = '不正解' #不正解と送信
                HttpResponceRedirect(django.shortcuts.reverse('treasure/hints' , args = (kwargs['hint_index']))) #同じページへ
        return super().post(request , *args , **kwargs)

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
