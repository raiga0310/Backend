from django.test import TestCase
from django.test import Client
from .models import Difficulty , Player
from django.urls import reverse
from django.contrib.auth.models import User
# Create your tests here.

class On_Goal_Test(TestCase):
    def setUp(self):
        self.client = Client()

        Difficulty.objects.create(name = '簡単')
        Difficulty.objects.create(name = '普通')
        Difficulty.objects.create(name = '難しい')
        Player.objects.create(difficulty = Difficulty.objects.get(pk = '1'))
        s = self.client.session
        s['player_pk'] = 1 #プレイヤーのpk
        s.save()
        self.assertEqual(1, s['player_pk'])

    def test_on_goal(self):
        response = self.client.get('/tresure/3/on-goal/')
        print(response.content)
        self.assertEqual(response.status_code, 200)
