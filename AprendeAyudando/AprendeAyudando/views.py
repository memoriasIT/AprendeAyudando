from django.shortcuts import render

def landingpage(request):
    return render(request, 'landingpage/index.html')