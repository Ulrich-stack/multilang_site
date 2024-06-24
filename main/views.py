from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
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
    articles = Article.objects.all() # pour récupérer les articles de ma base de données
    context = {
        'articles': articles,
        'LANGUAGE_CODE': get_language(), # pour récupérer le language actuel et le passer en contexte
    }
    return render(request, 'main/index.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    return render(request, "main/detail.html", {"article": article})

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '') # récupère le message de l'utilisateur

        response = client.chat.completions.create( # fait une réquête à OpenAI
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response.choices[0].message.content
        return JsonResponse({'response': bot_response})

    return JsonResponse({'response': 'Invalid request method'}, status=400)
