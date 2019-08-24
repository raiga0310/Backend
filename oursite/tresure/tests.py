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
        for player in Player.objects.all():  # playerの数だけ繰り返す。
            s = self.client.session
            s['player_pk'] = player.pk  # プレイヤーのpk(1スタート)をセッションに登録する。
            s.save()
            for diff in Difficulty.objects.all():  # Difficultyの長さだけ繰り返す。
                # 与えたセッションを使い,/tresure/(難易度のpk)/on-goal/をGETする。
                response = self.client.get('/tresure/' + str(diff.pk) +
                                           '/on-goal/', follow=True)
                # URLに与えた難易度のpkが,try_listのDifficulty(現在テスト中のプレイヤーに与えているDifficulty)のpkと等しい時
                if(diff.pk == self.try_difficulty_pk_list[player.pk - 1]):
                    # 最後のページへ飛移するはず。(302)
                    self.assertEqual(response.redirect_chain,
                                     [('/tresure/last/', 302)])
                    # 難易度の文字列化したものが表示されるはず。
                    self.assertContains(response,
                                        Difficulty.objects.
                                        get(pk=str(diff.pk)).name)
                else:
                    # 違うならエラーメッセージが表示されるはず。
                    self.assertContains(response, '難易度が違います。他のＱＲコードを読んでください。')
