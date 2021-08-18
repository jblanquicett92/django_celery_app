from django.shortcuts import render
from django.http import HttpResponse

def uuid(request):
    
    return render(request, 'index.html')