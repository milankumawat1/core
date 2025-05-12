from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def Recipies(request):
    if request.method == 'POST':
        data=request.POST
        recipie_image=request.FILES.get('recipie_image')

        recipie_name=data.get('recipie_name')
        recipie_description=data.get('recipie_description')
        print(recipie_name, recipie_description)

        Recipie.objects.create(
            recipie_name=recipie_name,
            recipie_description=recipie_description,
            recipie_image=recipie_image
        )
        return redirect('/recipies/')

    queryset=Recipie.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(recipie_name__icontains=request.GET.get('search'))



    
    context={'recipies':queryset}
    return render(request, 'recipies.html', context)

def delete_recipie(request, id):
    queryset=Recipie.objects.get(id=id)
    queryset.delete()
    return redirect('/recipies/')




@login_required(login_url='/login/')
def update_recipie(request, id):
    queryset=Recipie.objects.get(id=id)

    if request.method == 'POST':
        data=request.POST
        recipie_image=request.FILES.get('recipie_image')

        recipie_name=data.get('recipie_name')
        recipie_description=data.get('recipie_description')

        queryset.recipie_name=recipie_name
        queryset.recipie_description=recipie_description

        if recipie_image:
            queryset.recipie_image=recipie_image

        queryset.save()
        return redirect('/recipies/')
        
        
    context={'recipie':queryset}
    return render(request, 'update_recipie.html', context)


def login_page(request):

    if request.method == 'POST':
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user=authenticate(request, username=username, password=password)


        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/recipies/')

        
        
        
        


    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('/login/')



def register_page(request):

    if request.method == 'POST':
        data=request.POST
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        username=data.get('username')
        password=data.get('password')
        

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            
        )
        user.set_password(password)
        user.save()

        messages.success(request, 'Account created successfully')
        return redirect('/login/')

    return render(request, 'register.html')