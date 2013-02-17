# -*- coding: utf-8 -*-
import datetime
import os.path
import json
import hashlib
import re

from django.db import models
from django.db import IntegrityError
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse,resolve

import profiles.settings as settings
import global_settings
from profiles.utils.random_keys import generate_random_key,generate_unique_key

import mongobean.orm as orm

class TwitterUser(orm.Document):
    pass

# Create your models here.
class Commons(models.Model):

    created_at = models.DateTimeField(default = datetime.datetime.now,auto_now_add=True)
    modified_at = models.DateTimeField(default = datetime.datetime.now,auto_now=True)
    unique_key = models.CharField(max_length = 32,default = '',null = True,blank = True)

    data = models.TextField(default = '')

    def set_data(self,data):
        self.data = json.dumps(data)
        
    def get_data(self):
        if self.data == '':
            return None
        return json.loads(self.data)
    
    def save(self,*args,**kwargs):
        if self.unique_key == '':
            self.unique_key = generate_unique_key()
        super(Commons,self).save(*args,**kwargs)
    
    class Meta:
        abstract = True
        

class Profile(Commons):

    class Appearance:
        NAME = 0
        SCREEN_NAME = 3

    class NotificationPolicy:
        IMMEDIATE = 0
        ONCE_PER_DAY = 1
        ONCE_PER_WEEK = 2
        DONT_NOTIFY_ME = 3
    
    def __unicode__(self):
        return unicode(self.user.email)
        
    is_active = models.BooleanField(default = True)

    twitter_name = models.CharField(max_length = 200,default = '')
    twitter_screen_name = models.CharField(max_length=200,default = '',blank = True)
    twitter_id = models.BigIntegerField(default = None,blank = True,null = True)

    twitter_access_token = models.CharField(max_length=200,default = '',blank = True)
    twitter_access_token_secret = models.CharField(max_length=200,default = '',blank = True)

    user = models.OneToOneField(User)

    appearance_on_platform = models.IntegerField(default = Appearance.SCREEN_NAME)

    notification_policy = models.IntegerField(default = NotificationPolicy.IMMEDIATE)
    notification_weekday = models.IntegerField(default = 0)
    notification_time = models.TimeField(default = None,blank = True, null = True)
            
    def screenname(self,appearance = None):
        if not self.is_active:
            return ''
        if appearance == None:
            appearance = self.appearance_on_platform
        if appearance == Profile.Appearance.NAME and self.twitter_name:
            name = self.name
        elif appearance == Profile.Appearance.SCREEN_NAME and self.twitter_screen_name:
            name = self.twitter_screen_name
        else:
            name = "Anonymous"
        return name