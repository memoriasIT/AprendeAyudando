# Models
from .models import Course
from forum.models import Forum
from resources.models import Resource
from quiz.models import QuizCourse
from django.contrib.auth.models import User, Group
from AprendeAyudando.templatetags.auth_extras import is_owner

# Session Handling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group

# Routing
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from AprendeAyudando.views import has_group

#Queries
from django.db.models import Q


def index(request):
    courseList = Course.objects.order_by('-pub_date')[:5]

    #Miramos si tiene permisos de añadir cursos(en un principio solo Admins y Profes) para mostrar o no mostrar el enlace de "crear curso"
    is_teacher = False
    if request.user.has_perm('courses.add_course'):
        is_teacher = True

    context = {
        'courseList': courseList,
        'is_teacher': is_teacher,
        'filtered_by_enrolled': False
    }

    return render(request, 'courses/index.html', context)

@login_required
def enrolled(request):
    courseList = Course.objects.filter(Q(enrolled_users=request.user) | Q(teacher=request.user)).distinct()
    
    #Miramos si tiene permisos de añadir cursos(en un principio solo Admins y Profes) para mostrar o no mostrar el enlace de "crear curso"
    is_teacher = False
    if request.user.has_perm('courses.add_course'):
        is_teacher = True
    context = {
        'courseList': courseList,
        'is_teacher': is_teacher,
        'filtered_by_enrolled': True
    }
    return render(request, 'courses/index.html', context)


@login_required
def inscription(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if is_owner(request.user, course.teacher):
        return join(request, course_id)

    is_Estudiante_or_superuser = False
    if has_group(request.user, 'Estudiante') or request.user.is_superuser:
        is_Estudiante_or_superuser = True

    if request.method=='POST':
        if is_Estudiante_or_superuser:
            if request.user in course.banned_users.all():
                return banned(request, course_id)
            else:
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
def banned(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {
        'course': course
    }
    return render(request, 'courses/banned.html', context)

@login_required
def join(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    success = False
    isOwner = is_owner(request.user, course.teacher)

    # Si request.user intenta acceder a la pagina directamente con el id, nos redirige a la pagina de inscripcion
    if request.user not in course.enrolled_users.all() and not isOwner :
        return inscription(request, course_id) 


    #-----------------------------------------FOROS-------------------------------------------
    forumListCourse = Forum.objects.filter(activityCourseType='Course', activityCourseFk=course.id)


    #-----------------------------------------RECURSOS-----------------------------------------
    resourceListCourse = Resource.objects.filter(activityCourseType='Course', activityCourseFk=course.id)

    #-------------------------------------------TEST-------------------------------------------
    quizListCourse = QuizCourse.objects.filter(course=course)

    #-----------------------------------CONTROL DE ELEMENTOS DEL HTML--------------------------
    #Para mostrarnos el boton de "Desmatricular"
    show_de_enroll = False
    if request.user in course.enrolled_users.all():
        show_de_enroll = True

    context = {
        'course': course,
        'success': success,
        'usuario': request.user,
        'isOwner': isOwner,
        'show_de_enroll':show_de_enroll,
        'forumListCourse': forumListCourse,
        'resourceListCourse': resourceListCourse,
        'quizListCourse': quizListCourse
    }

    return render(request, 'courses/curso.html', context)



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
        new_course_description=request.POST["new_course_description"]
        new_course = Course.objects.create(title=new_course_name, description=new_course_description, teacher=request.user)
        new_course.save()
        isOwner = True

        context = {
            'course': new_course,
            'isOwner': isOwner,
        }
        return render(request, 'courses/curso.html',context)

    return render(request, 'courses/create.html',{})

@login_required
@permission_required('courses.delete_course', raise_exception=True)
def delete(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    print(course)
    print(request.method)

    Course.objects.filter(id=course_id).delete()
    return index(request)

@login_required
@permission_required('courses.add_course', raise_exception=True)
def users(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    userList = []
    for u in User.objects.all():
        if u in course.enrolled_users.all():
            userList.append(u)

    context = {
        'course' : course,
        'userList': userList,
    }

    return render(request, 'courses/users.html', context)

@login_required
@permission_required('courses.add_course', raise_exception=True)
def removeUser(request, course_id, user_id):
    course = get_object_or_404(Course, pk=course_id)
    user = get_object_or_404(User, pk=user_id)
    course.enrolled_users.remove(user)
    course.banned_users.add(user)
    return users(request, course_id)