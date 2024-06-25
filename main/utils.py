import openai
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from .models import Embedding, Article
from langchain_core.documents import Document

import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def create_vectorstore():
    articles = Article.objects.all()
    documents = [Document(page_content=article.content, metadata={"id": str(article.id)}) for article in articles]
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai.api_key)
    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
    return vectorstore

def update_index(new_documents):
    vectorstore = create_vectorstore()
    new_docs = [Document(page_content=doc["page_content"], metadata=doc["metadata"]) for doc in new_documents]
    vectorstore.add_documents(new_docs)

    
