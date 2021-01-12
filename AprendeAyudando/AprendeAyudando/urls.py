"""AprendeAyudando URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.contrib.auth import views as auth_views
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('', views.landingpage),

    url(r'^schedule/', include('schedule.urls')),
    url(r'^fullcalendar/', TemplateView.as_view(template_name="calendar/fullcalendar.html"), name='fullcalendar'),

    url('register/', views.user_register, name='user_register'),
    url('account/', views.account, name='account'),
    url('accountdelete/', views.delete_account, name='account_delete'),
    
    path('accounts/', include('django.contrib.auth.urls')),
        # accounts/login/ [name='login']
        # accounts/logout/ [name='logout']
        # accounts/password_change/ [name='password_change']
        # accounts/password_change/done/ [name='password_change_done']
        # accounts/password_reset/ [name='password_reset']
        # accounts/password_reset/done/ [name='password_reset_done']
        # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
        # accounts/reset/done/ [name='password_reset_complete']
    
    path('admin/', admin.site.urls),
    path('forum/', include('forum.urls')),
    path('courses/', include('courses.urls')),
    path('activity/', include('activity.urls')),
    path('news/', include('news.urls')),
    path('requestpermissions/', include('request_permissions.urls')),
    path('quiz/', include('quiz.urls')),
    path('review/', include('review.urls')),
    path('resources/', include('resources.urls')),
    path('recoverpassword/', views.recoverpassword, name="recoverpassword"),
    path('modify/<str:username>', views.modify, name="modify"),
    path('update/<str:username>', views.update, name="update"),
    path('messaging/', include('messaging.urls')),
]

admin.site.site_header = 'Administración Aprende Ayudando'
admin.site.index_title = 'Administración'
admin.site.site_title = 'Aprende Ayudando'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)