from django.shortcuts import render
# Session Handling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

#Extras
from AprendeAyudando.templatetags.auth_extras import is_owner

#HTTP
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

#Models
from courses.models import Course
from quiz.models import Quiz, QuizCourse

@login_required
@permission_required('quiz.add_quiz', raise_exception=True)
def createQuizCourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    isOwner = False

    if is_owner(request.user, course.teacher):
        isOwner = True
    ctx = {
        'is_course':True,
        'isOwner':isOwner,
        'course': course,
    }

    #----------------------------------------FORM-------------------------------------------
    if request.method=="POST":
        new_quiz_title = request.POST["new_quiz_title"]
        new_quiz_description = request.POST["new_quiz_description"]
        new_quiz_is_repeatable = request.POST["is_repeatable"]=='si'
        new_quiz_show_qualification = request.POST["show_qualification"]=='si'
        
        new_quiz = QuizCourse.objects.create(
            title=new_quiz_title,
            description=new_quiz_description,
            repeatable=new_quiz_is_repeatable,
            show_qualification=new_quiz_show_qualification,
            course=course
        )
        new_quiz.save()
        return HttpResponse("Se ha creado el curso con titulo: %s." %new_quiz.title)
    
    return render(request, 'quiz/create.html', ctx)#HttpResponse("Esta es la futura pagina de crear QUIZ para el curso: %s." %course.title)

@login_required
@permission_required('quiz.add_quiz', raise_exception=True)
def startCreateQuizCourse(request, course_id):
    if request.method=="POST":
        new_quiz_title = request.POST["new_quiz_title"]
        new_quiz_description = request.POST["new_quiz_description"]
        new_quiz_is_repeatable = request.POST["is_repeatable"]=='si'
        new_quiz_show_qualification = request.POST["show_qualification"]
        
        new_quiz = Quiz.objects.create(
            title=new_quiz_title,
            description=new_quiz_description,
            repeatable=new_quiz_is_repeatable,
            show_qualification=new_quiz_show_qualification
        )
        new_quiz.save()
        return HttpResponse("Se ha creado el curso con titulo: %s." %new_quiz.title)
    else:
        HttpResponseForbidden()
