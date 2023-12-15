from django.urls import path
from .views import index, envoie, recuperer,telechargement

urlpatterns = [
    path('',index,name="acceuil"),
    path('envoie/',envoie,name="envoie"),
    path('recupere/',recuperer,name="recuperer"),
    path('telechargement/',telechargement,name="telechargement")
 ]