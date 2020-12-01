from django.contrib import admin
from django.contrib import messages

from .models import Request_permissions
from django.contrib.auth.models import User, Group



class AdminRequestPermissions(admin.ModelAdmin):
    change_form_template = "permissionsForm.html"
    change_list_results_template = "test.html"
    list_display=("requester","requester_name","pub_date", "role")
    search_fields=("requester",)   #Para realizar barra de busqueda
    date_hierarchy="pub_date"

    # Delete the original delete selected elements
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def response_change(self, request, obj):
        if "_aceptarPeticion" in request.POST:
            requester = getattr(obj, "requester")
            role = getattr(obj, "role")
            
            my_group = Group.objects.get(name=role) 
            my_group.user_set.add(requester)
            
            obj.delete()

        if "_denegarPeticion" in request.POST:
            obj.delete() 


        return super().response_change(request, obj)

    def aceptarPeticion(modeladmin, request, queryset): 
        for obj in queryset:
            requester = getattr(obj, "requester")
            role = getattr(obj, "role")
            
            my_group = Group.objects.get(name=role) 
            my_group.user_set.add(requester)
            
            obj.delete()
        messages.success(request, "La(s) peticion(es) seleccionadas han sido aceptadas.") 

    def denegarPeticion(modeladmin, request, queryset): 
        queryset.delete()
        messages.success(request, "La(s) peticion(es) seleccionadas han sido denegadas.") 

    # Hide the add new element button
    def has_add_permission(self, request): 
        return False

    admin.site.add_action(aceptarPeticion, "Aceptar Petición") 
    admin.site.add_action(denegarPeticion, "Denegar Petición") 

    

admin.site.register(Request_permissions,AdminRequestPermissions)







