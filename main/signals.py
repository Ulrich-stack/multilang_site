from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from .vectorstore import load_vectorstore, create_vectorstore

@receiver(post_save, sender=Article)
def update_vectorstore(sender, instance, created, **kwargs):
    global global_vectorstore
    global_vectorstore = create_vectorstore()
