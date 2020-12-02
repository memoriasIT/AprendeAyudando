from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Forum

@login_required
@permission_required('forum.add_forum', raise_exception=True)
def createForum(request, activityCourseFk):
    if request.method=="POST":
        
        activityCourseType = ' '

        if request.user.has_perm('courses.add_course'):
            activityCourseType = 'Course'
        else:
            activityCourseType = 'Activity'

        new_forum_name=request.POST["new_forum_name"]
        new_forum = Forum.objects.create(title=new_forum_name, author=request.user, activityCourseFk= activityCourseFk, activityCourseType=activityCourseType)
        new_forum.save()

        isTeacher = True

        context = {
        'forum': new_forum,
        'isTeacher': isTeacher,
        }
        return render(request, 'forum/forum.html',context)
    return render(request, 'forum/createForum.html', {'activityCourseFk': activityCourseFk})
    


@login_required
@permission_required('forum.delete_forum', raise_exception=True)
def delete(request, forum_id):

    forum = get_object_or_404(Forum, pk=forum_id)
    
    print(forum)
    print(request.method)

    # HTML forms don't allow delete method yet
    if request.method == 'POST': 
        forum.delete() 
        return HttpResponse('El foro se ha eliminado correctamente.')
    else:
        return HttpResponse('Se necesita método POST.')


@login_required
def join(request, forum_id): 
    forum = get_object_or_404(Forum, pk=forum_id)
    
    success = False

    # If the current logged user isn't enrolled in the course then add him
    if request.user not in forum.enrolled_users.all():
        forum.enrolled_users.add(request.user)
        success = True

    return render(request, 'forum/forum.html',{'usuario': request.user, 'forum': forum, 'success': success})
