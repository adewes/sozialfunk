# Create your views here.f
# -*- coding: utf-8 -*-

from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.shortcuts import *
from django.core.urlresolvers import reverse,resolve
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as dlogin
from django.contrib.auth import logout as dlogout
from django.db import IntegrityError
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.models import ContentType

import profiles.settings as settings
import profiles.models as models
import profiles.forms as forms
import profiles.utils.random_keys as random_keys
import global_settings

import functools

import tweepy

import tweets.models as models

def index(request):
    context = RequestContext(request)
    tweets = models.Tweet.collection.find({u'user_screen_name':u'sozialfunktest'}).sort('-created_at')[:100]
    return render_to_response('tweets/index.html', {'tweets':tweets},context)
