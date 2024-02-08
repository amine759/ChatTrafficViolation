from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import *
from django.http import JsonResponse


@csrf_exempt
def index(request):
    return render(request, "polls/index.html")


def about(request):
    return render(request, "polls/about.html")


def chatbot(request):
    if request.method == "POST":
        message = request.POST["question"]
        pred, valid = predict(message)
        if valid:
            upsert_input(message,pred)

        res = pred.replace("\n", "<br>")
        return JsonResponse({"res": res})


def chat(request):
    return render(request, "polls/chat.html")


def cart(request):
    return render(request, "polls/cart.html")
