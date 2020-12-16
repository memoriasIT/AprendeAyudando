from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from AprendeAyudando.views import has_group

from forum.models import Forum
from .models import Activity
from .models import ActivityRequest

def index(request):
    activityList = Activity.objects.order_by('-pub_date')[:5]
    
    #Miramos si el usuario logeado se encuentra en la actividad o si el usuario logeado es el propietario de la actividad
    id_activities_list_inscripted = []
    for activity in activityList:
        if request.user in activity.enrolled_users.all() or request.user==activity.entity:
            id_activities_list_inscripted.extend([activity.id]) 

    #Miramos si tiene permisos de añadir actividades(en un principio solo Admins y EntidadesPP) para mostrar o no mostrar el enlace de "crear actividad"
    is_entity = False
    if request.user.has_perm('activity.add_activity'):
        is_entity = True
    context = {
        'activityList': activityList,
        'activities_list_inscripted': id_activities_list_inscripted,
        'is_entity': is_entity
    }
    return render(request, 'activity/index.html', context)

@login_required
def enrolled(request):
    activityListAux = Activity.objects.order_by('-pub_date')[:5]
    activityList = []
    #Miramos si el usuario logeado se encuentra en la actividad o si el usuario logeado es el propietario de la actividad
    id_activities_list_inscripted = []
    for activity in activityListAux:
        if request.user in activity.enrolled_users.all() or request.user==activity.entity:
            id_activities_list_inscripted.extend([activity.id])
            activityList.append(activity)

    #Miramos si tiene permisos de añadir actividades(en un principio solo Admins y EntidadesPP) para mostrar o no mostrar el enlace de "crear actividad"
    is_entity = False
    if request.user.has_perm('activity.add_activity'):
        is_entity = True
    context = {
        'activityList': activityList,
        'activities_list_inscripted': id_activities_list_inscripted,
        'is_entity': is_entity,
        'filtered_by_enrolled': True,
    }
    return render(request, 'activity/index.html', context)


def inscription(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    is_Estudiante_or_superuser = False
    if has_group(request.user, 'Estudiante') or request.user.is_superuser:
        is_Estudiante_or_superuser = True


    exist_activity_request = False
    if request.user.is_authenticated:   #Para evitar errores
        ar = ActivityRequest.objects.filter(activity=activity, requester=request.user)
        if ar.exists():
            exist_activity_request = True

    context = {
        #'grupo': grupo,
        'activity': activity,
        'is_Estudiante_or_superuser': is_Estudiante_or_superuser,
        'exist_activity_request': exist_activity_request
    }

    
    if request.method=='POST' and activity.restricted_entry:
        if has_group(request.user, 'Estudiante'):
            new_activity_request = ActivityRequest.objects.create(requester=request.user, activity=activity)
            new_activity_request.save()
            context['exist_activity_request'] = True
        elif request.user.is_superuser:
            activity.enrolled_users.add(request.user)
            return join(request, activity_id)

    if activity.restricted_entry:
        return render(request, 'activity/inscription.html', context)
    else:
        return join(request, activity_id)

@login_required
@permission_required('activity.view_activityrequest', raise_exception=True)  
def view_activity_request(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    #Para controlar que otra EntidadPP no acceda(solo podra el dueño o un superusuario)
    if request.user!=activity.entity and not request.user.is_superuser:
        return HttpResponseForbidden()

    user_list = ActivityRequest.objects.filter(activity=activity)

    context = {
        'activity':activity,
        'user_list': user_list,
        'usuario': request.user
    }

    return render(request, 'activity/activityrequest.html', context)


@login_required
@permission_required('activity.view_activityrequest', raise_exception=True)
@permission_required('activity.delete_activityrequest', raise_exception=True)
def action_activity_request(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    if request.method=='POST':
        #Tenemos el nombre del usuario, asi que obtenemos el objeto 
        selected_username = request.POST["selected_username"]   
        usu = get_object_or_404(User, username=selected_username)
        if 'aceptar' in request.POST:
            activity.enrolled_users.add(usu)
            ActivityRequest.objects.filter(requester=usu).delete()
            #return HttpResponse("Se ACEPTO la solicitud")
            return view_activity_request(request, activity_id)
        elif 'rechazar' in request.POST:
            ActivityRequest.objects.filter(requester=usu).delete()
            return view_activity_request(request, activity_id)
    return HttpResponse("error")

def join(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    #Mantenemos un control de quien entra aqui(si la actividad estra restringida)
    if activity.restricted_entry and not request.user.is_authenticated:
        return inscription(request, activity_id)
    
    isOwner = False
    if request.user==activity.entity:
        isOwner = True
    # Si tiene acceso restringido y ademas no esta inscrito(como Entidad o como Estudiante) entonces vamos al proceso de inscripcion
    if request.user not in activity.enrolled_users.all() and not isOwner and activity.restricted_entry:
        return inscription(request, activity_id)

    #-----------------------------------------FOROS-----------------------------------------
    #Miramos los foros que pertenecen a la actividad
    #forumListAux = Forum.objects.all()
    forumListCourse = Forum.objects.filter(activityCourseType='Activity', activityCourseFk=activity.id)
    """forumListCourse = []
    for forum in forumListAux:
        if activity.id == forum.activityCourseFk:   #No se comprueba si "forum" es Type Actividad
            forumListCourse.append(forum)"""

    

    #Para mostrarnos el boton de "Desmatricular" o "Desvincular Actividad"
    show_de_enroll = False
    if request.user in activity.enrolled_users.all():
        show_de_enroll = True

    context = {
        #'grupo': grupo,
        'activity': activity,
        'usuario': request.user,
        'isOwner': isOwner,
        'show_de_enroll': show_de_enroll,
        'forumListCourse': forumListCourse,
    }
    if (request.method=='POST' and request.user not in activity.enrolled_users.all() and request.user.is_authenticated):
        activity.enrolled_users.add(request.user)
        context['show_de_enroll'] = True

    return render(request, 'activity/activity.html',context)

    # Return to course
    # return render(request, 'courses/detail.html', {'course': course})



@login_required
def leave(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)

    success = False
    # If the current logged user isn't enrolled in the course then add him
    if request.user in activity.enrolled_users.all():
        activity.enrolled_users.remove(request.user)
        success = True

    if success:
        return render(request, 'landingpage/account.html')
    else:
        return HttpResponse("ERROR: No puedes cancelar tu inscripción en la siguiente actividad porque no estás inscrito: %s." % activity.title)


#Restringimos la entrada a los que puedan añadir actividades, si alguien intenta entrar sin permisos-> Forbiden error
@login_required
@permission_required('activity.add_activity', raise_exception=True)
def createActivity(request):

    if request.method=="POST":
        new_activity_name=request.POST["new_activity_name"]
        new_activity_description=request.POST["new_activity_description"]
        new_activity_is_restricted=request.POST["is_restricted_entry"]=='si'
        new_activity = Activity.objects.create(title=new_activity_name, description=new_activity_description, entity=request.user,restricted_entry=new_activity_is_restricted)
        new_activity.save()
        return render(request, 'activity/activity.html',{'activity': new_activity, 'isOwner': True})
    return render(request, 'activity/create.html',{})