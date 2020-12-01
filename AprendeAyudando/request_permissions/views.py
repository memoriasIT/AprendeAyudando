from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Request_permissions



@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def index(request):
    return HttpResponse("Solo puede entrar un Alumno o Admin")

@login_required
@permission_required('request_permissions.delete_request_permissions', raise_exception=True)
def give_permissions(request):
    ctx = { "permission_requests": Request_permissions.objects.all() } 
    return render(request, 'request_permissions/give_permissions.html', ctx)

@login_required
@permission_required('request_permissions.delete_request_permissions', raise_exception=True)
def accept(request, request_id):
    # TODO accept then delete:
    Request_permissions.objects.get(pk=request_id).delete()
    pass

@login_required
@permission_required('request_permissions.delete_request_permissions', raise_exception=True)
def deny(request, request_id):
    Request_permissions.objects.get(pk=request_id).delete()
    return give_permissions(request)
