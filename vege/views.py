from django.shortcuts import render, redirect
from .models import *
# Create your views here.
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
