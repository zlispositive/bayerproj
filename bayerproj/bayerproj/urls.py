from django.conf.urls import patterns, include, url
from django.contrib import admin
from bayerproj.views import *
# from ta import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'bayerproj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search-form/$',search_form),
    url(r'^search/$', search),
    url(r'^thanks/$', thanks),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', user_login, name='login'),
    url(r'^index/$', index),
    url(r'^index/(?P<title>\w+)/$', category, name='category'), #20140502-2332
    url(r'^add_request/$', add_request, name='add_request'), #20140503-1937
    url(r'^del_request/(?P<listnumber>\w+)/$', del_request, name='del_request'), #20140505-0930
    # url(r'^tackle_request/$', tackle_request, name='tackle_request'), #20140504-0012
    url(r'^tackle_request/(?P<listnumber>\w+)/$', tackle_request, name='tackle_request'), #20140504-2002
    url(r'^processing/(?P<listnumber>\w+)/$', process_request, name='process_request'), #20140505-1255
    url(r'^complete_request/(?P<listnumber>\w+)/$', complete_request, name='complete_request'), #20140505-1549
    url(r'^requestinfo/(?P<listnumber>\w+)/$', requestinfo, name='requestinfo'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^about/$', about, name='about'),
)
