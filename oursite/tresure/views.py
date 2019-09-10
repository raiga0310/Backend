from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Player, Difficulty, Goal, Quiz
from random import shuffle


class GoGoal(TemplateView):
    template_name = "tresure/go_goal.html"

    def get(self, request, *args, **kwargs):
        player = get_object_or_404(Player, pk=request.session.get('player_pk'))
        diff_pk = player.difficulty.pk
        kwargs['diff_pk'] = player.difficulty.pk
        if(diff_pk == 1):
            kwargs['goal'] = player.difficulty.goal.name
        else:
            #correspond = []
            kwargs['quizzes'] = player.quizzes.all()
            kwargs['change'] = ('10' if (diff_pk == 2) else '16') + '進数'
            #for i in range(0b1_0000_0000):
            #    correspond.append({'binary': format(i, '08b'),
            #                       'to_base':
            #                       (format(i, '08d') if diff_pk == 2
            #                        else format(i, '08x'))})
            #kwargs['correspond'] = correspond
        return super().get(request, *args, **kwargs)


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
