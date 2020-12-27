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
from quiz.models import Quiz, Question, Answer, Qualification, QuestionAsked
from activity.models import Activity

#Random
from random import random, randint

#Queries
from django.db.models import Q

#Constants
from AprendeAyudando.templatetags.auth_extras import ACTIVITY, COURSE


#-----------------------------------------CREACIÓN DE TESTS---------------------------------------------
@login_required
@permission_required('quiz.add_quizcourse', raise_exception=True)
def createQuiz(request, courseOrActivity, courseOrActivity_id):

    if(courseOrActivity == COURSE):
        course = get_object_or_404(Course, pk=courseOrActivity_id)
        isOwner = is_owner(request.user, course.teacher)
    else:
        activity = get_object_or_404(Activity, pk=courseOrActivity_id)
        isOwner = is_owner(request.user, activity.entity)

    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()

    #----------------------------------ELEMENTOS PARA HTML----------------------------------
    ctx = {
        'isOwner':isOwner,
        'courseOrActivity': courseOrActivity,
        'courseOrActivity_id':courseOrActivity_id
    }

    #----------------------------------------FORM-------------------------------------------
    if request.method=="POST" and (isOwner or request.user.is_superuser):
        new_quiz_title = request.POST["new_quiz_title"]
        new_quiz_description = request.POST["new_quiz_description"]
        new_quiz_is_repeatable = request.POST["is_repeatable"]=='si'
        new_quiz_show_qualification = request.POST["show_qualification"]=='si'
        number_questions = request.POST["number_questions"]
        if(courseOrActivity == COURSE):
            new_quiz = Quiz.objects.create(
                title=new_quiz_title,
                description=new_quiz_description,
                repeatable=new_quiz_is_repeatable,
                show_qualification=new_quiz_show_qualification,
                course=course
            )
        else:
            new_quiz = Quiz.objects.create(
                title=new_quiz_title,
                description=new_quiz_description,
                repeatable=new_quiz_is_repeatable,
                show_qualification=new_quiz_show_qualification,
                activity=activity
            )
        new_quiz.save()

        ctx['quiz'] = new_quiz
        ctx['number_questions'] = int(number_questions)
        return render(request, 'quiz/createquestion.html', ctx)
    return render(request, 'quiz/createquiz.html', ctx)

@login_required
@permission_required('quiz.add_questioncourse', raise_exception=True)
def createQuestions(request, courseOrActivity, courseOrActivity_id, quiz_id, number_questions):

    #----------------------------------ACTIVIDAD O CURSO?------------------------------------
    if(courseOrActivity == COURSE):
        course = get_object_or_404(Course, pk=courseOrActivity_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        isOwner = is_owner(request.user, course.teacher)
    else:
        activity = get_object_or_404(Activity, pk=courseOrActivity_id)
        quiz = get_object_or_404(Quiz, pk=quiz_id)
        isOwner = is_owner(request.user, activity.entity)

    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    #-----------------------------------ELEMENTOS PARA HTML-----------------------------------
    ctx = {
        'isOwner':isOwner,
        'quiz':quiz,
        'courseOrActivity':courseOrActivity,
        'courseOrActivity_id':courseOrActivity_id,
        'number_questions':number_questions
    }

    #-------------------------------------POST FORM-------------------------------------------
    if request.method=="POST":
        new_question_text = request.POST["new_question_text"]
        new_question_score = request.POST["new_question_score"]
        number_answers = request.POST["number_answers"]
        new_question = Question.objects.create(
            text=new_question_text,
            question_score=new_question_score,
            quiz=quiz
        )
        new_question.save()

        ctx['question'] = new_question
        ctx['number_answers'] = int(number_answers)
        ctx['range_number_answers'] = range(int(number_answers))
        return render(request, 'quiz/createanswers.html', ctx)
    
    #-----------------------------------------Default(first time)-------------------------------------
    
    return render(request, 'quiz/createquestion.html', ctx)

@login_required
@permission_required('quiz.add_answercourse', raise_exception=True)
def createAnswers(request, courseOrActivity, courseOrActivity_id, question_id, number_questions, number_answers):
    if(courseOrActivity == COURSE):
        course = get_object_or_404(Course, pk=courseOrActivity_id)
        question = get_object_or_404(Question, pk=question_id)
        isOwner = is_owner(request.user, course.teacher)
    else:
        activity = get_object_or_404(Activity, pk=courseOrActivity_id)
        question = get_object_or_404(Question, pk=question_id)
        isOwner = is_owner(request.user, activity.entity)

    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    #-----------------------------------ELEMENTOS PARA HTML-----------------------------------
    ctx = {
        'isOwner':isOwner,
        'courseOrActivity':courseOrActivity,
        'courseOrActivity_id':courseOrActivity_id,
        'quiz': question.quiz,
        'number_answers': number_answers,
        'constant_activity': ACTIVITY,
        'constant_course': COURSE,
    }

    #----------------------------------------FORM---------------------------------------------
    if request.method=="POST":
        checked_values = request.POST.getlist('new_answer_is_correct[]')
        
        for x in range(number_answers):
            new_answer_text = request.POST["new_answer_text"+str(x)]
            new_answer_is_correct = False
            if str(x) in checked_values:
                new_answer_is_correct = True
            new_answer = Answer.objects.create(
                text=new_answer_text,
                correct=new_answer_is_correct,
                question=question
            )
            new_answer.save()
        
        number_questions = number_questions - 1
        ctx['number_questions'] = number_questions
        return render(request, 'quiz/createquestion.html', ctx)

    return render(request, 'quiz/createanswers.html', ctx)




#---------------------------------------------------HACER TESTS--------------------------------------------------
@login_required
def startQuiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    
    #----------------------------COMPROBACION DE REPETICION DEL TEST----------------------
    exist_finished_qualification = None
    exist_started_qualification = None
    
    list_finished_qualification = Qualification.objects.filter(user=request.user, quiz=quiz, finish=True)
    list_started_qualification = Qualification.objects.filter(user=request.user, quiz=quiz, finish=False)

    if list_finished_qualification:
        exist_finished_qualification = True
    else:
        exist_finished_qualification = False
    
    if list_started_qualification:
        exist_started_qualification = True
    else:
        exist_started_qualification = False
    
    ctx = {
        'quiz':quiz,
        'exist_finished_qualification':exist_finished_qualification,
        'exist_started_qualification':exist_started_qualification
    }
    return render(request, 'quiz/startquiz.html', ctx)

@login_required
def doQuiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    #Habria que mirar si el usuario actual pertenece al curso o actividad (CONTROL DE ACCESO)

    #---------------------SELECCION DE UNA PREGUNTA NO REALIZADA ANTERIORMENTE----------------
    try:
        qualification = Qualification.objects.get(user=request.user, quiz=quiz, finish=False)
    except Qualification.DoesNotExist:
        qualification = Qualification.objects.create(
            user=request.user,
            total_score=0,
            quiz=quiz,
            finish=False
        )
        qualification.save()
    

    list_questions_asked = QuestionAsked.objects.values_list('question', flat=True).filter(qualification=qualification)
    if list_questions_asked:
        list_questions = Question.objects.filter(quiz=quiz).exclude(Q(id__in=list_questions_asked)).distinct()
    else:
        list_questions = Question.objects.filter(quiz=quiz)
    
    #---------------------------CONTROL PARA LA FINALIZACION DEL TEST-------------------------
    end_quiz = list_questions.count() == 0
    if end_quiz:
        qualification.finish = True 
        qualification.save()
        return startQuiz(request, quiz.id)
    
    question = list_questions.first() #Escogemos la primera pregunta(En un futuro se podria poner de forma aleatoria por ej)
    answers = Answer.objects.filter(question=question)
    is_last_answer = list_questions.count() <= 1

    #-----------------------------------ELEMENTOS PARA HTML-----------------------------------
    ctx = {
        'quiz':quiz,
        'question':question,
        'possible_answers':answers,
        'is_last_answer':is_last_answer
    }

    return render(request, 'quiz/doquiz.html', ctx)


@login_required
def doQuizQuestionAsked(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    possible_answers = Answer.objects.filter(question=question)
    quiz = question.quiz

    #------------PUNTUACION DE LA PREGUNTA Y ALMACENAMIENTO DE PREGUNTA REALIZADA----------
    if request.method == 'POST':
        checked_values = request.POST.getlist('list_answers[]')
        total_score = 0
        for answer in possible_answers:
            if str(answer.id) in checked_values and answer.correct:
                total_score = total_score + question.question_score
            #QUE HACEMOS CUANDO ESTA MAL LA PREGUNTA?? Restar?? Por ahora no hace nada

        qualification = Qualification.objects.get(user=request.user, quiz=quiz, finish=False)
        #Por si el usuario intenta volver atras(se ignora)
        try:
            question_asked = QuestionAsked.objects.create(
                qualification=qualification,
                question=question
            )
            question_asked.save()
        except:
            return doQuiz(request, quiz.id)
        qualification.total_score = qualification.total_score + total_score
        qualification.save()
        return doQuiz(request, quiz.id)
    else:
        return HttpResponseForbidden()
