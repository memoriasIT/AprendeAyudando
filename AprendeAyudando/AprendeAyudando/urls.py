from django.contrib import admin
from django.urls import include, path

from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.landingpage),

    #  ACCOUNT
    url('register/', views.user_register, name='user_register'),
    url('account/', views.account, name='account'),
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

    # COURSES AND ACTIVITIES
    path('forum/', include('forum.urls')),
    path('courses/', include('courses.urls')),
    path('activity/', include('activity.urls')),

    # MISCELLANEOUS
    path('requestpermissions/', include('request_permissions.urls')),
]
