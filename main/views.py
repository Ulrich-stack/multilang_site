from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Article
from openai import OpenAI
import json
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.utils.translation import gettext as _, get_language
from .vectorstore import global_vectorstore

# Charger les variables d'environnement
load_dotenv()

client = OpenAI()

def index(request):
    # Réinitialiser la session pour réinitialiser l'historique des conversations
    request.session.flush()  
    articles = Article.objects.all().order_by('-publication_date')
    context = {
        'articles': articles,
        'LANGUAGE_CODE': get_language(),
    }
    return render(request, 'main/index.html', context)

def detail(request, article_id):
    # Récupérer un article spécifique par son identifiant
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
        'LANGUAGE_CODE': get_language(),
    }
    return render(request, "main/article.html", context)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        # Charger les données de la requête POST
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if global_vectorstore is None:
            return JsonResponse({'response': 'VectorStore non disponible'}, status=500)

        # Récupérer l'historique des conversations de la session, si elle existe
        conversation_history = request.session.get('conversation_history', [])

        # Ajouter le nouveau message de l'utilisateur à l'historique des conversations
        conversation_history.append({"role": "user", "content": user_message})

        # Récupérer les documents pertinents du vectorstore
        relevant_docs = global_vectorstore.similarity_search(query=user_message, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Construire l'invite
        prompt = (
            f"Vous êtes un assistant utile. Utilisez le contexte fourni pour répondre à la question aussi précisément que possible. "
            f"Si le contexte ne contient pas les informations nécessaires, utilisez vos propres connaissances pour fournir une réponse utile et informative.\n\n"
            f"Contexte: {context}\n\n"
            f"Historique des conversations:\n" + "\n".join([msg["content"] for msg in conversation_history]) + "\n\n"
            f"Question: {user_message}\nRéponse:"
        )

        # Faire une requête à OpenAI avec l'invite mise à jour
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
        )

        bot_response = response.choices[0].message.content

        # Ajouter la réponse du bot à l'historique des conversations
        conversation_history.append({"role": "assistant", "content": bot_response})

        # Enregistrer l'historique des conversations mis à jour dans la session
        request.session['conversation_history'] = conversation_history

        return JsonResponse({'response': bot_response})

    return JsonResponse({'response': 'Méthode de requête non valide'}, status=400)
