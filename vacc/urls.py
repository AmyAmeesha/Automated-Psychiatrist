from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import * 
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vacc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', emotion),
    #url(r'^emotion/(/d{1,2}/$', emotion),
)
