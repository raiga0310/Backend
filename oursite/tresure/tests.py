from django.test import TestCase
from django.test import Client
from .models import Difficulty, Player
from django.urls import reverse
from django.contrib.auth.models import User
# Create your tests here.


class On_Goal_Test(TestCase):

    # テストするプレイヤーに与える難易度のpkのリスト
    try_difficulty_pk_list = [1, 3, 2]
    fixtures = ['difficulty.json']

    def setUp(self):
        self.client = Client()
        for i in self.try_difficulty_pk_list:  # Playerをtry_listに沿って作成
            Player.objects.create(difficulty=Difficulty.
                                  objects.get(pk=str(i)))

    def test_on_goal(self):
        for j in range(len(self.try_difficulty_pk_list)):  # playerの数だけ繰り返す。
            player_pk = j + 1
            s = self.client.session
            s['player_pk'] = player_pk  # プレイヤーのpk(1スタート)をセッションに登録する。
            s.save()
            for i in range(1, 3 + 1):  # Difficultyの長さだけ繰り返す。(iはDifficultyのpk)
                # 与えたセッションを使い,/tresure/(難易度のpk)/on-goal/をGETする。
                response = self.client.get('/tresure/' + str(i) + '/on-goal/',
                                           follow=True)
                # URLに与えた難易度のpkが,try_listのDifficulty(現在テスト中のプレイヤーに与えているDifficulty)のpkと等しい時
                if(i == self.try_difficulty_pk_list[j]):
                    # 最後のページへ飛移するはず。(302)
                    self.assertEqual(response.redirect_chain,
                                     [('/tresure/last/', 302)])
                    # 難易度の文字列化したものが表示される。
                    self.assertContains(response,
                                        Difficulty.objects.get(pk=str(i)).name)
                else:
                    # 違うならエラーメッセージが表示されるはず。
                    self.assertContains(response, "難易度が違います。他のＱＲコードを読んでください。")
