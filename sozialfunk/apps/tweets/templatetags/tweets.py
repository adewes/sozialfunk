from django import template
import re
import urllib
import datetime
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter(name='tweet_text_as_html')
def tweet_text_as_html(tweet):
    if 'retweeted_status' in tweet['twitter_data']:
        twitter_data = tweet['twitter_data']['retweeted_status']
        retweeted = True
    else:
        twitter_data = tweet['twitter_data']
        retweeted = False
    text = twitter_data['text']
    final_text = urlify(text,tweet)
    if retweeted:
        final_text = '<strong>Retweeted from</strong> @<a href="http://twitter.com/%s">%s</a><br />' % (twitter_data['user']['screen_name'],twitter_data['user']['screen_name'],)+final_text
    return final_text

@register.filter(name='urlify')
def urlify(text,tweet):

    def render_tweet_link(match,tweet_id,url_entities):
        url = match.group(1)
        display_url = url
        for url_entity in url_entities:
            if 'url' in url_entity and url_entity['url'] == url and 'display_url' in url_entity:
                display_url = url_entity['display_url']
        return '<a onclick="count_click(\'%s\')" href="%s">%s</a>' % (tweet_id,url,display_url)

    url_entities = []
    for key in tweet['twitter_data']['entities'].keys():
        url_entities += tweet['twitter_data']['entities'][key]
    if 'retweeted_status' in tweet['twitter_data'] and 'urls' in tweet['twitter_data']['retweeted_status']['entities']:
        for key in tweet['twitter_data']['retweeted_status']['entities'].keys():
            url_entities += tweet['twitter_data']['retweeted_status']['entities'][key]
    final_text = re.sub(r"(https?://[^\s]+)",lambda match:render_tweet_link(match,tweet_id = tweet['twitter_data']['id'],url_entities = url_entities),text)
    final_text = re.sub(r"@([\w\d]+)",r'<a href="http://twitter.com/\1">@\1</a>',final_text)
    final_text = re.sub(r"#([^\s]+)",lambda match:r'<a href="http://twitter.com/search?q=%s&src=hash">#%s</a>' % (urllib.quote((u"#"+match.group(1)).encode("utf-8")),match.group(1)),final_text)
    return final_text

@register.filter(name='human_readable_elapsed_time')
def human_readable_elapsed_time(timestamp):
    
    timeDiff = datetime.datetime.now() - timestamp
    days = timeDiff.days
    hours = timeDiff.seconds/3600
    minutes = timeDiff.seconds%3600/60
    seconds = timeDiff.seconds%3600%60
    
    str = ""
    tStr = ""
    if days > 0:
        if days == 1:   tStr = "Tag"
        else:           tStr = "Tagen"
        str = str + "%s %s" %(days, tStr)
        return str
    elif hours > 0:
        if hours == 1:  tStr = "Stunde"
        else:           tStr = "Stunden"
        str = str + "%s %s" %(hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:tStr = "Minute"
        else:           tStr = "Minuten"           
        str = str + "%s %s" %(minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:tStr = "Sekunde"
        else:           tStr = "Sekunden"
        str = str + "%s %s" %(seconds, tStr)
        return str
    else:
        return ""