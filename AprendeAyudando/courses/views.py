# Models
from .models import Course
from forum.models import Forum

# Session Handling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group

# Routing
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from AprendeAyudando.views import has_group

def index(request):
    courseList = Course.objects.order_by('-pub_date')[:5]
    
    #Miramos si el usuario logeado se encuentra en el curso o si el usuario logeado es el propietario del curso
    id_courses_list_inscripted = []
    for curso in courseList:
        if request.user in curso.enrolled_users.all() or request.user==curso.teacher:
            id_courses_list_inscripted.extend([curso.id]) 

    #Miramos si tiene permisos de añadir cursos(en un principio solo Admins y Profes) para mostrar o no mostrar el enlace de "crear curso"
    is_teacher = False
    if request.user.has_perm('courses.add_course'):
        is_teacher = True
    context = {
        'courseList': courseList,
        'courses_list_inscripted': id_courses_list_inscripted,
        'is_teacher': is_teacher,
        'filtered_by_enrolled': False
    }
    return render(request, 'courses/index.html', context)

@login_required
def enrolled(request):
    courseListAux = Course.objects.order_by('-pub_date')[:5]
    
    courseList = []
    #Miramos si el usuario logeado se encuentra en el curso o si el usuario logeado es el propietario del curso
    id_courses_list_inscripted = []
    for course in courseListAux:
        if request.user in course.enrolled_users.all() or request.user==course.teacher:
            id_courses_list_inscripted.extend([course.id]) 
            courseList.append(course)
    #Miramos si tiene permisos de añadir cursos(en un principio solo Admins y Profes) para mostrar o no mostrar el enlace de "crear curso"
    is_teacher = False
    if request.user.has_perm('courses.add_course'):
        is_teacher = True
    context = {
        'courseList': courseList,
        'courses_list_inscripted': id_courses_list_inscripted,
        'is_teacher': is_teacher,
        'filtered_by_enrolled': True
    }
    return render(request, 'courses/index.html', context)


@login_required
def inscription(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    is_Estudiante_or_superuser = False
    #if request.user.has_perm('courses.view_course'):
    #    grupo = 'Estudiante'
    #if request.user.has_perm('courses.add_course'):
    #    grupo = 'Profesor'
    #if request.user.has_perm('activity.add_activity'):
    #    grupo = 'Entidad'
    if has_group(request.user, 'Estudiante') or request.user.is_superuser:
        is_Estudiante_or_superuser = True

    if request.method=='POST':
        if is_Estudiante_or_superuser:
            course.enrolled_users.add(request.user)
            return join(request, course_id)
        else:
            return HttpResponse("ERROR: Solo un estudiante puede realizar una inscripcion a este curso")    #Nunca deberia de entrar aqui

    context = {
        'is_Estudiante_or_superuser': is_Estudiante_or_superuser,
        'course': course
    }
    return render(request, 'courses/inscription.html', context)

@login_required
def join(request, course_id): #Esto antes era join
    course = get_object_or_404(Course, pk=course_id)

    forumListAux = Forum.objects.all()
    
    #Miramos los foros que pertenecen al curso
    forumListCourse = []
    for forum in forumListAux:
        if course.id == forum.activityCourseFk:
            forumListCourse.append(forum)
    
    # // TODO add logic to add user to course
    success = False
    isTeacher = False
    if request.user==course.teacher:
       isTeacher = True

    # Si request.user intenta acceder a la pagina directamente con el id, nos redirige a la pagina de inscripcion
    if request.user not in course.enrolled_users.all() and not isTeacher:
        return inscription(request, course_id) 

    #Para mostrarnos el boton de "Desmatricular"
    show_de_enroll = False
    if request.user in course.enrolled_users.all():
        show_de_enroll = True

    grupo = 'Invitado';
    if request.user.has_perm('courses.view_course'):
        grupo = 'Estudiante'
    if request.user.has_perm('courses.add_course'):
        grupo = 'Profesor'
    if request.user.has_perm('activity.add_activity'):
        grupo = 'Entidad'

    context = {
        'grupo': grupo,
        'course': course,
        'success': success,
        'usuario': request.user,
        'isTeacher': isTeacher,
        'show_de_enroll':show_de_enroll,
        'forumListCourse': forumListCourse,
    }

    return render(request, 'courses/curso.html', context)

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
        return render(request, 'landingpage/account.html')
    else:
        return HttpResponse("ERROR: No puedes cancelar tu inscripción en el siguiente curso porque no estás inscrito: %s." % course.title)


#Restringimos la entrada a los que puedan añadir cursos, si alguien intenta entrar sin permisos-> Forbiden error
@login_required
@permission_required('courses.add_course', raise_exception=True)
def createCourse(request):

    if request.method=="POST":
        new_course_name=request.POST["new_course_name"]
        new_course = Course.objects.create(title=new_course_name, teacher=request.user)
        new_course.save()
        isTeacher = True

        context = {
        'course': new_course,
        'isTeacher': isTeacher,
    }

        return render(request, 'courses/curso.html',context)
    return render(request, 'courses/create.html',{})

