from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$',
        views.index, name='index'),
    url(r'^signup/$',
        views.signup, name='signup'),
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),

    url(r'^profile/',
        login_required(views.profile), name='profile'),
    url(r'^user_overview/',
        login_required(views.user_overview), name='user_overview'),
    ]
