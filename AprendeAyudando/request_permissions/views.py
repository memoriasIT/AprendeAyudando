from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Request_permissions
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from user_info.models import UserInfo
from django.utils import timezone
from .models import PROFESOR, ENTIDADPUBLICOPRIVADA, ADMINISTRADOR

@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def index(request):

    solicitudExistente = False
    rp = Request_permissions.objects.filter(requester=request.user)
    if rp.exists():
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
    request_selected = get_object_or_404(Request_permissions, pk=request_id)
    
    my_group = Group.objects.get(name=request_selected.role)
    my_group.user_set.add(request_selected.requester)

    if request_selected.role == PROFESOR:
        new_user_info = UserInfo.objects.create(
            user=request_selected.requester, 
            phone=request_selected.phone
            )
        new_user_info.save()
    elif request_selected.role == ENTIDADPUBLICOPRIVADA:
        new_user_info = UserInfo.objects.create(
            user=request_selected.user, 
            phone=request_selected.telefono, 
            organization_name=request_selected.org
            )
        new_user_info.save()
    """if role == ADMINISTRADOR:
        requester.is_superuser = True
        requester.is_staff = True
        requester.is_admin = True
        requester.save()"""
    
    request_selected.delete()

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
    if requestType == PROFESOR:
        role = PROFESOR
        #new_user_info = UserInfo.objects.create(user=request.user, phone=telefono)
        new_request = Request_permissions.objects.create(
        requester = request.user, 
        role = role, 
        requester_name = request.user.first_name, 
        requester_email = request.user.email,
        phone = telefono
        )
    else:
        org = request.POST["org"]
        #new_user_info = UserInfo.objects.create(user=request.user, phone=telefono, organization_name=org)
        role = ENTIDADPUBLICOPRIVADA
        new_request = Request_permissions.objects.create(
            requester = request.user, 
            role = role, 
            requester_name = request.user.first_name, 
            requester_email = request.user.email,
            phone = telefono,
            organization_name = org
            )
    #new_user_info.save()
    new_request.save()

    return render(request, 'landingpage/account.html')
    
@login_required
@permission_required('request_permissions.add_request_permissions', raise_exception=True)
def redirectForm(request, requestType):
    if requestType == PROFESOR:
        return render(request, 'request_permissions/request_form_prof.html')
    elif requestType == ENTIDADPUBLICOPRIVADA:
        return render(request, 'request_permissions/request_form_ent.html')
    else:
        return HttpResponse("Error: El requestType no existe")