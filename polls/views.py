from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from keras.models import load_model
from .chatbot import *
from django.http import JsonResponse
@csrf_exempt

def index(request):
    return render(request, 'polls/index.html')

def about(request):
    return render(request, 'polls/about.html')

def chatbot(request):
    
    if request.method=='POST':

        return JsonResponse({'res':'hello'})

def chat(request):
    return render(request, 'polls/chat.html')
    

def cart(request):
    return render(request, 'polls/cart.html')