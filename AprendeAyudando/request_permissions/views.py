from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Request_permissions
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from user_info.models import UserInfo
from .models import PROFESOR, ENTIDADPUBLICOPRIVADA, ADMINISTRADOR, ESTUDIANTE
from courses.models import Course
from activity.models import Activity
from django.core.mail import send_mail
from messaging.models import *


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

    #Quitamos el rol de alumno
    student_group = Group.objects.get(name=ESTUDIANTE)
    student_group.user_set.remove(request_selected.requester)

    #Quitamos sus cursos asociados y sus actividades con acceso restringido asociados
    listCourses = Course.objects.filter(enrolled_users=request_selected.requester)
    for course in listCourses:
        course.enrolled_users.remove(request_selected.requester)
    listActivities = Activity.objects.filter(enrolled_users=request_selected.requester, restricted_entry=True)
    for activity in listActivities:
        activity.enrolled_users.remove(request_selected.requester)


    if request_selected.role == PROFESOR:
        new_user_info = UserInfo.objects.create(
            user=request_selected.requester, 
            phone=request_selected.phone
        )
        new_user_info.save()
    elif request_selected.role == ENTIDADPUBLICOPRIVADA:
        new_user_info = UserInfo.objects.create(
            user=request_selected.requester, 
            phone=request_selected.phone, 
            organization_name=request_selected.organization_name
        )
        new_user_info.save()
    """if role == ADMINISTRADOR:
        requester.is_superuser = True
        requester.is_staff = True
        requester.is_admin = True
        requester.save()"""

    subject = 'Solicitud de rol aceptada'
    message = 'Hola {}. Se le ha sido garantizado el rol de \"{}\" tal y como pidió en su solicitud. Se han eliminado sus anteriores vínculos con los cursos y actividades en las que estuviera inscrito. Desde ahora puede empezar a crear sus {}.\nEsperamos que disfrute su experiencia.'.format(new_user_info.user.username, request_selected.role, "propios cursos" if request_selected.role == PROFESOR else "propias actividades")
    email_from = 'infoaprendeayudando@gmail.com'
    email_to = [new_user_info.user.email]
    send_mail(subject, message, email_from, email_to, fail_silently=True)

    mm = MessagingMessage.objects.create(
        title=subject,
        text=message,
        user_origin=User.objects.get(email=email_from),
        user_destination=User.objects.get(email=email_to[0])
    )
    mm.save()
    
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
        new_request = Request_permissions.objects.create(
            requester = request.user, 
            role = role, 
            requester_name = request.user.first_name, 
            requester_email = request.user.email,
            phone = telefono
        )
    else:
        org = request.POST["org"]
        role = ENTIDADPUBLICOPRIVADA
        new_request = Request_permissions.objects.create(
            requester = request.user, 
            role = role, 
            requester_name = request.user.first_name, 
            requester_email = request.user.email,
            phone = telefono,
            organization_name = org
        )
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