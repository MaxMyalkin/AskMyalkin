from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'ask.views.questions', name='questions'),
     url(r'^question$', 'ask.views.look_answers', name='look_answers'),
     url(r'^user$','ask.views.user_info' , name='user_info'),
     url(r'^index$', 'ask.views.questions', name='questions'),
     url(r'^ask$', 'ask.views.Quest_form', name='Quest_form'),
     url(r'^answer$', 'ask.views.Answer_form', name='Answer_form'),
     url(r'^correct$', 'ask.views.make_correct', name='make_correct'),
     url(r'^registration$', 'ask.views.registration' , name='registration'),
     url(r'^login$' , 'ask.views.login_view' , name='login_view'),
     url(r'^logout$' , 'ask.views.logout_view' , name='logout_view'),
     url(r'^change$' , 'ask.views.change', name='change'),
     url(r'^search$' , 'ask.views.search' , name='search'),
     url(r'^comment_q$' , 'ask.views.comment_q' , name='comment_q'),
     url(r'^comment_a$' , 'ask.views.comment_a' , name='comment_a'),
     url(r'^rating$' , 'ask.views.rating' , name='rating'),
     url(r'^graph$' , 'ask.views.graph' , name='graph'),
     url(r'^dynamic_graph$' , 'ask.views.dynamic_graph' , name='dynamic_graph'),
    # url(r'^, include('')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #url(r'^admin/', include(admin.site.urls)),
)
