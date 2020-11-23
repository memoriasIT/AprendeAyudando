from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Course


def index(request):
    courseList = Course.objects.order_by('-pub_date')[:5]
    context = {
        'courseList': courseList,
    }
    
    return render(request, 'courses/index.html', context)

def details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/detail.html', {'course': course})


def join(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    # // TODO add logic to add user to course

    # Return to course
    return render(request, 'courses/detail.html', {'course': course})




def leave(request, course_id):
    return HttpResponse("You no longer can participate in course id %s." % course_id)