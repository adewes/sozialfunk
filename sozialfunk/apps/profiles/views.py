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

class logout_first(object):
    
    def __init__(self):
        pass
    
    def __call__(self,function):
        @functools.wraps(function)    
        def logout_first_wrapper(request,*args,**kwargs):
            dlogout(request)
            return function(request,*args,**kwargs)
        return logout_first_wrapper

class login_required(object):
    
    def __init__(self,staff_required =False):
        self.staff_required = staff_required
    
    def __call__(self,function):
        @functools.wraps(function)
        def check_for_user(request,*args,**kwargs):
            if request.user.is_authenticated() and request.user.profile.is_active and (request.user.is_staff or not self.staff_required):
                return function(request,*args,**kwargs)
            else:
                request.flash['notice'] = _(u"Please log in first.")
                return redirect(login,next_url = request.get_full_path())
        return check_for_user

@login_required()
@csrf_protect
def profile_settings(request):
    context = RequestContext(request)
    return render_to_response('profiles/profile_settings.html', {},context)

@csrf_protect
def logout(request):
    if request.user.is_authenticated:
        dlogout(request)
        request.flash['notice'] = _(u"You have been signed out.")
    context = RequestContext(request)
    return render_to_response('profiles/logout.html', {},context)

def _directly_login_user(request,user):
    user.backend = "django.contrib.auth.backends.ModelBackend"
    dlogin(request,user)

def twitter_callback(request):
    try:
        auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY,global_settings.TWITTER.CONSUMER_KEY_SECRET)
        token = request.session['request_token']
        auth.set_request_token(token[0], token[1])
        auth.get_access_token(request.GET['oauth_verifier'])
        del request.session['request_token']
    except (tweepy.TweepError,KeyError):
        raise PermissionDenied

    request.session['access_token'] = (auth.access_token.key,auth.access_token.secret)
    
    api = tweepy.API(auth)
    
    twitter_user = api.me()
    
    try:
        profile = models.Profile.objects.get(twitter_id = twitter_user.id)
        profile_user = profile.user
    except models.Profile.DoesNotExist:
        print "Creating new profile for user %s" % twitter_user.screen_name
        profile = models.Profile()
        profile.twitter_screen_name = twitter_user.screen_name
        profile.twitter_name = twitter_user.name
        profile.twitter_id = twitter_user.id
        profile_user = models.User()
        candidate_username = None
        while (not candidate_username) or models.User.objects.filter(username = candidate_username).count():
            candidate_username = random_keys.generate_random_key()
        profile_user.username = candidate_username
        profile_user.save()
        profile.user = profile_user
        profile.save()
    
    _directly_login_user(request,profile_user)
    return redirect(profile_settings)
    
def login(request,email = None,next_url = ''):
    context = RequestContext(request)
    auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY,global_settings.TWITTER.CONSUMER_KEY_SECRET)
    try:
        redirect_url = auth.get_authorization_url()
        print redirect_url
    except tweepy.TweepError:
        raise PermissionDenied
    request.session['request_token'] = (auth.request_token.key, auth.request_token.secret)
    return redirect(redirect_url+"&x_auth_access_type=read")
