from django.shortcuts import render, get_object_or_404, reverse
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

    def get(self, request, *args, **kwargs):
        # セッションからplayerの情報を取得
        player = get_object_or_404(Player,
                                   pk=request.session.get('player_pk', -1))
        # 簡略化
        hint = {1: player.quiz1.hint, 2: player.quiz2.hint,
                3: player.quiz3.hint, 4: player.quiz4.hint}
        # 現在のページに対応したヒントを送信
        kwargs['hint'] = hint[kwargs['hint_index']]
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # キーワードを受け取ったなら
        if self.request.POST.get('number', None):
            # 簡略化
            keyword = {1: player.quiz1.keyword, 2: player.quiz2.keyword,
                       3: player.quiz3.keyword, 4: player.quiz4.keyword}
            # 受け取ったキーワードが現在のページの答えと等しいなら
            if keyword[kwargs['hint_index']] == self.request.POST.get('number',
                                                                      None):
                # 正解と送信
                kwargs['result'] = '正解'
                # 現在が４ページ目なら
                if kwargs['hint_index'] == 4:
                    # ゴール誘導ページへ
                    return HttpResponceRedirect(reverse('tresure:go-goal'))
                else:
                    # 次のページへ
                    return HttpResponceRedirect(reverse(
                            'tresure:hints', args=(kwargs['hint_index']+1)))
            else:
                # 不正解と送信
                kwargs['result'] = '不正解'
        return super().post(request, *args, **kwargs)


class Opening(TemplateView):
    template_name = 'tresure/opening.html'

    def post(self, request, **kwargs):
        if(request.POST.get('was_pushed', -1) != -1):
            if(request.session.get('player_pk', -1) != -1):
                return HttpResponseRedirect(reverse('tresure:hints', hint_index=1))
            else:
                return HttpResponseRedirect(reverse('tresure:dif-sel'))
        return super().post(self, request, **kwargs)


class DifSel(TemplateView):
    pass


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
