from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from AprendeAyudando.views import has_group

from forum.models import Forum
from resources.models import Resource
from .models import Activity
from .models import ActivityRequest
from quiz.models import Quiz
from AprendeAyudando.templatetags.auth_extras import ACTIVITY

#Queries
from django.db.models import Q


def index(request):
    activityList = Activity.objects.order_by('-pub_date')[:5] 

    #Miramos si tiene permisos de añadir actividades(en un principio solo Admins y EntidadesPP) para mostrar o no mostrar el enlace de "crear actividad"
    is_entity = False
    if request.user.has_perm('activity.add_activity'):
        is_entity = True
    context = {
        'activityList': activityList,
        'is_entity': is_entity
    }
    return render(request, 'activity/index.html', context)

@login_required
def enrolled(request):
    activityList = Activity.objects.filter(Q(enrolled_users=request.user) | Q(entity=request.user)).distinct()

    #Miramos si tiene permisos de añadir actividades(en un principio solo Admins y EntidadesPP) para mostrar o no mostrar el enlace de "crear actividad"
    is_entity = False
    if request.user.has_perm('activity.add_activity'):
        is_entity = True
    context = {
        'activityList': activityList,
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
            if request.user not in activity.banned_users.all():
                new_activity_request = ActivityRequest.objects.create(requester=request.user, activity=activity)
                new_activity_request.save()
                context['exist_activity_request'] = True
            else:
                return banned(request, activity_id)
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
    if activity.restricted_entry and not request.user.is_authenticated:
        return inscription(request, activity_id)
    
    isOwner = False
    if request.user==activity.entity:
        isOwner = True
    # Si tiene acceso restringido y ademas no esta inscrito(como Entidad o como Estudiante) entonces vamos al proceso de inscripcion
    if request.user not in activity.enrolled_users.all() and not isOwner and activity.restricted_entry:
        return inscription(request, activity_id)

    #-----------------------------------------FOROS-----------------------------------------
    forumListCourse = Forum.objects.filter(activityCourseType='Activity', activityCourseFk=activity.id)

    #-----------------------------------------RECURSOS-----------------------------------------
    resourceListCourse = Resource.objects.filter(activityCourseType='Activity', activityCourseFk=activity.id)

    #-------------------------------------------TEST-------------------------------------------
    quizListActivity = Quiz.objects.filter(activity=activity)

    #Para mostrarnos el boton de "Desmatricular" o "Desvincular Actividad"
    show_de_enroll = False
    if request.user in activity.enrolled_users.all():
        show_de_enroll = True

    context = {
        'activity': activity,
        'usuario': request.user,
        'isOwner': isOwner,
        'show_de_enroll': show_de_enroll,
        'forumListCourse': forumListCourse,
        'resourceListCourse': resourceListCourse,
        'quizListActivity': quizListActivity,
        'courseOrActivity': ACTIVITY
    }
    if (request.method=='POST' and request.user not in activity.enrolled_users.all() and request.user.is_authenticated and request.user!=activity.entity):
        activity.enrolled_users.add(request.user)
        context['show_de_enroll'] = True

    return render(request, 'activity/activity.html',context)



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

@login_required
@permission_required('activity.delete_activity', raise_exception=True)
def delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    print(activity)
    print(request.method)

    Activity.objects.filter(id=activity_id).delete()
    return index(request)

@login_required
@permission_required('activity.add_activity', raise_exception=True)
def users(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    userList = []
    for u in User.objects.all():
        if u in activity.enrolled_users.all():
            userList.append(u)

    context = {
        'activity' : activity,
        'userList': userList,
    }

    return render(request, 'activity/users.html', context)

@login_required
@permission_required('activity.add_activity', raise_exception=True)
def removeUser(request, activity_id, user_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    user = get_object_or_404(User, pk=user_id)
    activity.enrolled_users.remove(user)
    activity.banned_users.add(user)
    return users(request, activity_id)

@login_required
def banned(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    context = {
        'activity': activity
    }
    return render(request, 'activity/banned.html', context)
