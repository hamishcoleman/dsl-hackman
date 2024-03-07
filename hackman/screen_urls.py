from django.conf.urls import re_path

from . import screen_views as views


urls = ([
    re_path(r'^welcome/', views.welcome),
    re_path(r'^remind_payment/', views.remind_payment),
    re_path(r'^unpaid_membership/', views.unpaid_membership),
    re_path(r'^unpaired_card/', views.unpaired_card),
    re_path(r'^poll/', views.poll),
    re_path(r'^$', views.index),
], 'screen', 'screen')
