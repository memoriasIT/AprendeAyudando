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
from quiz.models import Quiz, QuizCourse, QuestionCourse, AnswerCourse

@login_required
@permission_required('quiz.add_quizcourse', raise_exception=True)
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
    if request.method=="POST" and (isOwner or request.user.is_superuser):
        new_quiz_title = request.POST["new_quiz_title"]
        new_quiz_description = request.POST["new_quiz_description"]
        new_quiz_is_repeatable = request.POST["is_repeatable"]=='si'
        new_quiz_show_qualification = request.POST["show_qualification"]=='si'
        number_questions = request.POST["number_questions"]
        new_quiz = QuizCourse.objects.create(
            title=new_quiz_title,
            description=new_quiz_description,
            repeatable=new_quiz_is_repeatable,
            show_qualification=new_quiz_show_qualification,
            course=course
        )
        new_quiz.save()

        ctx['quiz'] = new_quiz
        ctx['number_questions'] = int(number_questions)
        return render(request, 'quiz/createquestion.html', ctx)
    return render(request, 'quiz/createquiz.html', ctx)

@login_required
@permission_required('quiz.add_questioncourse', raise_exception=True)
def createQuestionsCourse(request, course_id, quiz_course_id, number_questions):
    course = get_object_or_404(Course, pk=course_id)
    quiz = get_object_or_404(QuizCourse, pk=quiz_course_id)

    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    isOwner = False
    if is_owner(request.user, course.teacher):
        isOwner = True
    
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    #-----------------------------------ELEMENTOS PARA HTML-----------------------------------
    ctx = {
        'is_course':True,
        'isOwner':isOwner,
        'course': course,
        'quiz': quiz,
        'number_questions': number_questions,
    }

    #-------------------------------------POST FORM-------------------------------------------
    if request.method=="POST":
        new_question_text = request.POST["new_question_text"]
        new_question_score = request.POST["new_question_score"]
        number_answers = request.POST["number_answers"]
        new_question = QuestionCourse.objects.create(
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
def createAnswersCourse(request, course_id, question_course_id, number_questions, number_answers):
    course = get_object_or_404(Course, pk=course_id)
    question = get_object_or_404(QuestionCourse, pk=question_course_id)

    #-----------------------------------CONTROL DE ACCESO-----------------------------------
    isOwner = False
    if is_owner(request.user, course.teacher):
        isOwner = True
    
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    #-----------------------------------ELEMENTOS PARA HTML-----------------------------------
    ctx = {
        'is_course':True,
        'isOwner':isOwner,
        'course': course,
        'quiz': question.quiz,
        'number_answers': number_answers,
    }

    #----------------------------------------FORM---------------------------------------------
    if request.method=="POST":
        checked_values = request.POST.getlist('new_answer_is_correct[]')
        
        for x in range(number_answers):
            new_answer_text = request.POST["new_answer_text"+str(x)]
            new_answer_is_correct = False
            if str(x) in checked_values:
                new_answer_is_correct = True
            new_answer = AnswerCourse.objects.create(
                text=new_answer_text,
                correct=new_answer_is_correct,
                question=question
            )
            new_answer.save()
        
        number_questions = number_questions - 1
        ctx['number_questions'] = number_questions
        return render(request, 'quiz/createquestion.html', ctx)

    return render(request, 'quiz/createanswers.html', ctx)

    