from django.db import models

# Create your models here.
class fichierIPFS(models.Model):
    cid=models.CharField(max_length=100)
    datedajout=models.DateTimeField(auto_now_add=True)
    nomFichier=models.CharField(max_length=100)
    taillefichier= models.CharField(max_length=100)
    


