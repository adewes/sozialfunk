from django.conf.urls.defaults import url,patterns
from django.views.generic.simple import direct_to_template

import tweets.views as views

urlpatterns = patterns('',
    url(r'^index/?$', views.index),
    )
