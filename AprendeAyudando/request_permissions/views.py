from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Request_permissions



@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def index(request):
    return HttpResponse("Solo puede entrar un Alumno o Admin")