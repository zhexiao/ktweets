from django.test import TestCase
from django.contrib.auth.models import User

class UserModelTests(TestCase):
    def test_user_email_unique(self):
        acct = User.objects.get(email="zhexiao27@gmail.com")
        self.assertEqual(acct.id, 1)

