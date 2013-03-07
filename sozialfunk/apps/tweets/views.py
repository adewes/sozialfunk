# Create your views here.f
# -*- coding: utf-8 -*-

from pymongo.errors import InvalidId

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
import tweets.tasks as tasks

import functools
import tweepy
import tweets.models as models

def friends(request,category = ''):
    if category:
        friends = models.Friend.collection.find({'categories':{'$in':[category]}}).sort('twitter_data.name')
    else:
        friends = models.Friend.collection.find().sort('twitter_data.name')
    context = RequestContext(request)
    return render_to_response('tweets/friends.html', {'selected_category':category,'friends':friends,'categories':settings.ORGANIZATIONS_CATEGORIES},context)

def get_tweet(request,tweet_id = 0):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        return HttpResponse(json.dumps({'status':404}),mimetype="application/json")
    else:
        template = loader.get_template("tweets/_tweet_details.html")
        context = RequestContext(request,{'tweet':tweet})
        html = template.render(context)
        return HttpResponse(json.dumps({'status':200,'html':html}),mimetype="application/json")

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

def _toggle_organization_category(request,organization_id,category,remove = False):
    try:
        organization = models.Friend.collection.find_one({u'_id':models.orm.ObjectId(str(organization_id))})
    except InvalidId:
        organization = None
    if organization == None:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':404}))
        else:
            raise Http404
        
    if not category in settings.ORGANIZATIONS_CATEGORIES:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':500}))
        else:
            raise PermissionDenied

    if not 'categories' in organization:
        organization['categories'] = []

    if remove:
        if category in organization['categories']:
            organization['categories'].remove(category)
    else:
        if not category in organization['categories']:
            organization['categories'].append(category)

    organization.save()

    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200,'categories':organization['categories']}))
    else:
        return redirect(index)

@login_required(staff_required = True)
def remove_organization_from_category(request,organization_id = '',category = ''):
    return _toggle_organization_category(request,organization_id,category,remove = True)

@login_required(staff_required = True)
def add_organization_to_category(request,organization_id = '',category = ''):
    return _toggle_organization_category(request,organization_id,category,remove = False)

@login_required(staff_required = True)
def remove_from_category(request,tweet_id = 0,category = ''):
    return _toggle_category(request,tweet_id,category,remove = True)

@login_required(staff_required = True)
def add_to_category(request,tweet_id = 0,category = ''):
    return _toggle_category(request,tweet_id,category,remove = False)

def _verify_vote_fields_are_present(request,tweet):
    if not 'upvote_users' in tweet:
        tweet['upvote_users'] = []
    if not 'downvote_users' in tweet:
        tweet['downvote_users'] = []
    if not 'upvotes' in tweet:
        tweet['upvotes'] = 0
    if not 'downvotes' in tweet:
        tweet['downvotes'] = 0

def count_click(request,tweet_id = 0,url = ''):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        return redirect(url)
    if not 'clicks' in tweet:
        tweet['clicks'] = 0
        tweet['anonymous_clicks'] = 0
        tweet['clicks_sessions'] = []
        tweet['clicks_users'] = []
        tweet['clicked_urls'] = {}
        tweet['anonymous_clicked_urls'] = {}
    sanitized_url = url.replace(".","_")
    if request.user.is_authenticated():
        if not request.user.id in tweet['clicks_users']:
            tweet['clicks_users'].append(request.user.id)
            tweet['clicks']+=1
            if not sanitized_url in tweet['clicked_urls']:
                tweet['clicked_urls'][sanitized_url] = [url,0]
            tweet['clicked_urls'][sanitized_url][1]+=1
    else:
        if not request.session.session_key in tweet['clicks_sessions']:
            tweet['clicks_sessions'].append(request.session.session_key)
            tweet['anonymous_clicks']+=1
            if not sanitized_url in tweet['anonymous_clicked_urls']:
                tweet['anonymous_clicked_urls'][sanitized_url] = [url,0]
            tweet['anonymous_clicked_urls'][sanitized_url][1]+=1
    tweet.save()
    return redirect(url)

@login_required()
def upvote(request,tweet_id = 0):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':404}))
        else:
            raise Http404
    _verify_vote_fields_are_present(request,tweet)
    if request.user.id in tweet['downvote_users']:
        tweet['downvote_users'].remove(request.user.id)
        tweet['downvotes']-=1
    if not request.user.id in tweet['upvote_users']:
        tweet['upvote_users'].append(request.user.id)
        tweet['upvotes']+=1
    if tweet['score'] == 0:
        tweet['score'] = 1
    tweet.save()
    tasks.update_score(tweet['id'])
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
    _verify_vote_fields_are_present(request,tweet)
    if request.user.id in tweet['upvote_users']:
        tweet['upvote_users'].remove(request.user.id)
        tweet['upvotes']-=1
    tweet.save()
    tasks.update_score(tweet['id'])
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200}))
    else:
        return redirect(index)

@login_required()
def downvote(request,tweet_id = 0):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':404}))
        else:
            raise Http404
    _verify_vote_fields_are_present(request,tweet)
    if request.user.id in tweet['upvote_users']:
        tweet['upvote_users'].remove(request.user.id)
        tweet['upvotes']-=1
    if not request.user.id in tweet['downvote_users']:
        tweet['downvote_users'].append(request.user.id)
        tweet['downvotes']+=1
    tweet.save()
    tasks.update_score(tweet['id'])
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200}))
    else:
        return redirect(index)

@login_required()
def undo_downvote(request,tweet_id = 0):
    tweet = models.Tweet.collection.find_one({'id':int(tweet_id)})
    if tweet == None:
        if request.accepts('application/json'):
            return HttpResponse(json.dumps({'status':404}))
        else:
            raise Http404
    _verify_vote_fields_are_present(request,tweet)
    if request.user.id in tweet['downvote_users']:
        tweet['downvote_users'].remove(request.user.id)
        tweet['downvotes']-=1
    tweet.save()
    tasks.update_score(tweet['id'])
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200}))
    else:
        return redirect(index)

def _render_tweets(request,tweets):
    tweets_html = []
    for tweet in tweets:
        template = loader.get_template("tweets/_tweet.html")
        context = RequestContext(request,{'tweet':tweet})
        tweets_html.append(template.render(context))
    return tweets_html

def index(request,category = None):
    context = RequestContext(request)
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])
        except AttributeError:
            page = 1
    else:
        page = 1
    if category:
        if not category in settings.TWEET_CATEGORIES:
            raise PermissionDenied
        tweets = models.Tweet.collection.find({'score':{'$gte':1},'categories':{'$in':[category]},'twitter_data.retweeted_status':{'$exists':False}}).sort('score',-1)
    else:
        tweets = models.Tweet.collection.find({'score':{'$gte':1},'twitter_data.retweeted_status':{'$exists':False}}).sort('score',-1)
    filtered_tweets = tweets[settings.TWEETS_PER_PAGE*(page-1):settings.TWEETS_PER_PAGE*page]
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200,'tweets_html':_render_tweets(request,filtered_tweets)}),mimetype="application/json")
    else:
        return render_to_response('tweets/index.html', {'next_page':page+1,'selected_category':category,'tweets':filtered_tweets,'categories':settings.TWEET_CATEGORIES},context)

def raw_timeline(request,category = None):
    context = RequestContext(request)
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])
        except AttributeError:
            page = 1
    else:
        page = 1
    if category:
        if not category in settings.TWEET_CATEGORIES:
            raise PermissionDenied
    tweets = models.Tweet.collection.find({'timeline':'home','twitter_data.retweeted_status':{'$exists':False}}).sort('created_at',-1)
    filtered_tweets = tweets[settings.TWEETS_PER_PAGE*(page-1):settings.TWEETS_PER_PAGE*page]
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200,'tweets_html':_render_tweets(request,filtered_tweets)}),mimetype="application/json")
    else:
        return render_to_response('tweets/raw_timeline.html', {'next_page':page+1,'tweets':filtered_tweets},context)

@login_required()
def mentions(request,category = None):
    context = RequestContext(request)
    if 'page' in request.GET:
        try:
            page = int(request.GET['page'])
        except AttributeError:
            page = 1
    else:
        page = 1
    if category:
        if not category in settings.TWEET_CATEGORIES:
            raise PermissionDenied
    tweets = models.Tweet.collection.find({'timeline':'mentions','twitter_data.retweeted_status':{'$exists':False}}).sort('created_at',-1)
    filtered_tweets = tweets[settings.TWEETS_PER_PAGE*(page-1):settings.TWEETS_PER_PAGE*page]
    if request.accepts('application/json'):
        return HttpResponse(json.dumps({'status':200,'tweets_html':_render_tweets(request,filtered_tweets)}),mimetype="application/json")
    else:
        return render_to_response('tweets/mentions.html', {'next_page':page+1,'tweets':filtered_tweets},context)


def dismiss_info_box(request):
    request.session['info_box_dismissed'] = True
    return redirect(index)