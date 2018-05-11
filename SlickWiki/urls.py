from django.urls import include, path, re_path
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from wiki.models import Article, Revision, User
import wiki.views
import django.contrib.auth.views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'SlickWiki.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    re_path(r'^admin/', admin.site.urls),

    # Recent changes
    re_path(r'special/recentchanges/?', 
        ListView.as_view(
            model=Revision,
            paginate_by=20,
            template_name='wiki/recent_changes.html') ),

    # User stuff
    re_path(r'special/login/?', django.contrib.auth.views.login, name='login'),
    re_path(r'special/logout/?', django.contrib.auth.views.logout, {'next_page': '/'}),
    re_path(r'special/createaccount/?', wiki.views.create_account),

    re_path(r'special/userlist/?', 
        ListView.as_view(
            model=User,
            ordering=['date_joined'],
            paginate_by=20,
            template_name='wiki/user_list.html') ),

    # User
    re_path(r'user/(?P<username>[-a-zA-Z0-9]+)/?$', wiki.views.user_info),

    # Search articles
    re_path(r'special/search/?', wiki.views.get_search_results),

    # Individual revision
    re_path(r'revision/(?P<pk>\d+)/?$', DetailView.as_view(model=Revision)),

    # Diff
    re_path(r'special/diff/(?P<rev1id>\d+)/(?P<rev2id>\d+)/?$', wiki.views.diff),
    
    # Index
    re_path(r'^$', ListView.as_view( model=Article, template_name='wiki/index.html', ordering='current_revision' ) ),

    # Edit article
    re_path(r'(?P<slug>[-a-zA-Z0-9\- ]+)/edit/?$', wiki.views.edit_article),

    # History of article
    re_path(r'(?P<slug>[-a-zA-Z0-9\- ]+)/history/?$', wiki.views.article_history),

    # View article
    re_path(r'^(?P<slug>[-a-zA-Z0-9\- ]+)/?$', wiki.views.view_article),

]