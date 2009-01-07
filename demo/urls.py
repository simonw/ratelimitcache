from django.conf.urls.defaults import *
from django.http import HttpResponse
from pprint import pformat

import sys; sys.path.append('..')
from ratelimitcache import ratelimit, ratelimit_post

# Regular usage
@ratelimit(minutes=1, requests=10)
def index(request):
    return HttpResponse('Hello, World')


# Slightly weird usage so we can show debug information
class ratelimit_debug(ratelimit):
    def disallowed(self, request):
        return HttpResponse('RATE LIMIT EXCEEDED<br>%s' % pformat(
            self.get_counters(request)
        ))
limiter = ratelimit_debug(prefix = 'rl-debug')
@limiter
def debug(request):
    return HttpResponse(pformat(limiter.get_counters(request)))

# Weird again, this time demonstrating the ratelimit_post decorator
class ratelimit_debug_post(ratelimit_post):
    key_field = 'username'
    def disallowed(self, request):
        return HttpResponse('RATE LIMIT EXCEEDED<br>%s' % pformat(
            self.get_counters(request)
        ))
limiter_post = ratelimit_debug_post(prefix='rl-debug-post')
@limiter_post
def login(request):
    html = """
    <form action="/login/" method="post">
    <p><input type="text" name="username" value="%s"> <input type="submit"></p>
    </form>
    """ % request.POST.get('username', '')
    return HttpResponse(html + pformat(limiter_post.get_counters(request)))

urlpatterns = patterns('',
    (r'^$', index),
    (r'^debug/$', debug),
    (r'^login/$', login),
)
