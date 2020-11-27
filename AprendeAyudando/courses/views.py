from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from .models import Course

@login_required
def index(request):
    courseList = Course.objects.order_by('-pub_date')[:5]
    

    id_courses_list_inscripted = []
    for curso in courseList:
        if request.user in curso.enrolled_users.all() or request.user==curso.teacher:
            id_courses_list_inscripted.extend([curso.id]) 

    context = {
        'courseList': courseList,
        'courses_list_inscripted' : id_courses_list_inscripted
    }
    return render(request, 'courses/index.html', context)

@login_required
def inscription(request, course_id): #Esto antes era details
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/inscripcion.html', {'course': course})

@login_required
def join(request, course_id): #Esto antes era join
    course = get_object_or_404(Course, pk=course_id)
    
    # // TODO add logic to add user to course
    success = False

    # If the current logged user isn't enrolled in the course then add him
    if request.user not in course.enrolled_users.all():
        course.enrolled_users.add(request.user)
        success = True

    return render(request, 'courses/curso.html',{'usuario': request.user, 'course': course, 'success': success})

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



@login_required
@permission_required('courses.add_course', raise_exception=True)
def createCourse(request):

    if request.method=="POST":
        new_course_name=request.POST["new_course_name"]
        new_course = Course.objects.create(title=new_course_name, teacher=request.user)
        new_course.save()
        return HttpResponse("Se ha creado el curso: %s" % new_course_name)
    return render(request, 'create.html',{})

