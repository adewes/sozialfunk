from django import template
import re
import datetime

register = template.Library()

@register.filter(name='get_html')
def get_html(tweet):
    if 'retweeted_status' in tweet['twitter_data']:
        twitter_data = tweet['twitter_data']['retweeted_status']
        retweeted = True
    else:
        twitter_data = tweet['twitter_data']
        retweeted = False
    text = twitter_data['text']
    final_text = re.sub(r"(https?://[^\s]+)",r'<a href="\1">\1</a>',text)
    final_text = re.sub(r"@([\w\d]+)",r'<a href="http://twitter.com/\1">@\1</a>',final_text)
    if retweeted:
        final_text = '<strong>RT</strong> @<a href="http://twitter.com/%s">%s</a>' % (twitter_data['user']['screen_name'],twitter_data['user']['screen_name'],)+": "+final_text
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
        if days == 1:   tStr = "day"
        else:           tStr = "days"
        str = str + "%s %s" %(days, tStr)
        return str
    elif hours > 0:
        if hours == 1:  tStr = "hour"
        else:           tStr = "hours"
        str = str + "%s %s" %(hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:tStr = "min"
        else:           tStr = "mins"           
        str = str + "%s %s" %(minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:tStr = "sec"
        else:           tStr = "secs"
        str = str + "%s %s" %(seconds, tStr)
        return str
    else:
        return ""