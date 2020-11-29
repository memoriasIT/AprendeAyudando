from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Forum

@login_required
@permission_required('forum.add_forum', raise_exception=True)
def createForum(request):

    if request.method=="POST":
        new_forum_name=request.POST["new_forum_name"]
        new_forum = Forum.objects.create(title=new_forum_name, teacher=request.user)
        new_forum.save()
        return HttpResponse("Se ha creado el foro: %s" % new_forum_name)
    return render(request, 'createForum.html',{})


# @login_required
# @permission_required('forum.delete_forum', raise_exception=True)
# def deleteForum(request):

    # if request.method=="POST":
    #     new_forum_name=request.POST["new_forum_name"]
    #     new_course = Course.objects.create(title=new_course_name, teacher=request.user)
    #     new_course.save()
    #     return HttpResponse("Se ha creado el curso: %s" % new_course_name)
    # return render(request, 'createForum.html',{})