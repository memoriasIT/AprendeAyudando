from django.shortcuts import render
from django.contrib.auth import get_user_model

# Session Handling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

#Models
from .models import MessagingMessage
from django.contrib.auth.models import User
from django.core.mail import send_mail

@login_required
@permission_required('messaging.view_messagingmessage', raise_exception=True)
def index(request):
    list_received_message = MessagingMessage.objects.filter(user_destination=request.user)
    list_sent_messages = MessagingMessage.objects.filter(user_origin=request.user)

    all_messages = list_received_message | list_sent_messages
    all_messages = all_messages.distinct()
    
    ctx = {
        'list_received_message':list_received_message,
        'list_sent_messages':list_sent_messages,
        'all_messages':all_messages
    }

    return render(request, 'messaging/index.html', ctx)

@login_required
@permission_required('messaging.view_messagingmessage', raise_exception=True)
def doMessage(request):

    ctx = {
        'elements':None,
        'show_email_or_user_error':False
    }

    if request.method == 'POST':
        new_message_to_email_or_username = request.POST["new_message_to_email_or_username"]
        new_message_title = request.POST["new_message_title"]
        new_message_text = request.POST["new_message_text"]
        try:
            if '@' in new_message_to_email_or_username:
                new_user_destination = User.objects.get(email=new_message_to_email_or_username)
                is_email = True
            else:
                new_user_destination = User.objects.get(username=new_message_to_email_or_username)

            mm = MessagingMessage.objects.create(
                title=new_message_title,
                text=new_message_text,
                user_origin=request.user,
                user_destination=new_user_destination
            )
            mm.save()

            subject = '{} - De: {}'.format(mm.title, request.user.username)
            message = '{} te ha mandado el siguiente mensaje:\n\n {}'.format(request.user.username, mm.text)
            email_from = 'infoaprendeayudando@gmail.com'
            email_to = [new_user_destination.email]
            send_mail(subject, message, email_from, email_to, fail_silently=True)

            return index(request)
        except User.DoesNotExist:
            elements = {
                'new_message_to_email_or_username':new_message_to_email_or_username,
                'new_message_title':new_message_title,
                'new_message_text':new_message_text
            }
            ctx['elements'] = elements
            ctx['show_email_or_user_error'] = True
            render(request, 'messaging/domessage.html', ctx)

    return render(request, 'messaging/domessage.html', ctx)

@login_required
@permission_required('messaging.view_messagingmessage', raise_exception=True)
def viewMessage(request, message_id):
    message = get_object_or_404(MessagingMessage, id=message_id)

    #------------------------CONTROL DE ACCESO-------------------
    if not message.user_destination==request.user and not message.user_origin==request.user:
        return HttpResponseForbidden()
    ctx = {
        'message':message
    }
    if request.method == 'POST':
        if not request.user == message.user_origin: 
            ctx['elements'] = {'new_message_to_email_or_username':message.user_origin}
        else:
            ctx['elements'] = {'new_message_to_email_or_username':message.user_destination}
        return render(request, 'messaging/domessage.html', ctx)
    

    return render(request, 'messaging/viewmessage.html', ctx)