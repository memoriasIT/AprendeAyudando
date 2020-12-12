from django.contrib import admin
from .models import UserInfo

class AdminUserInfo(admin.ModelAdmin):
    list_display=("user","phone", "organization_name")
    search_fields=("user","phone",)   #Para realizar barra de busqueda

admin.site.register(UserInfo,AdminUserInfo)
