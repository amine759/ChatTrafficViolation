from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import upsert_input, predict
from django.http import JsonResponse
import ast


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
            upsert_input.delay(message, pred)  #

        prediction = ast.literal_eval(pred)
        
        chat_response = (
            "Cette amende appartient à la classe : "
            + str(prediction[0])
            + "<br>"
            + "Les points à retirer : "
            + str(prediction[-1])
            + "<br>"
            + "Montant à payer en cas de règlement immédiat ou dans les 24 heures suivant l`infraction : "
            + str(prediction[1])
            + "<br>"
            + "Si le règlement est effectué dans les 15 jours suivants : "
            + str(prediction[2])
        )

        res = chat_response

        return JsonResponse({"res": res})


def chat(request):
    return render(request, "polls/chat.html")


def cart(request):
    return render(request, "polls/cart.html")
