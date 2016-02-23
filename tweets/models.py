from django.db import models
from django.contrib.auth.models import User

# user twitter mention table
class TwitterMention(models.Model):
    name = models.CharField(max_length=255, default='')
    user = models.ManyToManyField(User, db_table='twitter_mention_xref_user', related_name='tw_mention')

    class Meta:
        db_table = 'twitter_mention'
        ordering = ('name', )

    def __str__(self):
        return self.name
