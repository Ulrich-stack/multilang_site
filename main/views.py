import uuid
from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from django.http import JsonResponse
from .models import Article, Embedding
from openai import OpenAI
import openai
import json
import os
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import Document


# Charger les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


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

# Fonction pour mettre à jour l'index avec les nouveaux documents
def update_index(new_documents):
    # Charger les embeddings existants depuis la base de données
    embeddings_data = Embedding.objects.all()
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai.api_key)

    # Convertir les données de la base de données en format FAISS
    documents = [Document(page_content=doc.content, metadata=doc.metadata) for doc in embeddings_data]

    # Ajouter les nouveaux documents
    documents.extend([Document(page_content=doc["content"], metadata=doc["metadata"]) for doc in new_documents])

    # Indexer les documents avec FAISS
    index = FAISS.from_documents(documents, embeddings)

    # Sauvegarder les nouveaux embeddings dans la base de données
    for doc in new_documents:
        vector = index.index.reconstruct(index.index.ntotal - 1)  # Reconstruire le dernier vecteur ajouté
        Embedding.objects.create(
            document_id=doc["metadata"]["id"],
            embedding_vector=vector.tobytes(),
            metadata=doc["metadata"]
        )

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '') # récupère le message de l'utilisateur

        # Ajouter le message de l'utilisateur comme nouveau document
        new_document = [{"content": user_message, "metadata": {"id": str(uuid.uuid4()), "type": "user_message"}}]
        update_index(new_document)


        response = client.chat.completions.create( # fait une réquête à OpenAI
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response.choices[0].message.content
        
                # Ajouter la réponse du bot comme nouveau document
        bot_document = [{"content": bot_response, "metadata": {"id": str(uuid.uuid4()), "type": "bot_response"}}]
        update_index(bot_document)
        
        return JsonResponse({'response': bot_response})

    return JsonResponse({'response': 'Invalid request method'}, status=400)
