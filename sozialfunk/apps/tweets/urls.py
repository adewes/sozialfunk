from django.conf.urls.defaults import url,patterns
from django.views.generic.simple import direct_to_template

import tweets.views as views

urlpatterns = patterns('',
    url(r'^index/?$', views.index),
    url(r'^index/(.*)$', views.index),
    url(r'^add_to_category/$', views.add_to_category),
    url(r'^add_to_category/([\d]+)$', views.add_to_category),
    url(r'^add_to_category/([\d]+)/(.*)$', views.add_to_category),
    url(r'^remove_from_category/$', views.remove_from_category),
    url(r'^remove_from_category/([\d]+)/(.*)$', views.remove_from_category),
    url(r'^upvote/$', views.upvote),
    url(r'^upvote/([\d]+)$', views.upvote),
    url(r'^undo_upvote/$', views.undo_upvote),
    url(r'^undo_upvote/([\d]+)$', views.undo_upvote),
    url(r'^get_tweet/$', views.get_tweet),
    url(r'^get_tweet/([\d]+)$', views.get_tweet),
    )
