from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from tinymce.models import HTMLField


urlpatterns=[
    url(r'^$', views.welcome, name="welcome"),
    url(r'^profile$', views.user_profile, name='user-profile'),
    url(r'^edit/profile$', views.edit_profile, name="edit-profile"),
    url(r'^new/project$',views.new_project, name ='new-project'),
    url(r'^api/profile/$', views.ProfileList.as_view(), name='profile-API'),
    url(r'^api/project/$', views.ProjectList.as_view(), name='project-API'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^vote/(?P<id>\d+)', views.rating,name='rating'),
    url(r'^newcomment/(\d+)/$', views.new_comment, name='new-comment'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)