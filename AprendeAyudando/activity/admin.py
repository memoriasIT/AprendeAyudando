from django.contrib import admin
from .models import Activity, ActivityRequest

class AdminActivity(admin.ModelAdmin):
    list_display=("title","entity","id","pub_date")
    search_fields=("title",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

class AdminActivityRequest(admin.ModelAdmin):
    list_display=("requester","activity","pub_date")
    search_fields=("requester",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

admin.site.register(Activity,AdminActivity)
admin.site.register(ActivityRequest,AdminActivityRequest)
