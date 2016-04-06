from django.test import TestCase
from django.contrib.auth.models import User

class UserModelTests(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.user = User.objects.create_user(username='zx', email='zx@gmail.com', password='zx')

    def test_user_email_unique(self):
        acct = User.objects.get(email="zx@gmail.com")
        self.assertEqual(acct.username, self.user.username)

