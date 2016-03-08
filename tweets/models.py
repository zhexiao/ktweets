from django.db import models
from django.contrib.auth.models import User

# user twitter tracks table
class TwitterTracks(models.Model):
    text = models.CharField(max_length=255, default='')
    user = models.ManyToManyField(User, db_table='twitter_track_xref_user', related_name='tw_tracks')

    class Meta:
        db_table = 'twitter_tracks'
        ordering = ('text', )

    def __str__(self):
        return self.name
