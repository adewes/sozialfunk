from celery.task import task
import settings as settings
import tweets.models as models

import datetime
import time
import math
import re
from traceback import format_exc
import global_settings

from celery.task import periodic_task

import tweepy

import json

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'raw', raw)
    return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse

tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse

@periodic_task(run_every=datetime.timedelta(seconds=600),default_retry_delay=10)
def update_followers():
    preferences = models.Preferences.collection.find_one({'application':'followers'})

    if not preferences:
        preferences = models.Preferences(application = 'followers')

    auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY, global_settings.TWITTER.CONSUMER_KEY_SECRET)
    auth.set_access_token(global_settings.TWITTER.ACCESS_TOKEN, global_settings.TWITTER.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    followers_ids_cursor = tweepy.Cursor(api.followers_ids)

    followers_ids = []

    for follower_id in followers_ids_cursor.items():
        followers_ids.append(follower_id)
        if len(followers_ids) > 5000:
            break

    followers_ids = followers_ids[:200]

    print len(followers_ids)

    obsolete_followers_ids = map(lambda x:x['id'],models.Follower.collection.find({'id':{'$nin':followers_ids}}))
    existing_followers_ids = map(lambda x:x['id'],models.Follower.collection.find({'id':{'$in':followers_ids}}))
    new_followers_ids = [id for id in followers_ids if id not in existing_followers_ids]

    print "%d obsolete followers, %d new followers and %d existing followers" % (len(obsolete_followers_ids),len(new_followers_ids),len(existing_followers_ids))

    models.Follower.collection.remove({'id':{'$in':obsolete_followers_ids}})

    i = 0
    while i < len(new_followers_ids):
        twitter_users = api.lookup_users(new_followers_ids[i:i+100])
        for twitter_user in twitter_users:
            follower = models.Follower.collection.find_one({'id':twitter_user.id})
            if not follower:
                follower = models.Follower(id = twitter_user.id,screen_name = twitter_user.screen_name)
            follower['twitter_data'] = twitter_user.raw
            follower.save()
        i+=100

    print "We have %d followers so far" % models.Follower.collection.find().count()
 

@periodic_task(run_every=datetime.timedelta(seconds=600),default_retry_delay= 10)
def update_friends():
    preferences = models.Preferences.collection.find_one({'application':'friends'})

    if not preferences:
        preferences = models.Preferences(application = 'friends')

    auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY, global_settings.TWITTER.CONSUMER_KEY_SECRET)
    auth.set_access_token(global_settings.TWITTER.ACCESS_TOKEN, global_settings.TWITTER.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    friends_ids_cursor = tweepy.Cursor(api.friends_ids)

    friends_ids = []

    for friend_id in friends_ids_cursor.items():
        friends_ids.append(friend_id)
        if len(friends_ids) > 5000:
            break

    friends_ids = friends_ids[:200]

    print len(friends_ids)

    obsolete_friends_ids = map(lambda x:x['id'],models.Friend.collection.find({'id':{'$nin':friends_ids}}))
    existing_friends_ids = map(lambda x:x['id'],models.Friend.collection.find({'id':{'$in':friends_ids}}))
    new_friends_ids = [id for id in friends_ids if id not in existing_friends_ids]

    print "%d obsolete friends, %d new friends and %d existing friends" % (len(obsolete_friends_ids),len(new_friends_ids),len(existing_friends_ids))

    models.Friend.collection.remove({'id':{'$in':obsolete_friends_ids}})

    i = 0
    while i < len(new_friends_ids):
        twitter_users = api.lookup_users(new_friends_ids[i:i+100])
        for twitter_user in twitter_users:
            friend = models.Friend.collection.find_one({'id':twitter_user.id})
            if not friend:
                friend = models.Friend(id = twitter_user.id,screen_name = twitter_user.screen_name)
            friend['twitter_data'] = twitter_user.raw
            friend.save()
        i+=100

    print "We have %d friends so far" % models.Friend.collection.find().count()

@periodic_task(run_every=datetime.timedelta(seconds=120),default_retry_delay= 10)
def update_score(tweet_id = None):
    if tweet_id:
        tweets = models.Tweet.collection.find({'id':tweet_id})
    else:
        tweets = models.Tweet.collection.find({'timeline':'home','score':{'$gte':0}}).sort('upvotes',1)
    for tweet in tweets:
        elapsed_hours = (datetime.datetime.now()-tweet.tweet_created_at()).total_seconds()/60./60.
        recency_factor = math.exp(-elapsed_hours/24.0)
        earlier_tweets = models.Tweet.collection.find({'user_id':tweet['user_id'],'created_at':{'$lt':tweet['created_at']}}).sort('created_at',-1)
        if earlier_tweets.count():
            earlier_tweet = earlier_tweets[0]
            earlier_tweet_elapsed_hours  = (tweet.tweet_created_at()-earlier_tweet.tweet_created_at()).total_seconds()/60./60.
            repetition_factor = 1.0-math.exp(-earlier_tweet_elapsed_hours/10.0)
        else:
            repetition_factor = 1
        if 'upvotes' and 'downvotes' in tweet:
            votes_score = (tweet['upvotes']/(1+tweet['downvotes']))*10
        else:
            votes_score = 0
        link_score = len(re.findall(r"http://",tweet['twitter_data']['text'],re.I))*10
        followers_score = math.log(1+tweet['twitter_data']['user']['followers_count'])
        total_score = (link_score+votes_score+followers_score)*recency_factor*repetition_factor
        tweet['score'] = math.floor(total_score)
        tweet.save()


@periodic_task(run_every=datetime.timedelta(seconds=120),default_retry_delay= 10)
def update_home_timeline():
    return update_timeline(timeline = 'home')

@periodic_task(run_every=datetime.timedelta(seconds=120),default_retry_delay= 10)
def update_mentions_timeline():
    return update_timeline(timeline = 'mentions')

@periodic_task(run_every=datetime.timedelta(seconds=120),default_retry_delay= 10)
def update_retweets_timeline():
    return update_timeline(timeline = 'retweets')

@task
def update_timeline(timeline = 'home'):
    if timeline not in ['home','user','mentions','retweets']:
        raise Exception("Invalid timeline parameter!")
    since_id_key = timeline+'_since_id'
    preferences = models.Preferences.collection.find_one({'application':'timeline'})
    if not preferences:
        preferences = models.Preferences(application = 'timeline')

    auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY, global_settings.TWITTER.CONSUMER_KEY_SECRET)
    auth.set_access_token(global_settings.TWITTER.ACCESS_TOKEN, global_settings.TWITTER.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    api_funcs = {
        'home':api.home_timeline,
        'user':api.user_timeline,
        'mentions':api.mentions_timeline,
        'retweets':api.retweets_of_me,
    }

    since_id = 0

    if since_id_key in preferences:
        since_id = preferences[since_id_key]

    tweets = []
    max_id = 0
    cnt = 0
    while True:
        cnt+=1
        args = {
                'count' : 200,
        }
        if since_id:
            args['since_id'] = since_id
        if max_id:
            args['max_id'] = max_id
        api_func = api_funcs[timeline]
        tweets_chunk = api_func(**args)
        tweets.extend(tweets_chunk)
        if len(tweets):
            max_id = min(map(lambda x:x.id,tweets))-1
        print "Fetched %d tweets so far..." % len(tweets)
        if len(tweets_chunk) < args['count'] or cnt > 10:
            break

    for tweet in tweets:
        tweet_instance = models.Tweet().collection.find_one({'id':tweet.id})
        if not tweet_instance:
            tweet_instance = models.Tweet()
        tweet_instance['twitter_data'] = tweet.raw
        tweet_instance['id'] = tweet.id
        tweet_instance['timeline'] = timeline
        if timeline == 'home':
            tweet_instance['score'] = 1
        tweet_instance['created_at'] = tweet.created_at
        tweet_instance['user_id'] = tweet.user.id
        tweet_instance['user_screen_name'] = tweet.user.screen_name.lower()
        tweet_instance.save()

    print "Found %d new tweets" % len(tweets)

    if len(tweets):
        preferences[since_id_key] = max(map(lambda x:x.id,tweets))
    preferences.save()
