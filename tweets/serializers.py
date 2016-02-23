from rest_framework import serializers
from django.contrib.auth.models import User
from tweets.models import *



# user serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')



# twitter mention serializers
class TwitterMentionSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = TwitterMention
        fields = ('id', 'name', 'user')
