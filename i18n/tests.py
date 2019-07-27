from django.test import TestCase
from django.test.client import Client
from i18n.models import Profile
from django.contrib.auth.models import User

# Create your tests here.

class PageTest(TestCase):
    #fixtures = ['test.json']
    def setUp(self):
        username = 'admin'
        password = 'admin'
        # 新規ユーザ作成
        new_user = User(username=username)
        # パスワード保存
        new_user.set_password(password)
        new_user.save()

        # 新規プロフィール作成
        new_profile = Profile(user=new_user)
        new_profile.save()
        self.client = Client()

        # 一度ログインしておく
        self.login()

    def test_login_page(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_top_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_language_page(self):
        response = self.client.get('/language/')
        self.assertEqual(response.status_code, 200)

    def test_change_language_to_ja(self):
        response = self.client.post('/language/', {'language': 'ja'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/language/')
        html = response.content.decode('utf8')
        self.assertIn('<title>言語設定ページ</title>', html)

    def test_change_language_to_en(self):
        response = self.client.post('/language/', {'language': 'en'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/language/')
        html = response.content.decode('utf8')
        self.assertIn('<title>Language setting page</title>', html)  

    def login(self):
        response = self.client.get('/login/')
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 302)
