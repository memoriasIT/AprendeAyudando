from django.contrib import admin
from .models import Forum, Debate, Message


class AdminForum(admin.ModelAdmin): 
    pass
    list_display=("title","author")
    search_fields=("title",)   #Para realizar barra de busqueda

class AdminDebate(admin.ModelAdmin):
    list_display=("title","author")
    search_fields=("title",)   #Para realizar barra de busqueda

class AdminMessage(admin.ModelAdmin):
    list_display=("author", "debate")
    search_fields=("author",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"


admin.site.register(Forum,AdminForum)
admin.site.register(Debate,AdminDebate)
admin.site.register(Message,AdminMessage)
