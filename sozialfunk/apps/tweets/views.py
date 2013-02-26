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
import json

from profiles.views import login_required

import tweets.forms as forms
import tweets.settings as settings

import functools

import tweepy

import tweets.models as models

def get_tweet(request,tweet_id = 0):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        return HttpResponse(json.dumps({'status':404}),mimetype="application/json")
    else:
        template = loader.get_template("tweets/_tweet_details.html")
        context = RequestContext(request,{'tweet':tweet})
        html = template.render(context)
        return HttpResponse(json.dumps({'status':200,'html':html}),mimetype="application/json")

@login_required()
def _toggle_category(request,tweet_id,category,remove = False):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':404}))
        else:
            raise Http404
        
    if not category in settings.TWEET_CATEGORIES:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':500}))
        else:
            raise PermissionDenied

    if not 'categories' in tweet:
        tweet['categories'] = []

    if remove:
        if category in tweet['categories']:
            tweet['categories'].remove(category)
    else:
        if not category in tweet['categories']:
            tweet['categories'].append(category)

    tweet.save()

    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200,'categories':tweet['categories']}))
    else:
        return redirect(index)

@login_required()
def remove_from_category(request,tweet_id = 0,category = ''):
    return _toggle_category(request,tweet_id,category,remove = True)

@login_required()
def add_to_category(request,tweet_id = 0,category = ''):
    return _toggle_category(request,tweet_id,category,remove = False)

@login_required()
def upvote(request,tweet_id = 0):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':404}))
        else:
            raise Http404
    if not 'upvote_users' in tweet:
        tweet['upvote_users'] = []
    if not 'upvotes' in tweet:
        tweet['upvotes'] = 0
    if not request.user.profile.twitter_screen_name in tweet['upvote_users']:
        tweet['upvote_users'].append(request.user.profile.twitter_screen_name)
        tweet['upvotes']+=1
    tweet.save()
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200}))
    else:
        return redirect(index)

@login_required()
def undo_upvote(request,tweet_id = 0):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':404}))
        else:
            raise Http404
    if not 'upvote_users' in tweet:
        tweet['upvote_users'] = []
    if not 'upvotes' in tweet:
        tweet['upvotes'] = 0
    if request.user.profile.twitter_screen_name in tweet['upvote_users']:
        tweet['upvote_users'].remove(request.user.profile.twitter_screen_name)
        tweet['upvotes']-=1
    tweet.save()
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200}))
    else:
        return redirect(index)

def index(request,category = None):
    context = RequestContext(request)
    if category:
        if not category in settings.TWEET_CATEGORIES:
            raise PermissionDenied
        tweets = models.Tweet.collection.find({'categories':{'$in':[category]}}).sort('created_at',-1)[:1000]
    else:
        tweets = models.Tweet.collection.find().sort('created_at',-1)[:1000]
    tweet_users = []
    filtered_tweets = []
    for tweet in tweets:
        if tweet['twitter_data']['user']['screen_name'] in tweet_users:
            continue
        tweet_users.append(tweet['twitter_data']['user']['screen_name'])
        filtered_tweets.append(tweet)
        if len(filtered_tweets) >= 100:
            break
    return render_to_response('tweets/index.html', {'selected_category':category,'tweets':filtered_tweets,'categories':settings.TWEET_CATEGORIES},context)
