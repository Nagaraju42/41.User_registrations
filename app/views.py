from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
from app.forms import *


def Registration(request):
    d={'ufo':UserForm(), 'pfo':ProfileForm()}
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            #password=ufd.cleaned_data('password')
            #NSUO=set_password(password)
            NSUO.set_password(ufd.cleaned_data['password'])
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()

           

            return HttpResponse('registration successfully')

        else:
            return HttpResponse('not valid')                    


    return render(request,'registration.html',d)

def home(request):
    if request.method=='POST':
        username=request.session.get(username)
        d={'username':username}
        return render(request,'Home_page.html',d)
    return render(request,'Home_page.html')


def userlogin(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username/Password')
    return render(request,'login.html')

@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    un=request.session['username']
    print(un)
    uno=User.objects.get(username=un)
    po=Profile.objects.get(username=uno)
    d={'uno':uno,'po':po}
    return render(request,'display_profile.html',d)