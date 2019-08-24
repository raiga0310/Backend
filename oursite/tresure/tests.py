from django.test import TestCase
from django.test import Client
from .models import Difficulty , Player
from django.urls import reverse
from django.contrib.auth.models import User
# Create your tests here.

class On_Goal_Test(TestCase):
    try_list = [1,3,2] #テストするプレイヤーに与える難易度のリスト[(簡単),(難しい),(普通)]
    def setUp(self):
        self.client = Client()

        Difficulty.objects.create(name = '簡単')
        Difficulty.objects.create(name = '普通')
        Difficulty.objects.create(name = '難しい')
        for i in self.try_list: #Playerをtry_listに沿って作成
            Player.objects.create(difficulty = Difficulty.objects.get(pk = str(i)))

    def test_on_goal(self):
        for j in range(len(self.try_list)): #playerの数だけ繰り返す。
            s = self.client.session
            s['player_pk'] = j + 1 #プレイヤーのpk(1スタート)をセッションに登録する。
            s.save()
            for i in range(1 , 3 + 1):
                response = self.client.get('/tresure/'+ str(i) +'/on-goal/') #与えたセッションを使い,/tresure/(難易度のpk)/on-goal/をGETする。
                if(i == self.try_list[j]): #URLに与えた難易度のpkが,try_listのDifficulty(現在テスト中のプレイヤーに与えているDifficulty)のpkと等しい時
                    self.assertEqual(response.status_code, 302)# 最後のページへ飛移するはず。(302) 
                else:
                    self.assertEqual(response.status_code, 200) #違うならエラーメッセージ(ページ自体は正常に表示されるのでレスポンスは200のはず)