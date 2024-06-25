import uuid
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Article, Embedding
from openai import OpenAI
import json
import os
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.utils.translation import gettext as _ , get_language
from .utils import create_vectorstore, update_index
import openai

# Charger les variables d'environnement
load_dotenv()


client = OpenAI()

def index(request):
    articles = Article.objects.all()  # Assuming you have an Article model
    context = {
        'articles': articles,
        'LANGUAGE_CODE': get_language(),  # Adding the current language code to the context
    }
    return render(request, 'main/index.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, pk = article_id)
    return render(request, "main/detail.html", {"article": article})


@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Créer un document à partir du message de l'utilisateur
        new_document = [{"page_content": user_message, "metadata": {"id": "user_message"}}]
        
        # Mettre à jour l'index avec le nouveau document
        update_index(new_document)
        
        # Récupérer les documents pertinents pour la question
        vectorstore = create_vectorstore()
        relevant_docs = vectorstore.similarity_search(query=user_message, k=3)
        
        # Construire le message pour le modèle
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        prompt = f"Context: {context}\n\nQuestion: {user_message}\nAnswer:"
        
        # Faire une requête à OpenAI
        response = client.chat.completions.create(
            messages=[
                {
                "role": "user",
                "content": prompt
                },
            ],
            model="gpt-3.5-turbo",
        )
        
        bot_response = response.choices[0].message.content
        return JsonResponse({'response': bot_response})

    return JsonResponse({'response': 'Invalid request method'}, status=400)