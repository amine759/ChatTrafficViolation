from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import upsert_input, predict, chain
from django.http import JsonResponse
import ast
from .models import Amendes


def write_to_db(classe, category):
    Amendes.objects.create(classe=classe, category=category)


@csrf_exempt
def index(request):
    return render(request, "polls/index.html")


def about(request):
    return render(request, "polls/about.html")


def chatbot(request):
    if request.method == "POST":
        message = request.POST["question"]
        pred, valid, embeddings, sentiment = predict(message)

        if valid:
            # upsert_input(pred, embeddings)  let's not upsert to pinecone right now

            prediction = ast.literal_eval(pred)

            chat_response = chain(prediction, sentiment)
            write_to_db(message, prediction)

            return JsonResponse({"res": chat_response})
        else:
            return JsonResponse({"res": pred})


def write_to_db(classe, category):
    Amendes.objects.create(classe=classe, category=category)


def chat(request):
    return render(request, "polls/chat.html")


def cart(request):
    return render(request, "polls/cart.html")
