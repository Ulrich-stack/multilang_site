from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from .vectorstore import load_vectorstore, create_vectorstore

#à chaque fois qu'un nouvel article est ajouté à la base de donnée on recrée les vecteurs
#pour que les données exploitées par le chatbot soient à jour
@receiver(post_save, sender=Article)
def update_vectorstore(sender, instance, created, **kwargs):
    global global_vectorstore
    global_vectorstore = create_vectorstore()
