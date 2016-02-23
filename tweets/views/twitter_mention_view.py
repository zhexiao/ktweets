from django.http import Http404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from tweets.models import TwitterMention
from tweets.serializers import *


# get all lists
class TwitterMentionLists(APIView):
    def get(self, request, format=None):
        lists = TwitterMention.objects.order_by('-id').all()
        paginator = PageNumberPagination()
        paginator_result = paginator.paginate_queryset(lists, request)
        serializer = TwitterMentionSerializer(paginator_result, many=True)
        return paginator.get_paginated_response(serializer.data)
