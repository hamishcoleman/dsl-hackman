"""hackman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.conf.urls import re_path, include
from django.http import HttpResponse
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from . import views
from . import rest_api
from . import screen_urls


def robots(request):
    return HttpResponse('User-agent: *\nDisallow: /',
                        content_type='text/plain')


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^screen/', screen_urls.urls),
    re_path(r'^robots.txt$', robots),
    re_path(r'^login/', views.login, name='login'),
    re_path(r'^logout/', views.logout),

    re_path(
        '^password_change/$',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    re_path(
        '^password_change/done/$',
        views.password_change_done,
        name='password_change_done'
    ),
    re_path(
        '^password_reset/$',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    re_path(
        '^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    re_path(
        '^reset/(?P<uidb64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  # noqa
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    re_path('^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
            name='password_reset_complete'),

    re_path(r'^door_open/', views.door_open),
    re_path(r'^rfid_pair/', views.rfid_pair),
    re_path(
        r'^account_actions/',
        views.account_actions,
        name='account_actions'
    ),
    re_path(r'^account_create/', views.account_create, name='account_create'),
    re_path(r'^payment_submit/', views.payment_submit),
    re_path(r'^$', views.index, name='index'),
    re_path(
        r'^oauth/',
        include('oauth2_provider.urls', namespace='oauth2_provider')
    ),

    re_path(r'^api/v1/profile/', rest_api.profile),
    re_path(r'^api/v1/tags_not_matching/', rest_api.tags_not_matching),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
