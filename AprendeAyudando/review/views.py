from django.shortcuts import render
from AprendeAyudando.views import account
from django.contrib.auth.models import User, Group

# Session Handling
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group

# Routing
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from AprendeAyudando.views import has_group

#Queries
from django.db.models import Q

from .models import Review


# Create your views here.

@login_required
def create(request, id_enrollable, title_enrollable):
    
    ctx = {
        'enrollable_id': id_enrollable,
        'enrollable_title' : title_enrollable
    }

    if request.method=="POST":
        review = Review.objects.create(
            enrollable_id = id_enrollable,
            user=request.user,
            rating = request.POST["rating"],
            problems = request.POST["problems"],
            improvements = request.POST["improvements"]
        )
        review.save()
        return account(request) 

    return render(request, 'review/create_review.html', ctx)

def list(request, id_enrollable, title_enrollable, activityOrCourse):
    reviews = Review.objects.all().filter(enrollable_id=id_enrollable)
    isActivity = activityOrCourse == 'Activity'
    ctx = {
        'enrollable_id': id_enrollable,
        'enrollable_title' : title_enrollable,
        'reviews' : reviews,
        'isActivity': isActivity,
    }

    return render(request, 'review/list.html', ctx)

def details(request, id_review, title_enrollable):
    review = get_object_or_404(Review, pk=id_review)
    
    ctx = {
        'review' : review,
        'enrollable_title' : title_enrollable,
    }

    return render(request, 'review/details.html', ctx)