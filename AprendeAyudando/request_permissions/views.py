from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Request_permissions
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def index(request):
    return render(request, 'request_permissions/request_form.html')

@login_required
@permission_required('request_permissions.delete_request_permissions', raise_exception=True)
def give_permissions(request):
    ctx = { "permission_requests": Request_permissions.objects.all() } 
    return render(request, 'request_permissions/give_permissions.html', ctx)

@login_required
@permission_required('request_permissions.delete_request_permissions', raise_exception=True)
def accept(request, request_id):
    obj = get_object_or_404(Request_permissions, pk=request_id)
    obj = Request_permissions.objects.get(pk=request_id)
    requester = getattr(obj, "requester")
    role = getattr(obj, "role")
    
    my_group = Group.objects.get(name=role) 
    my_group.user_set.add(requester)
    
    obj.delete()

    return give_permissions(request)

@login_required
@permission_required('request_permissions.delete_request_permissions', raise_exception=True)
def deny(request, request_id):
    Request_permissions.objects.get(pk=request_id).delete()
    return give_permissions(request)
