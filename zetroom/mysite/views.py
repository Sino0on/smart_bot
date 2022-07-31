import requests
from django.shortcuts import render, redirect
from server.models import *
from server.forms import FeedbackForm

url = "https://api.telegram.org/bot5346235377:AAGg1mWc4FPRxGn1GFcnOBcj75MMLlrAJlA/sendMessage"


def index(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            payload = {
                "text": f"{form}",
                "chat_id": '-1001519795077',
            }

            response = requests.post(url, json=payload)
            form.save()
            return redirect('/')
    return render(request, 'index.html', {'questions': questions, 'form': FeedbackForm})
