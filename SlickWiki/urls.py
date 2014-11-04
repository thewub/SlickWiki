from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from wiki.models import Article, Revision, User


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SlickWiki.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Recent changes
    url(r'special/recentchanges/?', 
        ListView.as_view(model=Revision, template_name='wiki/recent_changes.html') ),

    # User stuff
    url(r'special/login/?', 'django.contrib.auth.views.login'),
    url(r'special/logout/?', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'special/createaccount/?', 'wiki.views.create_account'),

    url(r'special/userlist/?', ListView.as_view(model=User, template_name='wiki/user_list.html') ),

    # Search articles
    url(r'special/search/?', 'wiki.views.get_search_results'),

    # Individual revision
    url(r'revision/(?P<pk>\d+)/?$', DetailView.as_view(model=Revision)),
    
    # Article list
    url(r'^/?$', ListView.as_view(model=Article) ),

    # Edit article
    url(r'(?P<slug>[-a-zA-Z0-9]+)/edit/?$', 'wiki.views.edit_article'),

    # History of article
    url(r'(?P<slug>[-a-zA-Z0-9]+)/history/?$', 'wiki.views.article_history'),

    # View article
    url(r'^(?P<slug>[-a-zA-Z0-9]+)/?$', 'wiki.views.view_article'),
)
