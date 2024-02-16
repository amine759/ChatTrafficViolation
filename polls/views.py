from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import upsert_input, predict, chain
from django.http import JsonResponse
import ast
from .models import Amendes

@csrf_exempt
def index(request):
    return render(request, "polls/index.html")


def about(request):
    return render(request, "polls/about.html")


def chatbot(request):
    if request.method == "POST":
        message = request.POST["question"]
        pred, valid, embeddings = predict(message)

        if valid:
            upsert_input.delay(pred, embeddings)  #

            prediction = ast.literal_eval(pred)

            chat_response = chain(prediction)
            
            write_to_db(message,prediction)

            return JsonResponse({"res": chat_response})
        else :
            return JsonResponse({"res": pred})

def write_to_db(amende, category):
    obj = Amendes(amende=amende,category=category)
    obj.save()
    Amendes.objects.create(amende=amende, category=category)

def chat(request):
    return render(request, "polls/chat.html")


def cart(request):
    return render(request, "polls/cart.html")
