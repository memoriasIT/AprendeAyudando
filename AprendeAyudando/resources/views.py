from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.shortcuts import render
from courses.models import Course
from activity.models import Activity
from resources.models import Resource
from courses.views import join as curso
from activity.views import join as activity

# Create your views here.
@login_required
#@permission_required('resource.add_resource', raise_exception=True)
def createResource(request, activityCourseFk):

    if request.method=="POST":
        activityCourseType = ' '

        if request.user.has_perm('courses.add_course'):
            activityCourseType = 'Course'
        else:
            activityCourseType = 'Activity'

        new_resource_name=request.POST["new_resource_name"]
        new_resource_link=request.POST["new_resource_link"]
        if not new_resource_link.startswith('http://') and not new_resource_link.startswith('https://'):
            new_resource_link='http://'+new_resource_link
        new_resource = Resource.objects.create(activityCourseFk= activityCourseFk, activityCourseType=activityCourseType, resourceText = new_resource_name, resourceLink = new_resource_link)
        new_resource.save()

        if(activityCourseType == 'Course'):
            return curso(request, activityCourseFk)
        else:
            return activity(request, activityCourseFk)

    return render(request, 'resource/createResource.html', {'activityCourseFk': activityCourseFk})

@login_required
#@permission_required('resource.delete_resource', raise_exception=True)
def delete(request, resource_id):

    resource = get_object_or_404(Resource, pk=resource_id)
    print(resource)
    print(request.method)
    isOwner = True
    if resource.activityCourseType == 'Course':
        course = get_object_or_404(Course, pk=resource.activityCourseFk)
        context = {
            'course': course,
            'isOwner': isOwner,
        }
    else:
        activity =get_object_or_404(Activity, pk=resource.activityCourseFk)
        context = {
            'activity': activity,
            'isOwner': isOwner,
        }
    Resource.objects.filter(id=resource_id).delete()
    if resource.activityCourseType == 'Course':
        return render(request, 'courses/curso.html', context)
    else:
        return render(request, 'activity/activity.html', context)
