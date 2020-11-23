from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Course

@login_required
def index(request):
    courseList = Course.objects.order_by('-pub_date')[:5]
    context = {
        'courseList': courseList,
    }
    
    return render(request, 'courses/index.html', context)

@login_required
def details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/detail.html', {'course': course})

@login_required
def join(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # // TODO add logic to add user to course

    # Return to course
    return render(request, 'courses/detail.html', {'course': course})



@login_required
def leave(request, course_id):
    return HttpResponse("You no longer can participate in course id %s." % course_id)


# @permission_required('createCourse TODO')
# def createCourse(request):
#     # // TODO