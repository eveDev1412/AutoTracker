from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import JsonResponse


def Registro_persona(request):
    template = loader.get_template('registro de persona.html')
    return HttpResponse(template.render())

def consulta(request):
    template = loader.get_template('consulta.html')
    return HttpResponse(template.render())

def Datos_de_auto(request):
    template = loader.get_template('Registro Datos de Auto.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())

def monitoreo(request):
    template = loader.get_template('monitoreo.html')
    return HttpResponse(template.render())

def consulta_tracking(request):
    template = loader.get_template('consulta monitoreo.html')
    return HttpResponse(template.render())

def Registros_usuarios(request):
    template = loader.get_template('registros_usuario.html')
    return HttpResponse(template.render())

def Registros_robo(request):
    template = loader.get_template('registro.html')
    return HttpResponse(template.render())
