from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from .models import Article
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Variable globale pour stocker le vectorstore
global_vectorstore = None

def create_vectorstore():
    articles = Article.objects.all()
    documents = [Document(page_content=article.content, metadata={"id": str(article.id)}) for article in articles]
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai.api_key)
    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
    return vectorstore

def load_vectorstore():
    global global_vectorstore
    if global_vectorstore is None:
        global_vectorstore = create_vectorstore()
    return global_vectorstore

# Charger le vectorstore au démarrage de l'application
load_vectorstore()
