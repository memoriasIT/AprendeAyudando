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
    success = False

    # If the current logged user isn't enrolled in the course then add him
    if request.user not in course.enrolled_users.all():
        course.enrolled_users.add(request.user)
        success = True

    if success:
        return HttpResponse("Bienvenido %s, ahora estás inscrito en el curso: %s." % (request.user.username, course.title))
    else:
        return HttpResponse("ERROR: Ya estás inscrito en este curso: %s." % course.title)

    # Return to course
    # return render(request, 'courses/detail.html', {'course': course})



@login_required
def leave(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    success = False
    # If the current logged user isn't enrolled in the course then add him
    if request.user in course.enrolled_users.all():
        course.enrolled_users.remove(request.user)
        success = True

    if success:
        return HttpResponse("Ya no estás inscrito en este curso: %s." % course.title)
    else:
        return HttpResponse("ERROR: No puedes cancelar tu inscripción en el siguiente curso porque no estás inscrito: %s." % course.title)


# @permission_required('createCourse TODO')
# def createCourse(request):
#     # // TODO
