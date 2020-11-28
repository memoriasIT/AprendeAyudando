from django.contrib import admin
from .models import Request_permissions

class AdminRequestPermissions(admin.ModelAdmin):
    list_display=("requester","requester_name","pub_date")
    search_fields=("requester",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

admin.site.register(Request_permissions,AdminRequestPermissions)
