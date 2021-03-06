import mongobean.orm as orm
import datetime

class Statistics(orm.Document):
    pass

class Follower(orm.Document):
    pass

class Friend(orm.Document):
    pass

class Retweet(orm.Document):
    pass

class Mention(orm.Document):
    pass

class Question(orm.Document):
    pass

class HelpRequest(orm.Document):
    pass

class HelpOffer(orm.Document):
    pass

class Thanks(orm.Document):
    pass

class Announcement(orm.Document):
    pass

class Event(orm.Document):
    pass

class Tweet(orm.Document):

    def tweet_created_at(self):
        return datetime.datetime.strptime(self['twitter_data']['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

class Preferences(orm.Document):
    pass