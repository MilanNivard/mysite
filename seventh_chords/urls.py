from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$',
        login_required(views.seventh_chords), name='seventh_chords'),
    url(r'^lvl1/',
        views.all_lvls, name='all_lvls'),
    url(r'^lvl2/',
        views.all_lvls, name='all_lvls'),
    url(r'^lvl3/',
        views.all_lvls, name='all_lvls'),
    url(r'^lvl4/',
        views.all_lvls, name='all_lvls'),
    url(r'^lvl5/',
        views.all_lvls, name='all_lvls'),
    url(r'^lvl6/',
        views.all_lvls, name='all_lvls'),
    # url(r'^playbutton/',
    #    views.playbutton, name='playbutton'),
    url(r'^table_sev/',
        views.table_sev, name='table_sev'),
    url(r'^prog_bar/',
        views.prog_bar, name='prog_bar'),
    url(r'^left_column/',
        views.left_column, name='left_column'),
    ]
