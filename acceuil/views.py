from django.shortcuts import render
import requests as REQ
from django.http import JsonResponse,HttpResponse
from .models import fichierIPFS


url_envoie ='http://127.0.0.1:9094/add'
hashBloque = ""

# Create your views here.
def index(request):
    return render(request,'acceuil.html')

def envoie(request):
    if request.method == 'POST':
        fichier=request.FILES.get('file')
        
                
        if fichier:
            ficheDEF = {'file':(fichier.name,fichier)}
            try:
                
                reponse=REQ.post(url_envoie,files=ficheDEF)
                if reponse.status_code==200:
                    ipfs_hash_poche=reponse.json()
                    ipfs_hash = ipfs_hash_poche.get('cid')
                    if fichierIPFS.objects.filter(cid=ipfs_hash).exists():
                        donnees={'success': True,'message':'enregistré avec succès', 'hash_fichier':ipfs_hash} 
                        return JsonResponse(donnees)
                    else:    
                        fichierIPFS.objects.create(nomFichier=fichier.name,cid=ipfs_hash,taillefichier= request.POST.get('taille'))

                    donnees={'success': True,'message':'enregistré avec succès', 'hash_fichier':ipfs_hash} 
                    return JsonResponse(donnees)
                else:
                    donnees={'success': False,'message':'votre fichier n\'a pas été enregistré'}
                    return JsonResponse(donnees)
            except Exception as e:
                donnees={'success': False,'message':'impossible de se connecter au cluster'}
                return JsonResponse(donnees)            
    else:
        return render(request,'acceuil.html')   
    
def recuperer(request):
    global hashBloque
    if request.method == 'POST':
        if fichierIPFS.objects.filter(cid=request.POST.get('hash_passé')).exists():
            hashBloque = request.POST.get('hash_passé')
            resultat=fichierIPFS.objects.get(cid=request.POST.get('hash_passé'))
            nomfic,taillefic=resultat.nomFichier,resultat.taillefichier
            
            donnees={'success': True,'message':'l\'identifiant hash existe','nomfic':nomfic,'taillefic':taillefic}
            return JsonResponse(donnees) 
        else: 
            donnees={'success': False,'message':'l\'identifiant hash n\'existe pas'}
            return JsonResponse(donnees)    
    else:
        donnees={'success': False,'message':'methode invalide'} 
        return JsonResponse(donnees)    
      

def telechargement(request):
     global hashBloque
     nomfiche=fichierIPFS.objects.get(cid=hashBloque)
     nomfichefinal=nomfiche.nomFichier
     url_IPFS = "http://127.0.0.1:5001/api/v0/cat?arg={}".format(hashBloque)
     try:
        fichier= REQ.post(url_IPFS) 
        if fichier.status_code == 200:
            reponse= HttpResponse(fichier.content, content_type='application/octet-stream')
            reponse['Content-Disposition']=f'attachment; filename="{nomfichefinal}"'
            return reponse
        else:
            donnees={'success': False,'message':'impossible de télécharger'} 
            return JsonResponse(donnees)
     except:
        donnees={'success': False,'message':"impossible d'atteindre le serveur"} 
        return JsonResponse(donnees)    
    
