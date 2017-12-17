from django.db import models
import datetime


class LvlTri(models.Model):
    lvl = models.IntegerField(default=0, null=True, blank=True)
    sub_lvl = models.IntegerField(default=0, null=True, blank=True)
    question = models.CharField(default='', max_length=50, null=True, blank=True)
    answer = models.CharField(default='', max_length=50, null=True, blank=True)
    result = models.IntegerField(default=0, null=True, blank=True)
    hi_score = models.IntegerField(default=0, null=True, blank=True)
    time = models.CharField(default=datetime.datetime.now(), max_length=250, null=True, blank=True)
    max_sub_lvl = models.IntegerField(default=0, null=True, blank=True)
    user = models.CharField(max_length=250)
