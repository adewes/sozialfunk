from django.conf.urls.defaults import url,patterns
from django.views.generic.simple import direct_to_template

import profiles.views as views

urlpatterns = patterns('',
    url(r'^logout/?$', views.logout),
    url(r'^login/?$', views.login),
    url(r'^login/(?P<next_url>.*)$', views.login),
    url(r'^settings$', views.profile_settings),
    url(r'^twitter_callback$', views.twitter_callback),
    )
