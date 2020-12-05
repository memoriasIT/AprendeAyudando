from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from courses.models import Course
from activity.models import Activity
from forum.models import Forum

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

    if forum.activityCourseType == 'Course':
        course = get_object_or_404(Course, pk=forum.activityCourseFk)
        context = {
            'course': course,
        }
    else:
        activity =get_object_or_404(Activity, pk=forum.activityCourseFk)
        context = {
            'activity': activity,
        }
    

    # HTML forms don't allow delete method yet
    if request.method == 'POST': 
        Forum.objects.filter(id=forum_id).delete()
    if forum.activityCourseType == 'Course':
        return render(request, 'courses/curso.html', context)
    else:
        return render(request, 'activity/activity.html', context)


@login_required
def join(request, forum_id): 
    forum = get_object_or_404(Forum, pk=forum_id)

    isAuthor = False

    if request.user == forum.author:
        isAuthor = True
    
    success = False

    # If the current logged user isn't enrolled in the course then add him
    if request.user not in forum.enrolled_users.all():
        forum.enrolled_users.add(request.user)
        success = True

    context = {
        'usuario': request.user,
        'forum': forum,
        'success': success,
        'isAuthor' : isAuthor
    }

    return render(request, 'forum/forum.html',context)
