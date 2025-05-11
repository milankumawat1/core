from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    people = [
        {'name': 'John', 'age': 20},
        {'name': 'Jane', 'age': 21},
        {'name': 'Jim', 'age': 22},
    ] 
    vegetables = ['tomato', 'potato']

    return render(request, 'index.html',context={'page':'Home', 'people':people, 'vegetables':vegetables})


def about(request):
    context = {
        'page': 'About'
    }
    return render(request, 'about.html', context)

def contact(request):
    context = {
        'page': 'Contact'
    }
    return render(request, 'contact.html', context)


