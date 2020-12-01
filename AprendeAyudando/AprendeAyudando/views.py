# MODELS
from django.contrib.auth.models import User, Group

# SESSION
from .forms import RegisterForm
from django.contrib.auth import login, logout

# ROUTING
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render


def landingpage(request):
    return render(request, 'landingpage/index.html')

def account(request):
    return render(request, 'landingpage/account.html')

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
