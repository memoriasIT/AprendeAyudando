from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Activity

@login_required
def index(request):
    activityList = Activity.objects.order_by('-pub_date')[:5]
    

    id_activities_list_inscripted = []
    for activity in activityList:
        if request.user in activity.enrolled_users.all() or request.user==activity.entity:
            id_activities_list_inscripted.extend([activity.id]) 

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
def inscription(request, activity_id): #Esto antes era details
    activity = get_object_or_404(Activity, pk=activity_id)
    return render(request, 'activity/inscription.html', {'activity': activity})

@login_required
def join(request, activity_id): #Esto antes era join
    activity = get_object_or_404(Activity, pk=activity_id)
    
    # // TODO add logic to add user to course
    success = False

    # If the current logged user isn't enrolled in the course then add him
    if request.user not in activity.enrolled_users.all():
        activity.enrolled_users.add(request.user)
        success = True

    return render(request, 'activity/activity.html',{'usuario': request.user, 'activity': activity, 'success': success})

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
        return HttpResponse("Ya no estás inscrito en esta actividad: %s." % activity.title)
    else:
        return HttpResponse("ERROR: No puedes cancelar tu inscripción en la siguiente actividad porque no estás inscrito: %s." % activity.title)



@login_required
@permission_required('activity.add_activity', raise_exception=True)
def createActivity(request):

    if request.method=="POST":
        new_activity_name=request.POST["new_activity_name"]
        new_activity = Activity.objects.create(title=new_activity_name, entity=request.user)
        new_activity.save()
        return HttpResponse("Se ha creado la actividad: %s" % new_activity_name)
    return render(request, 'activity/create.html',{})
