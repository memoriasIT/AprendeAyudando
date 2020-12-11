from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Request_permissions
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from user_info.models import UserInfo
from django.utils import timezone

@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def index(request):
    solicitudExistente = False
    
    for r in Request_permissions.objects.all():
        if r.requester == request.user:
            solicitudExistente = True
    context = {"solicitudExistente": solicitudExistente}

    return render(request, 'request_permissions/request_form.html', context)

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

@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def createRequest(request, requestType):
    
    telefono = request.POST["telefono"]
    if requestType == 'Profesor':
        role = 'Profesor'
        new_user_info = UserInfo.objects.create(user=request.user, phone=telefono)
    else:
        org = request.POST["org"]
        new_user_info = UserInfo.objects.create(user=request.user, phone=telefono, organization_name=org)
        role = 'EntidadPublicoPrivada'
    
    new_user_info.save()

    new_request = Request_permissions.objects.create(pub_date = timezone.now, requester = request.user, role = role, requester_name = request.user.first_name + request.user.last_name, requester_email = request.user.email)
    new_request.save()

    return render(request, 'landingpage/account.html')
    
@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def redirectForm(request, requestType):
    if requestType == 'Profesor':
        return render(request, 'request_permissions/request_form_prof.html')
    else:
        return render(request, 'request_permissions/request_form_ent.html')