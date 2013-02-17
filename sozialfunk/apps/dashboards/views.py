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

import global_settings

import functools

def index(request):
    context = RequestContext(request)
    return render_to_response('dashboards/index.html',{},context)
