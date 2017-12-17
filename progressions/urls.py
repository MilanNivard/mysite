from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$',
        login_required(views.progressions), name='progressions'),
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
    #     views.playbutton, name='playbutton'),
    url(r'^table_pro/',
        views.table_pro, name='table_pro'),
    url(r'^prog_bar/',
        views.prog_bar, name='prog_bar'),
    url(r'^table_pro_ans/',
        views.table_pro_ans, name='table_pro_ans'),
    url(r'^left_column_pro/',
        views.left_column_pro, name='left_column_pro'),
    ]
