from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Article
from openai import OpenAI
import json
import os
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.utils.translation import gettext as _

# Charger les variables d'environnement
load_dotenv()

client = OpenAI()

def index(request):
    articles_liste = Article.objects.all()
    return render(request, 'main/index.html', {"articles": articles_liste})

def detail(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    return render(request, "main/detail.html", {"article": article})

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Make a request to OpenAI using the new API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response.choices[0].message.content
        return JsonResponse({'response': bot_response})

    return JsonResponse({'response': 'Invalid request method'}, status=400)
