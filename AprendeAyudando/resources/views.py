from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.shortcuts import render
from courses.models import Course
from activity.models import Activity
from resources.models import Resource
from AprendeAyudando.templatetags.auth_extras import COURSE, ACTIVITY
from activity.views import join as viewsActivityJoin
from courses.views import join as viewsCourseJoin
from django.http import HttpResponseForbidden

@login_required
@permission_required('resources.add_resource', raise_exception=True)
def createResource(request, courseOrActivity, activityCourseFk):
    
    #------------------------CONTROL DE ACCESO-------------------
    if courseOrActivity == COURSE:
        course = get_object_or_404(Course, id=activityCourseFk)
        isOwner = course.teacher == request.user
    else:
        activity = get_object_or_404(Activity, id=activityCourseFk)
        isOwner = activity.entity == request.user
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    #---------------------------FORM POST----------------------
    if request.method=="POST":
        new_resource_name=request.POST["new_resource_name"]
        new_resource_link=request.POST["new_resource_link"]
        if not new_resource_link.startswith('http://') and not new_resource_link.startswith('https://'):
            new_resource_link='http://'+new_resource_link
        new_resource = Resource.objects.create(
            activityCourseFk= activityCourseFk,
            activityCourseType=courseOrActivity,
            resourceText = new_resource_name,
            resourceLink = new_resource_link
        )
        new_resource.save()

        if(courseOrActivity == COURSE):
            return viewsCourseJoin(request, activityCourseFk)
        else:
            return viewsActivityJoin(request, activityCourseFk)
    
    ctx = {
        'activityCourseFk': activityCourseFk,
        'courseOrActivity': courseOrActivity
    }
    return render(request, 'resource/createResource.html', ctx)

@login_required
@permission_required('resources.delete_resource', raise_exception=True)
def delete(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    #------------------------CONTROL DE ACCESO-------------------
    if resource.activityCourseType == COURSE:
        course = get_object_or_404(Course, id=resource.activityCourseFk)
        isOwner = course.teacher == request.user
    else:
        activity = get_object_or_404(Activity, id=resource.activityCourseFk)
        isOwner = activity.entity == request.user
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()

    #------------------------ELIMINACION------------------------
    
    activity_or_course_id = resource.activityCourseFk
    Resource.objects.filter(id=resource_id).delete()

    if resource.activityCourseType == COURSE:
        return viewsCourseJoin(request, activity_or_course_id)
    else:
        return viewsActivityJoin(request, activity_or_course_id)
