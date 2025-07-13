from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



@login_required
def home_view(request):
    return render(request, "home.html")