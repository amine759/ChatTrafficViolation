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
        request.session["user_inputs"] = message
        print(message)

        pred, valid = predict(message)
        request.session["predictions"] = pred
        request.session["valid"] = valid

        print(pred)
        res = pred.replace("\n", "<br>")
        return JsonResponse({"res": res})


def batch_user_input(request):
    # Initialize an empty list to store user inputs in the session
    if "user_inputs" not in request.session:
        request.session["user_inputs"] = []
    if "predictions" not in request.session:
        request.session["predictions"] = []

    # Retrieve user input from the request
    user_input = request.session.get(
        "question"
    )  # Assuming user input is sent via POST request
    prediction, valid = request.session.get("predictions"), request.session.get("valid")
    if valid:
        # Append the user input to the list of user inputs in the session
        request.session["user_inputs"].append(user_input)
        request.session["predictions"].append(prediction)

    # Optionally, you can save the session to persist the changes immediately
    request.session.save()


def close_session_and_upsert(request):
    # Retrieve accumulated user inputs from the session
    user_inputs = request.session.pop("user_inputs", [])
    predictions = request.session.pop("predictions", [])

    upsert_batch_input(user_inputs, predictions)
    index_info = pc.info_index(index)
    # Extract the number of records (vectors) from the index info
    print(index_info["stats"]["n"])
    request.session.save()


def logout(request):
    # Delete session data
    try:
        del request.session["user_inputs"]
        del request.session["preedictions"]
        del request.session["valid"]
    except KeyError:
        pass


def chat(request):
    return render(request, "polls/chat.html")


def cart(request):
    return render(request, "polls/cart.html")
