from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.shortcuts import render
from courses.models import Course
from activity.models import Activity
from resources.models import Resource
from AprendeAyudando.templatetags.auth_extras import COURSE, ACTIVITY
from activity.views import join as viewsActivityJoin
from courses.views import join as viewsCourseJoin
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, Group

from django.core.files.storage import FileSystemStorage

# Notifications
from django.core.mail import send_mail
from messaging.models import MessagingMessage

# Calendar
import datetime
from schedule.models import Calendar
from django.utils.dateparse import parse_date
from schedule.models import Event


@login_required
@permission_required('resources.add_resource', raise_exception=True)
def createResource(request, courseOrActivity, activityCourseFk):

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
        new_resource_name=request.POST["new_resource_name"]

        try:
            if request.POST["isLocalFile"] == 'on':
                isLocalFile = True
            else:
                isLocalFile = False
        except:
            isLocalFile = False


        new_resource_link=request.POST.get("new_resource_link", "")

        try:
            file = request.FILES['file']
            fs = FileSystemStorage()
            fs.save(file.name, file)
        except:
            file = None


        try:
            if request.POST["isShownInCalendar"] == 'on':
                isShownInCalendar = True
            else:
                isShownInCalendar = False
        except:
            isShownInCalendar = False

        if isShownInCalendar:
            date_str = request.POST.get('dateInCalendar', None)
            dateInCalendar = parse_date(date_str)
        else:
            dateInCalendar = datetime.datetime.now()

        if not new_resource_link.startswith('http://') and not new_resource_link.startswith('https://'):
            new_resource_link='http://'+new_resource_link
        new_resource = Resource.objects.create(
            activityCourseFk= activityCourseFk,
            activityCourseType=courseOrActivity,
            resourceText = new_resource_name,
            isLocalFile = isLocalFile,
            resourceLink = new_resource_link,
            file = file,
            isShownInCalendar = isShownInCalendar,
            dateInCalendar = dateInCalendar
        )
        new_resource.save()

        type = new_resource.activityCourseType
        enrollable = get_object_or_404(Course, pk=new_resource.activityCourseFk) if type == COURSE else get_object_or_404(Activity, pk=new_resource.activityCourseFk)
        # teacher = enrollable.teacher if type == COURSE else enrollable.entity
        for user in enrollable.enrolled_users.all():
            subject = '[{}] Nuevo recurso: {}'.format(enrollable.title, new_resource.resourceText)
            message = '{}: \"{}\" ha añadido un nuevo recurso a \"{}\"\n\n{}: {}'.format('El profesor' if type == COURSE else 'La entidad', request.user.username, enrollable.title, new_resource.resourceText, new_resource.resourceLink)
            email_from = 'infoaprendeayudando@gmail.com'
            email_to = [user.email]
            send_mail(subject, message, email_from, email_to, fail_silently=True)
            
            mm = MessagingMessage.objects.create(
                title=subject,
                text=message,
                user_origin=User.objects.get(email=email_from),
                user_destination=user
            )
            mm.save()
    
        if isShownInCalendar:
            createEventInCalendar(new_resource_name, dateInCalendar, courseOrActivity)

        if(courseOrActivity == COURSE):
            return viewsCourseJoin(request, activityCourseFk)
        else:
            return viewsActivityJoin(request, activityCourseFk)
    
    ctx = {
        'activityCourseFk': activityCourseFk,
        'courseOrActivity': courseOrActivity
    }
    return render(request, 'resource/createResource.html', ctx)


def createEventInCalendar(title, date, courseOrActivity):
    if(courseOrActivity == COURSE):
        calendar = Calendar.objects.get(pk=3)
    else:
        calendar = Calendar.objects.get(pk=1)

    try:
        data = {
            'title': title,
            'start': date,
            'end': date,
            'calendar': calendar,
            'color_event': '#a7afb2'
        }
        event = Event(**data)
        event.save()
    except:
        print('Event was not created for '+ title)
        pass


@login_required
@permission_required('resources.delete_resource', raise_exception=True)
def delete(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    #------------------------CONTROL DE ACCESO-------------------
    if resource.activityCourseType == COURSE:
        course = get_object_or_404(Course, id=resource.activityCourseFk)
        isOwner = course.teacher == request.user
    else:
        activity = get_object_or_404(Activity, id=resource.activityCourseFk)
        isOwner = activity.entity == request.user
    if not isOwner and not request.user.is_superuser:
        return HttpResponseForbidden()

    #------------------------ELIMINACION------------------------
    
    activity_or_course_id = resource.activityCourseFk
    Resource.objects.filter(id=resource_id).delete()

    if resource.activityCourseType == COURSE:
        return viewsCourseJoin(request, activity_or_course_id)
    else:
        return viewsActivityJoin(request, activity_or_course_id)
