# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 14:12:19 2020

@author: TR
"""

import subprocess
from sp import *

donnees=('Graphe1', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
         [('A', 'A', 2), ('A', 'B', 5), ('A', 'C', 8), ('B', 'C', 6),
          ('B', 'D', 8), ('B', 'E', 6), ('C', 'B', 2), ('C', 'D', 1),
          ('C', 'E', 2), ('D', 'E', 3), ('D', 'F', 1), ('E', 'A', 5),
          ('E', 'D', 1), ('E', 'G', 5), ('F', 'D', 4), ('F', 'E', 1),
          ('F', 'G', 3), ('F', 'H', 6), ('E', 'I', 3), ('G', 'H', 2),
          ('H', 'B', 6), ('H', 'B', 7), ('I', 'J', 4), ('J', 'I', 5)])


 
class Graphe() :
    def __init__(self , nom , Liste_Sommets ,Liste_Arcs  ) :
        self.nom=nom  
        self.Liste_Sommets= []  #stock les sommets du graphe
        self.Liste_Arcs= []     #stock les arcs du graphe sous la forme d'un tuple
        self.Dictionnaire_objet_nom={} #dictionnaire qui fais correspondre le nom de la variable à l'objet(clé=nom; valeur=objet)



    def __repr__(self) :
        return '({},{},{})'.format(self.nom,self.Liste_Sommets,self.Liste_Arcs)

  

#création des sommets, des arcs et des voisins 
    def Liste_creation(self,liste_arc,liste_sommet): 
        for elt_som in liste_sommet:
            a=Sommet(elt_som)
            self.Liste_Sommets.append(a)   #remplissage de la listes des sommets
        for i in range(len(self.Liste_Sommets)):
            self.Dictionnaire_objet_nom[donnees[1][i]] = self.Liste_Sommets[i]  #remplissage du dictionnaire faisant correspondre le nom du sommet et l'objet associé
        for elt_arc in liste_arc:
                self.Liste_Arcs.append(Arc(elt_arc[0],elt_arc[1],elt_arc[2]))  #remplissage de la liste des arcs 
        for elt_som in self.Dictionnaire_objet_nom.keys(): #création des voisins d'un sommet sous la forme d'une liste de tuples contenant le sommet d'arrivé et le poids de l'arc correspondant
            for elt_arc in self.Liste_Arcs:
                if elt_som==elt_arc.depart: #true si on prends comme départ le sommet dont on veut connaitre les voisins
                    self.Dictionnaire_objet_nom[elt_som].voisins.append((elt_arc.arrive,elt_arc.poids)) 
            for i in range(len(self.Dictionnaire_objet_nom[elt_som].voisins)): #enlever les doublon des arcs avec un poids supérieur pour régler de potentiel futur problème
                for j in range(len(self.Dictionnaire_objet_nom[elt_som].voisins)):
                    if i!=j:
                        if self.Dictionnaire_objet_nom[elt_som].voisins[i][0]==self.Dictionnaire_objet_nom[elt_som].voisins[j][0]: #si même arrivé alors:
                            if self.Dictionnaire_objet_nom[elt_som].voisins[i][1]>self.Dictionnaire_objet_nom[elt_som].voisins[j][1]: #si un poids plus grand alors:
                                    self.Dictionnaire_objet_nom[elt_som].voisins.pop(i) #enleve l'arc avec le poids le plus grand (pas besoin d'un else comme j'itère sur i et j indiférrament)


#créer le tableau dans le shell
    def Tableau_Shell(self,resultat_Djikistra):
        for i in range(len(self.Liste_Sommets)):  #formatage de la liste des resultats pour avoir un beau tableau(je rajoute des tirets sur les valeurs non définies)
            for elt in self.Liste_Sommets:
                if elt not in list(resultat_Djikistra[i].keys()): #resultat_Djikistra[i].keys() n'est pas subscriptable donc je la transforme en list
                    resultat_Djikistra[i][elt]= '-'
        Tableau= '|   |'
        for i in range(len(resultat_Djikistra)):
            Tableau+=' {:^3} |' .format(str(self.Liste_Sommets[i]))  #str car le {:^3} n'est pas reconnu par ma classe Sommet           
        for i in range(len(resultat_Djikistra)):
            Tableau+='\n| {} |'.format(self.Liste_Sommets[i])
            for j in range(len(self.Liste_Sommets)):
                if i==j: #met la valeur 0 pour le chemin du sommet au meme sommet
                    Tableau+=' {:^3} |'.format(resultat_Djikistra[i][self.Liste_Sommets[j].nom])  
                else:
                    Tableau+=' {:^3} |'.format(resultat_Djikistra[i][self.Liste_Sommets[j]])  
        return Tableau
  
    
#créer toute la page HTML  
    def Page_Html(self,resultat_Djikistra,rajout_dans_html):#crée la code HTML pour créer la page HTML contenant l'image, les arcs du plus long des plus courts chemins et le Tableau des résultats 
        Table='<html>  <br /> <title> Page_HTML_Projet_104_Rey </title><br /> <head> <br />{}<br /><table border="1" cellpadding="15">  <FONT size="6pt">Distance minimale entre les sommets:</FONT>  <tr><th></th>'.format(rajout_dans_html) #rajout me permet de directement mettre l'image et les arcs du plus long des plus courts chemins
        for i in range(len(resultat_Djikistra)):
            Table+='<th>{}</th>'.format(self.Liste_Sommets[i]) 
        Table+='</tr>'
        for i in range(len(resultat_Djikistra)):
            Table+='<tr> <th>{}</th>'.format(self.Liste_Sommets[i])
            for j in range(len(Graphe1.Liste_Sommets)):
                if i==j: #met la valeur 0 pour le chemin du sommet au meme sommet
                    Table+=' <td>{}</td>'.format(resultat_Djikistra[i][self.Liste_Sommets[j].nom])  
                if i!=j: #met le poids correspondant a l'arc entre le sommet i et le sommet j
                        Table+=' <td>{}</td>'.format(resultat_Djikistra[i][self.Liste_Sommets[j]])
        Table+=' </head> \n </html>' 
        return Table         

                    
#appelle du trajet le plus long pour le mettre en rouge    
#rejette le texte que Graphviz peut lire  
    def Graphviz(self,trajet_le_plus_long): 
        graphe='digraph G {' #initialisation pour la lrecture via graphviz
        Liste_Arcs=[] #je crée une copie de self.Liste_Arcs mais plus en la décrivant par l'objet Arc car il est incomparable à un tuple, vu qu'il ne sont pas du même type 
        for elt in self.Liste_Arcs:
            Liste_Arcs.append((elt.depart,elt.arrive,elt.poids))        
        for elt in Liste_Arcs:
            if elt not in trajet_le_plus_long: #Verifie que l'arc n'est pas dans la trajet du plus long des plus court chemin pour ne pas le crée en rouge
                graphe+=' {} -> {} [label = {}];'.format(elt[0],elt[1],elt[2])  #création de l'arc avec le poids correspondant au plus long des plus courts chemins pour le tracer
            else:
                graphe+='{0} [color=red];{1} [color=red];{0} -> {1} [label = {2},color = red];'.format(elt[0],elt[1],elt[2])  #création de l'arc avec le poids correspondant au plus long des plus courts chemins pour le tracer en rouge
        graphe+='rankdir=LR}' #le rankdir permet de mettre l'image en format paysage
        return graphe




                        
                
class Arc() :
    def __init__(self, depart ,arrive, poids):
        self.depart=depart
        self.arrive=arrive
        self.poids=poids
       
    def __repr__(self):
        return '({},{},{})'.format(self.depart,self.arrive,self.poids)
 
    
 
   

    
class Sommet() :
    def __init__(self, nom):
        self.nom = nom
        self.voisins = [] #liste contenant les tuples (arrivé, poids)



    def __repr__(self):
        return '{}'.format(self.nom)



#Calcul tous les poids des chemins possible à partir d'un sommet de départ d'un certain graphe
#return le dictionnaire contenant le sommet d'arrivé et le poids totale entre ce sommet et le sommet de départ
    def Dijkstra(self,nom_graphe):     
        calcules = [self.nom] #rempli la liste des sommets calculés
        provisoire = [] #sommet en attente d'être calculés
        dictionnaire_poids={self.nom:0} #clé=arrivé et valeur=poids depuis le point de depart
        for elt in self.voisins:
            provisoire.append(nom_graphe.Dictionnaire_objet_nom[elt[0]]) #rajoute tous les noms des voisins de départ, utilisation du dictionnaire pour associer l'objet et non juste le nom de la variable
            dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]=elt[1] #clé=arrivé et valeur=poids depuis le point de depart, utilisation du dictionnaire pour associer l'objet et non juste le nom de la variable
        while provisoire: # correspond à provisoire n'est pas vide
            prochain= provisoire[0]  #initialisation du sommet pour trouver le sommet le plus proche
            minimum_poids=dictionnaire_poids[prochain]   #initialisation du poids minimum
            indice=0   #initialisation de l'indice du sommet dans provisoire
            for i in range(len(provisoire)): #recherche du sommet le plus proche
                if dictionnaire_poids[provisoire[i]]<minimum_poids: 
                    prochain=provisoire[i]   
                    minimum_poids= dictionnaire_poids[provisoire[i]]   
                    indice=i
            calcules.append(prochain) #rajout du sommet le plus proche à la liste calculés 
            provisoire.pop(indice) #on enlève le sommet le plus proche de  la listre provisoire
            for elt in prochain.voisins:
                if nom_graphe.Dictionnaire_objet_nom[elt[0]] not in calcules:  #verifie que le sommet n'est pas déja dansla liste calculés
                    if nom_graphe.Dictionnaire_objet_nom[elt[0]] in provisoire: #verifie que le sommet est dans provisoire
                        if dictionnaire_poids[prochain]+elt[1]<dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]:
                            dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]=dictionnaire_poids[prochain]+elt[1] #prise en compte du nouveau poids
                    else:
                        provisoire.append(nom_graphe.Dictionnaire_objet_nom[elt[0]]) #rajout du sommet dans provisoire
                        dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]=dictionnaire_poids[prochain]+elt[1] #prise en compte du nouveau poids
        return dictionnaire_poids   



#version qui va enregistrer les arcs parcourus pour pouvoir faire l'historique du plus long des plus courts chemins j'aurais pu la faire dans le même algo mais pour pas avoir à calculer tous les historiques de chemins pour tous les sommets j'ai fais cette fonction annexe
    def Dijkstra_plus_long_chemin(self,nom_graphe): 
        calcules = [self.nom]
        Historique_chemin=[]
        provisoire = []
        dictionnaire_poids={self.nom:0} #clé=arrivé et valeur=poids depuis le point de depart
        for elt in self.voisins:
            provisoire.append(nom_graphe.Dictionnaire_objet_nom[elt[0]]) #rajoute tous les noms des voisins de départ, utilisation du dictionnaire pour associer l'objet et non juste le nom de la variable
            dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]=elt[1] #clé=arrivé et valeur=poids depuis le point de depart, utilisation du dictionnaire pour associer l'objet et non juste le nom de la variable
        while provisoire: # correspond à provisoire n'est pas vide
            Dico_historique_arc={}   #remise à zéro du Dico_historique_arc
            prochain= provisoire[0]   #initialisation du sommet pour trouver le sommet le plus proche
            minimum_poids=dictionnaire_poids[prochain]    #initialisation du poids minimum
            indice=0  #initialisation de l'indice du sommet dans provisoire
            for i in range(len(provisoire)): #recherche du minimum
                if dictionnaire_poids[provisoire[i]]<minimum_poids:
                    prochain=provisoire[i]
                    minimum_poids= dictionnaire_poids[provisoire[i]]
                    indice=i
            calcules.append(prochain)
            provisoire.pop(indice)
            for elt in prochain.voisins:
                if nom_graphe.Dictionnaire_objet_nom[elt[0]] not in calcules:  
                    if nom_graphe.Dictionnaire_objet_nom[elt[0]] in provisoire:
                        if dictionnaire_poids[prochain]+elt[1]<dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]:
                            dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]=dictionnaire_poids[prochain]+elt[1]                          
                    else:
                        provisoire.append(nom_graphe.Dictionnaire_objet_nom[elt[0]])
                        dictionnaire_poids[nom_graphe.Dictionnaire_objet_nom[elt[0]]]=dictionnaire_poids[prochain]+elt[1]
                        Dico_historique_arc[prochain]=nom_graphe.Dictionnaire_objet_nom[elt[0]] #rajout dans le dictionnaire du sommet précédent en tant que clé et du sommet suivant en tant que valeur
            if Dico_historique_arc!={}: #si dico_historique_arc n'est pas vide
                Historique_chemin.append(Dico_historique_arc) 
        return Historique_chemin
    
    
   #crée les différents texte pour les ajouter soit dans le shell soit dans le fichier HTML  #dans ce programme on utilise list sur les types dict_keys ou dict_values car ils sont pas iterable  
   #sort aussi Liste_graphviz pour faciliter la conception du graphe avec Graphviz et le meme texte mais pour une lecture via le html
    def plus_long_chemin_historique(self,nom_graphe):
       texte_chemins_le_plus_long='\nArcs contenus dans le plus long des plus courts chemins: \n' #initialisation du texte pour le shell
       Liste_Graphviz=[] #liste pour aider à la conception de l'image du graphe
       Historique_chemin=self.Dijkstra_plus_long_chemin(nom_graphe)
       Historique_chemin=[{self:list(Historique_chemin[0].keys())[0]}]+Historique_chemin+[{list(Historique_chemin[-1].values())[0]:'Ok'}] #on ajoute le premier chemin qui n'était pas inclus dans la liste crée par algo_plus_long_chemin et un dernier juste pour que la fonction finissent la lecture de liste normalement
       texte_chemins_le_plus_long_html='<br />Arcs contenus dans le plus long des plus courts chemins: <br /><br />' #initialisation du texte pour le HTML
       i=0 #initialisation de la constante de lecture pour le while
       while i<len(Historique_chemin)-1:
           elt_comparé=Historique_chemin[i] #initialisation de l'elt comparé
           if list(elt_comparé.values())==list(Historique_chemin[i+1].keys()): #si l'arrivé du dernier dictionnaire dans l'historique de déplacement et le départ des dictionnaires prochains dans l'historique de déplacement sont égale
               for elt in list(elt_comparé.keys())[0].voisins: #boucle pour retrouvé le poids de l'arc correspondant
                   if nom_graphe.Dictionnaire_objet_nom[elt[0]]==list(Historique_chemin[i+1].keys())[0]: #si le voisin de l'elt comparé est égale au départ du prochain arc dans l'historique de déplacement
                       texte_chemins_le_plus_long+='Origine: {}, Extremité: {}, Poids: {} \n'.format(list(elt_comparé.keys())[0],list(Historique_chemin[i+1].keys())[0],elt[1]) #ici on remplie le texte avec départ/arrivé/poids pour le shell
                       Liste_Graphviz.append((list(elt_comparé.keys())[0].nom,list(Historique_chemin[i+1].keys())[0].nom,int(elt[1]))) #je chnage le format pour que la comparaison avec la liste d'arc soit facilité lors de la création du graphe avec graphviz
                       texte_chemins_le_plus_long_html+='Origine: <B>{}</B>, Extremité: <B>{}</B>, Poids: <B>{}</B> <br />'.format(list(elt_comparé.keys())[0],list(Historique_chemin[i+1].keys())[0],elt[1]) #ici on remplie le texte avec départ/arrivé/poids pour le HTML
               i+=1
           else:
               Historique_chemin.pop(i+1)
               for elt in list(elt_comparé)[0].voisins: #boucle pour retrouvé le poids de l'arc correspondant
                   if nom_graphe.Dictionnaire_objet_nom[elt[0]]==list(Historique_chemin[i+2].keys())[0]: #si le voisin de l'elt comparé est égale au départ du prochain arc dans l'historique de déplacement
                       texte_chemins_le_plus_long+='Origine: {}, Extremité: {}, Poids: {} \n'.format(list(elt_comparé.keys())[0],list(Historique_chemin[i+2].keys())[0],elt[1]) #ici on remplie le texte avec départ/arrivé/poids pour le shell
                       Liste_Graphviz.append((list(elt_comparé.keys())[0].nom,list(Historique_chemin[i+1].keys())[0].nom,int(elt[1]))) #je chnage le format pour que la comparaison avec le la liste d'arc soit facilité lors de la création du grpahe avec graphviz
                       texte_chemins_le_plus_long_html+='Origine : <B>{}</B>, Extremité : <B>{}</B>, Poids : <B>{}</B> <br />'.format(list(elt_comparé.keys())[0],list(Historique_chemin[i+2].keys())[0],elt[1]) #ici on remplie le texte avec départ/arrivé/poids pour le HTML
                       i+=2
       return texte_chemins_le_plus_long,Liste_Graphviz,texte_chemins_le_plus_long_html 









#Initialisation du Graphe:            
Graphe1=Graphe(donnees[0],donnees[1],donnees[2])
Graphe1.Liste_creation(donnees[2],donnees[1])




#Resultats pour le Graphe:
Resultat=[]
for elt in Graphe1.Liste_Sommets:
    Resultat.append(elt.Dijkstra(Graphe1))
 
    


#Pour trouver le plus long des plus court chemin à partir de résultat
Le_plus_long_des_plus_courts_chemins=0 
arrive_long=0
depart_long=0
for i in range(len(Resultat)):
    for elt in Resultat[i].keys():
        if Resultat[i][elt]!= '-':
            if Resultat[i][elt]>Le_plus_long_des_plus_courts_chemins:
                Le_plus_long_des_plus_courts_chemins=Resultat[i][elt]
                arrive_long=elt
                depart_long= Graphe1.Liste_Sommets[i]
print('Le plus long des plus courts chemins est de {} à {} en {}'.format(depart_long,arrive_long,Le_plus_long_des_plus_courts_chemins))
Long_Chemin=depart_long.plus_long_chemin_historique(Graphe1)
print(Long_Chemin[0])




#Pour créer le tableau dans le shell         
Tableau=Graphe1.Tableau_Shell(Resultat)                                     
print(Tableau)                  





#Pour créer l'image du graphe sous format PNG
graphe_image=Graphe1.Graphviz(Long_Chemin[1])
Graphe=open('graphe.gv','w')
Graphe.write(graphe_image)
Graphe.close()
subprocess.call(['C:\\Users\\thoma\\anaconda3\\Library\bin\\dot.exe',"-Tpng","-ographe.png","graphe.gv"])  #mettre le chemin correspondant à son ordinateur pour acceder au dot.exe de graphviz





#Pour créer le Tableau dans le html                       
fichier=open('Tableau des poids des chemins.html','w')
fichier.write(Graphe1.Page_Html(Resultat,'<p> <FONT size="6pt">Graphe étudié:</FONT><br /> <img src="graphe.png" alt="Image du graphe"/> </p> <br /> <FONT size="6pt">Le plus long des plus courts chemins est de {} à {} en {}</FONT><br />'.format(depart_long,arrive_long,Le_plus_long_des_plus_courts_chemins)+Long_Chemin[2]))   #le rajout permet de mettre directement l'image et les arcs contenus dans le plus long des plus courts chemins
fichier.close()




#Essai d'utilisation de Simple Parser, cependant elle ne fonctionne pas elle n'arrive pas à lire tout le fichier et je n'arrive pas à comprendre pourquoi

fichier=open('C:\\Users\\thoma\\Desktop\\104\\Graphe1.txt','r') #mettre le chemin pour acceder au fichier Graphe1.txt
Texte_fichier=fichier.read()
fichier.close()
print(Texte_fichier)























