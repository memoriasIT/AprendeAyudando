from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from courses.models import Course
from activity.models import Activity
from forum.models import Forum, Debate, Message

@login_required
@permission_required('forum.add_forum', raise_exception=True)
def createForum(request, activityCourseFk):
    if request.method=="POST":
        activityCourseType = ' '

        if request.user.has_perm('courses.add_course'):
            activityCourseType = 'Course'
        else:
            activityCourseType = 'Activity'

        new_forum_name=request.POST["new_forum_name"]
        new_forum = Forum.objects.create(title=new_forum_name, author=request.user, activityCourseFk= activityCourseFk, activityCourseType=activityCourseType)
        new_forum.save()

        isAuthor = True

        context = {
        'forum': new_forum,
        'isAuthor': isAuthor,
        }
        return render(request, 'forum/forum.html',context)
    return render(request, 'forum/createForum.html', {'activityCourseFk': activityCourseFk})
    


@login_required
@permission_required('forum.delete_forum', raise_exception=True)
def delete(request, forum_id):

    forum = get_object_or_404(Forum, pk=forum_id)
    print(forum)
    print(request.method)
    isOwner = True
    if forum.activityCourseType == 'Course':
        course = get_object_or_404(Course, pk=forum.activityCourseFk)
        context = {
            'course': course,
            'isOwner': isOwner,
        }
    else:
        activity =get_object_or_404(Activity, pk=forum.activityCourseFk)
        context = {
            'activity': activity,
            'isOwner': isOwner,
        }
    Forum.objects.filter(id=forum_id).delete()
    if forum.activityCourseType == 'Course':
        return render(request, 'courses/curso.html', context)
    else:
        return render(request, 'activity/activity.html', context)


@login_required
def join(request, forum_id): 
    forum = get_object_or_404(Forum, pk=forum_id)
    debatesList = Debate.objects.filter(forum = forum)

    isAuthor = False

    if request.user == forum.author:
        isAuthor = True
    
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
        'isAuthor' : isAuthor
    }

    return render(request, 'forum/forum.html',context)

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
        #---------------------------------------INFO CONTROL-------------------------------------------
    isAuthor = request.user == forum.author
    context = {
        'debate' : debate,
        'initialMessage' : initialMessage,
        'forum' : forum,
        'isAuthor': isAuthor,
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