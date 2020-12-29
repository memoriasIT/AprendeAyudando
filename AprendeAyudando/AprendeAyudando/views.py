from django.shortcuts import render

from django.contrib.auth.models import User, Group
<<<<<<< HEAD
from django.http import HttpResponseRedirect
=======
from django.http import HttpResponseRedirect, HttpResponseForbidden
>>>>>>> 30ce8cfe202543276c2b6a2d65893274fcff5a7a
from .forms import RegisterForm, RecoverForm, UploadForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
import random
import string

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def landingpage(request):
    grupo = 'Invitado'
    if request.user.has_perm('courses.view_course'):
        grupo = 'Estudiante'
    if request.user.has_perm('courses.add_course'):
        grupo = 'Profesor'
    if request.user.has_perm('activity.add_activity'):
        grupo = 'Entidad'

    context = {
        'grupo': grupo
    }
    return render(request, 'landingpage/index.html', context)

def news(request):
    return render(request, 'news/index.html')

@login_required
def account(request):
    return render(request, 'landingpage/account.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        if "cancel" in request.POST:
            return redirect('/account')
        else:
            request.user.delete()
            return redirect('/')

    return render(request, 'landingpage/delete_account.html')
    
def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'registration/register.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.save()
               
                # Add role student to new user
                studentGroup = Group.objects.get(name='Estudiante')
                studentGroup.user_set.add(user)

                # Login the user
                login(request, user)
               
                # redirect to accounts page:
                return HttpResponseRedirect(reverse('account'))

   # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

    return render(request, template, {'form': form})

def recoverpassword(request):
    # if this is a POST request we need to process the form data
    template = 'registration/recoverpassword.html'
   
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        miForm = RecoverForm(request.POST)
        # check whether it's valid:
        if miForm.is_valid():
            if User.objects.filter(email=miForm.cleaned_data['email']).exists():
                # Minuto 19:19
                infForm=miForm.cleaned_data

                size = 12
                chars = string.ascii_uppercase+string.ascii_lowercase+string.digits

                newPass = ''.join(random.choice(chars) for x in range(size))
                subject = 'Solicitud de nueva contraseña'
                message = 'Ha solicitado una nueva contraseña en la plataforma AprendeAyudando. Su nueva contraseña es: %s.' %newPass
                email_from = settings.EMAIL_HOST_USER 
                email_to = [infForm['email']]
                
                user = User.objects.get(email=infForm['email'])
                user.set_password(newPass)
                user.save()
                
                send_mail(subject, message, email_from, email_to)

                
                return render(request, template, {
                    'form': miForm,
                    'error_message': 'The new password has been sent to your email'
                })
            else:
                return render(request, template, {
                    'form': miForm,
                    'error_message': 'Try again. Email does not exists.'
                })
            

   # No post data availabe, let's just show the page.
    else:
        miForm = RecoverForm()

    return render(request, template, {'form': miForm})

@login_required
def modify(request, username):
    template = 'registration/modify.html'
    user = User.objects.get(username=username)
<<<<<<< HEAD
=======
    if not request.user == user:
        return HttpResponseForbidden()
>>>>>>> 30ce8cfe202543276c2b6a2d65893274fcff5a7a
    modForm = UploadForm(instance=user)
    return render(request, template, {'form': modForm, 'username':username})

@login_required
def update(request, username):
    template = 'registration/modify.html'
    user = User.objects.get(username=username)
    userEmail = user.email
    modForm = UploadForm(request.POST, instance=user)
    if request.method == 'POST':
        if modForm.is_valid():

            infForm=modForm.cleaned_data
            email = infForm['email']
            password = infForm['password']
            confpassword = infForm['password_repeat']
            firstName = infForm['first_name']
            lastName = infForm['last_name']

            if User.objects.filter(email=email).exists() and userEmail != email:
                    return render(request, template, {
                        'form': modForm,
                        'error_message': 'Email already exists.'
                    })
            elif password != confpassword:
                    return render(request, template, {
                        'form': modForm,
                        'error_message': 'Passwords do not match.'
                    })
            else:
                
                user.email = email
                user.first_name = firstName
                user.last_name = lastName
                
                if password != "":
                    user.set_password(password)
                    user.save()

                    subject = 'Cambio de contraseña'
                    message = 'Buenas %s %s.\nEn su cuenta de la plataforma AprendeAyudando la contraseña ha sido modificada.\nSi usted no ha cambiado la contraseña pulse sobre el siguiente enlace para recuperarla\n\nhttp://127.0.0.1:8000/recoverpassword/\n\nMuchas gracias.\nUn saludo.' %(user.first_name, user.last_name)
                    email_from = settings.EMAIL_HOST_USER 
                    email_to = [infForm['email']]
                
                    send_mail(subject, message, email_from, email_to)

                else:
                    user.save()

                # Login the user
                login(request, user)

                return HttpResponseRedirect(reverse('account'))
    else:
        modForm = UploadForm(request.POST, instance=user)

    return render(request, template, {'form': modForm, 'username':username})
            
        