from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from .models import Player,Difficulty

# Create your views here.
def index(request):
    return HttpResponse("中身無し")

class OnGoal(TemplateView):
    template_name = "tresure/on_goal.html"

    def get(self, request, **kwargs):
        player = get_object_or_404(Player , pk = request.session.get('player_pk' , -1))
        
        if kwargs['pk'] == player.difficulty.pk:
            return HttpResponseRedirect(reverse('tresure:last'))
        return super().get(request, **kwargs)

class Last(TemplateView):
    template_name = "tresure/last.html"

    def get(self, request, **kwargs):
        player = get_object_or_404(Player , pk = request.session.get('player_pk' , -1))
        kwargs['dif'] = player.difficulty 
        return super().get(request, **kwargs)
    
