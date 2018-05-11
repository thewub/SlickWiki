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

    path('admin/', admin.site.urls),

    # Recent changes
    path('special/recentchanges/', 
        ListView.as_view(
            model=Revision,
            paginate_by=20,
            template_name='wiki/recent_changes.html') ),

    # User stuff
    path('special/login/', django.contrib.auth.views.login, name='login'),
    path('special/logout/', django.contrib.auth.views.logout, {'next_page': '/'}),
    path('special/createaccount/', wiki.views.create_account),

    path(r'special/userlist/', 
        ListView.as_view(
            model=User,
            ordering=['date_joined'],
            paginate_by=20,
            template_name='wiki/user_list.html') ),

    # User
    path('user/<username>/', wiki.views.user_info),

    # Search articles
    path('special/search/', wiki.views.get_search_results),

    # Individual revision
    path('revision/<int:pk>/', DetailView.as_view(model=Revision)),

    # Diff
    path('special/diff/<int:rev1id>/<int:rev2id>/', wiki.views.diff),
    
    # Index
    path('', ListView.as_view( model=Article, template_name='wiki/index.html', ordering='current_revision' ) ),

    # Edit article
    path('<slug:slug>/edit/', wiki.views.edit_article),

    # History of article
    path('<slug:slug>/history/', wiki.views.article_history),

    # View article
    path('<slug:slug>/', wiki.views.view_article),

]