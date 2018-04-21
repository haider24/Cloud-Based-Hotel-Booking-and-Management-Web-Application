from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('homepage.html')

    # rendering the template in HttpResponse
    # context = {
    #     'name': 'Belal Khan',
    #     'fname': 'Azad Khan',
    #     'course': 'Python Django Framework',
    #     'address': 'Kanke, Ranchi, India',
    # }

    # rendering the template in HttpResponse
    # but this time passing the context and request
    return HttpResponse(template.render())
# Create your views here.

def loginpage(request):
    template=loader.get_template('login.html')
    return HttpResponse(template.render())