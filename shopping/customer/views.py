from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Customer



def mainpage(request):
    '''
    For logging users in
    '''
    if request.method == "POST":
        type = request.POST.get('type')
        if type=="login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request,username=username,password=password)  #django default authentication
            if user is not None:
                login(request,user)
                return redirect('customerhomepage')
            else: 
                messages.error(request,"Wrong Credentials! Please Try again")
        elif type=="register":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:   #creating Customer object
                user=User.objects.create_user(username=username,password=password,email=email)
                user.save()
                messages.success(request," Signup successfull ")
                return redirect('customerhomepage')
            except:
                messages.error(request," Error occured. Please Try again!")
                return redirect('loginpage')
    return render(request, 'login.html')   


def dashboard(request):
    return render(request, 'index.html')   
