from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Embedding(models.Model):
    document_id = models.CharField(max_length=255, unique=True)
    embedding_vector = models.BinaryField()
    metadata = models.JSONField()