from celery.task import task
import settings as settings
import tweets.models as tweets_models
import workers.models as workers_models

import datetime
import time
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


@task
def update_followers():
    preferences = workers_models.Preferences.collection.find_one({'application':'followers'})

    if not preferences:
        preferences = workers_models.Preferences(application = 'followers')

    auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY, global_settings.TWITTER.CONSUMER_KEY_SECRET)
    auth.set_access_token(global_settings.TWITTER.ACCESS_TOKEN, global_settings.TWITTER.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    followers_ids_cursor = tweepy.Cursor(api.followers_ids,screen_name = 'BarackObama')

    followers_ids = []

    for follower_id in followers_ids_cursor.items():
        followers_ids.append(follower_id)
        if len(followers_ids) > 5000:
            break

    followers_ids = followers_ids[:200]

    print len(followers_ids)

    obsolete_followers_ids = map(lambda x:x.id,tweets_models.Follower.collection.find({'id':{'$nin':followers_ids}}))
    existing_followers_ids = map(lambda x:x.id,tweets_models.Follower.collection.find({'id':{'$in':followers_ids}}))
    new_followers_ids = [id for id in followers_ids if id not in existing_followers_ids]

    print "%d obsolete followers, %d new followers and %d existing followers" % (len(obsolete_followers_ids),len(new_followers_ids),len(existing_followers_ids))

    tweets_models.Follower.collection.remove({'id':{'$in':obsolete_followers_ids}})

    i = 0
    while i < len(new_followers_ids):
        twitter_users = api.lookup_users(new_followers_ids[i:i+100])
        for twitter_user in twitter_users:
            follower = tweets_models.Follower.collection.find_one({'id':twitter_user.id})
            if not follower:
                follower = tweets_models.Follower(id = twitter_user.id,screen_name = twitter_user.screen_name)
            follower['twitter_data'] = twitter_user.raw
            follower.save()
        i+=100

    print "We have %d followers so far" % tweets_models.Follower.collection.find().count()
 

@task
def update_friends():
    preferences = workers_models.Preferences.collection.find_one({'application':'followers'})

    if not preferences:
        preferences = workers_models.Preferences(application = 'followers')

    auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY, global_settings.TWITTER.CONSUMER_KEY_SECRET)
    auth.set_access_token(global_settings.TWITTER.ACCESS_TOKEN, global_settings.TWITTER.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    print "Found %d new tweets" % len(tweets)

    if len(tweets):
        preferences[since_id_key] = max(map(lambda x:x.id,tweets))
    preferences.save()

def update_friends():
    preferences = workers_models.Preferences.collection.find_one({'application':'followers'})

    if not preferences:
        preferences = workers_models.Preferences(application = 'followers')

    auth = tweepy.OAuthHandler(global_settings.TWITTER.CONSUMER_KEY, global_settings.TWITTER.CONSUMER_KEY_SECRET)
    auth.set_access_token(global_settings.TWITTER.ACCESS_TOKEN, global_settings.TWITTER.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    print "Found %d new tweets" % len(tweets)

    if len(tweets):
        preferences[since_id_key] = max(map(lambda x:x.id,tweets))
    preferences.save()


@periodic_task(run_every=datetime.timedelta(seconds=60),default_retry_delay= 10)
def update_timeline(timeline = 'home'):
    if timeline not in ['home','user','mentions','retweets']:
        raise Exception("Invalid timeline parameter!")
    since_id_key = timeline+'_since_id'
    preferences = workers_models.Preferences.collection.find_one({'application':'timeline'})
    if not preferences:
        preferences = workers_models.Preferences(application = 'timeline')

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
        tweet_instance = tweets_models.Tweet().collection.find_one({'id':tweet.id})
        if not tweet_instance:
            tweet_instance = tweets_models.Tweet()
        tweet_instance['twitter_data'] = tweet.raw
        tweet_instance['id'] = tweet.id
        tweet_instance['created_at'] = tweet.created_at
        tweet_instance['user_id'] = tweet.user.id
        tweet_instance['user_screen_name'] = tweet.user.screen_name.lower()
        tweet_instance.save()

    print "Found %d new tweets" % len(tweets)

    if len(tweets):
        preferences[since_id_key] = max(map(lambda x:x.id,tweets))
    preferences.save()
