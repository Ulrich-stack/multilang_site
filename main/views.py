from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Article
from openai import OpenAI
import json
import os
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.utils.translation import gettext as _, get_language
from .vectorstore import global_vectorstore
import openai

# Charger les variables d'environnement
load_dotenv()

client = OpenAI()

def index(request):
    request.session.flush()  # Clear the session to reset the conversation history
    articles = Article.objects.all().order_by('-publication_date')
    context = {
        'articles': articles,
        'LANGUAGE_CODE': get_language(),
    }
    return render(request, 'main/index.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    return render(request, "main/article.html", {"article": article})

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if global_vectorstore is None:
            return JsonResponse({'response': 'VectorStore not available'}, status=500)

        # Retrieve the conversation history from the session, if it exists
        conversation_history = request.session.get('conversation_history', [])

        # Append the new user message to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        # Retrieve relevant documents from the vectorstore
        relevant_docs = global_vectorstore.similarity_search(query=user_message, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Construct the prompt
        prompt = (
            f"You are a helpful assistant. Use the provided context to answer the question as accurately as possible. "
            f"If the context does not contain the information needed, use your own knowledge to provide a helpful and informative answer.\n\n"
            f"Context: {context}\n\n"
            f"Conversation History:\n" + "\n".join([msg["content"] for msg in conversation_history]) + "\n\n"
            f"Question: {user_message}\nAnswer:"
        )

        # Make a request to OpenAI with the updated prompt
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gpt-3.5-turbo",
        )

        bot_response = response.choices[0].message.content

        # Append the bot's response to the conversation history
        conversation_history.append({"role": "assistant", "content": bot_response})

        # Save the updated conversation history back into the session
        request.session['conversation_history'] = conversation_history

        return JsonResponse({'response': bot_response})

    return JsonResponse({'response': 'Invalid request method'}, status=400)
