from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from courses.models import Course
from activity.models import Activity
from activity.views import join as viewsActivityJoin
from courses.views import join as viewsCourseJoin
from forum.models import Forum, Debate, Message, Reply
from AprendeAyudando.templatetags.auth_extras import COURSE, ACTIVITY
from django.http import HttpResponseForbidden

#-----------------------------------------FOROS------------------------------------------

@login_required
@permission_required('forum.add_forum', raise_exception=True)
def createForum(request, courseOrActivity, activityCourseFk):
    
    #------------------------CONTROL DE ACCESO-------------------
    if courseOrActivity == COURSE:
        course = get_object_or_404(Course, id=activityCourseFk)
        isOwner = course.teacher == request.user
    else:
        activity = get_object_or_404(Activity, id=activityCourseFk)
        isOwner = activity.entity == request.user
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()

    #---------------------------FORM POST----------------------
    if request.method=="POST":

    if request.method=="POST":
        new_forum_name=request.POST["new_forum_name"]
        new_forum = Forum.objects.create(
            title=new_forum_name,
            author=request.user,
            activityCourseFk=activityCourseFk,
            activityCourseType=courseOrActivity
        )
        new_forum.save()
        return join(request, new_forum.id)
    
    ctx = {
        'activityCourseFk': activityCourseFk,
        'courseOrActivity': courseOrActivity
    }
    return render(request, 'forum/createForum.html', ctx)
    


@login_required
@permission_required('forum.delete_forum', raise_exception=True)
def delete(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)

    #------------------------CONTROL DE ACCESO-------------------
    if forum.activityCourseType == COURSE:
        course = get_object_or_404(Course, id=forum.activityCourseFk)
        isOwner = course.teacher == request.user
    else:
        activity = get_object_or_404(Activity, id=forum.activityCourseFk)
        isOwner = activity.entity == request.user
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()

    #------------------------ELIMINACION------------------------
    activity_or_course_id = forum.activityCourseFk
    Forum.objects.filter(id=forum_id).delete()
    if forum.activityCourseType == COURSE:
        return viewsCourseJoin(request, activity_or_course_id)
    else:
        return viewsActivityJoin(request, activity_or_course_id)

@login_required
def join(request, forum_id): 
    forum = get_object_or_404(Forum, pk=forum_id)
    debatesList = Debate.objects.filter(forum = forum)

    isAuthor = request.user == forum.author
    
    isCourse = forum.activityCourseType == COURSE
    
    success = False
    # If the current logged user isn't enrolled in the course then add him
    if request.user not in forum.enrolled_users.all() and request.user != forum.author:
        forum.enrolled_users.add(request.user)
        success = True

    context = {
        'usuario': request.user,
        'forum': forum,
        'success': success,
        'debatesList': debatesList,
        'isAuthor' : isAuthor,
        'isCourse': isCourse
    }

    return render(request, 'forum/forum.html',context)


#-----------------------------------------DEBATES------------------------------------------
@login_required
def createDebate(request, forum_id):
    forum = get_object_or_404(Forum, pk=forum_id)
    if request.method=="POST":

        #Obtenemos el contenido del mensaje inicial
        initial_message_subject=request.POST["initial_message_subject"]
        initial_message_content=request.POST["initial_message_content"]

        #Creamos el debate
        new_debate = Debate.objects.create(title = initial_message_subject, author=request.user, forum = forum)
        new_debate.save()
        new_debate_id = new_debate.id
        #Creamos el mensaje inicial
        initial_message = Message.objects.create(author=request.user, subject = initial_message_subject, 
            content=initial_message_content, debate = new_debate, initial=True)
        initial_message.save()

        return viewDebate(request, new_debate_id)
    return render(request, 'forum/createDebate.html', {'forum': forum})
    
@login_required
def viewDebate(request, debate_id):
    debate = get_object_or_404(Debate, pk=debate_id)
    forum = debate.forum
        #-----------------------------------------MENSAJES-------------------------------------------
    initialMessage = Message.objects.filter(debate = debate, initial = True).first()
    replies = Reply.objects.filter(originalMessage=initialMessage)
    repliesList = []
    for r in replies:
        repliesList.append(r.replyMessage)
    
        #---------------------------------------INFO CONTROL-------------------------------------------
    isAuthor = request.user == forum.author
    context = {
        'debate' : debate,
        'initialMessage' : initialMessage,
        'forum' : forum,
        'isAuthor': isAuthor,
        'repliesList': repliesList,
    }
    return render(request, 'forum/debate.html', context)

@login_required
def deleteDebate(request, debate_id):

    debate = get_object_or_404(Debate, pk=debate_id)
    forum = debate.forum
    print(debate)
    print(request.method)
    Debate.objects.filter(id=debate_id).delete()
    
    return join(request, forum.id)

#-----------------------------------------MENSAJES------------------------------------------
def reply(request, message_id):
    originalMessage = get_object_or_404(Message, pk=message_id)
    if request.method=="POST":

        #Obtenemos el contenido de la respuesta
        message_subject=request.POST["message_subject"]
        message_content=request.POST["message_content"]

        #Creamos el mensaje
        replyMessage = Message.objects.create(author=request.user, subject = message_subject, 
            content=message_content, debate = originalMessage.debate, initial=False)
        replyMessage.save()

        reply = Reply.objects.create(originalMessage=originalMessage, replyMessage = replyMessage)
        reply.save()

        return viewDebate(request, originalMessage.debate.id)
    return render(request, 'forum/reply.html', {'originalMessage': originalMessage})