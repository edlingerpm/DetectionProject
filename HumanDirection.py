# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 2020

@author: Pierre-Marie EDLINGER
"""
import cv2
import operator
import RutaipCommonFunctions as Rtp
import numpy as np

###############################################################################
#positions: 0 = rien; 1 = haut; 2=droite; 3=bas; 4=gauche 
def dessineTriangle(fenetre, capture, position):
    if position != 0:
        largeur = int(capture.get(3))
        hauteur = int(capture.get(4))
        centreHorizontal = largeur/2
        centreVertical = hauteur/2
        if position == 1: #dessine un triangle en haut
            pts = np.array([[centreHorizontal,10],[centreHorizontal-50,40],[centreHorizontal+50,40]], np.int32)
        elif position == 2: #dessine un triangle à droite
            pts = np.array([[largeur-10,centreVertical],[largeur-40,centreVertical-50],[largeur-40,centreVertical+50]], np.int32)
        elif position == 3: #dessine un triangle en bas
            pts = np.array([[centreHorizontal,hauteur-10],[centreHorizontal-50,hauteur-40],[centreHorizontal+50,hauteur-40]], np.int32)
        elif position == 4: #dessine un triangle à gauche
            pts = np.array([[10,centreVertical],[40,centreVertical-50],[40,centreVertical+50]], np.int32)
        #dessine le triangle
        pts = pts.reshape((-1,1,2))
        cv2.polylines(fenetre, [pts],True,(0,255,0), 5)
###############################################################################

#création d'un répertoire + nommage du fichier final
Rtp.creationRepertoireImage()    
nom = './Images/images_Visage.jpg'

#Ouverture de la camera
cap = Rtp.choixCamera()

# choix du fichier haarcascade
face_cascade=cv2.CascadeClassifier("./Haarcascade/haarcascade_frontalface_alt2.xml")

largeurFenetre = int(cap.get(3))
hauteurFenetre = int(cap.get(4))
marge=70
centreVertical = largeurFenetre/2
centreHorizontal = hauteurFenetre/2

#sert à décider si on continue ou pas, pourra servir 
#si on utilise le code ci-dessous à partir d'ailleur
#continuation = True

#directionFleche = 0 #0 = rien; 1 = haut; 2=droite; 3=bas; 4=gauche
tab_fleche=[0,0,0,0,0]

while True:
    ret, frame=cap.read()
    
    # création d'un tableau
    tab_face=[]
    
    #########################################################################
    #    Gestion de l'IA qui rempli un tableau 
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face=face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in face:
        tab_face.append([x, y, x+w, y+h])

    tab_face=sorted(tab_face, key=operator.itemgetter(0, 1))
    index=0
    #########################################################################
        
    for x, y, x2, y2 in tab_face:
        #   s'il y a eu un visage de décelé
        if not index or (x-tab_face[index-1][0]>marge or y-tab_face[index-1][1]>marge):

            #proche du centre de l'image
            if (x - (largeurFenetre-x2) < 10)and(y - (hauteurFenetre-y2) < 10) : 
                # je ne veux pas qu'un rectangle apparaisse sur la photo
                cv2.rectangle(frame, (0, 0), (1, 1), (0, 0, 255), 2)
                tab_fleche=[0,0,0,0,0]
                
                try:
                    #enregistrement de l'image
                    cv2.imwrite(nom,frame)
                    #print("image créée!")
                    # fermeture du programme ou pas
                    #continuation = False
                except:
                    print("Problème d'enregistrement de l'image!")
            else : # si on est pas encore au centre, il faut guider avec les flèches
                #0 = rien; 1 = haut; 2=droite; 3=bas; 4=gauche
                #si x2 est trop à droite --> flèche gauche 
                #!!!!!! inverser car caméra inverse l'image. à adapter plus tard
                if x2 > (centreVertical+(x2-x)/2) : 
                    tab_fleche[2] = 2
                else : tab_fleche[2] = 0
                    
                # si x est trop à gauche --> flèche droite
                if x < (centreVertical-(x2-x)/2) : 
                    tab_fleche[4] = 4
                else : tab_fleche[4] = 0
                
                # si y est trop haut --> flèche bas
                if y < (centreHorizontal-(y2-y)/2) : 
                    tab_fleche[3] = 3
                else : tab_fleche[3] = 0
                
                # si y est trop bas --> flèche haut
                if y2 > (centreHorizontal+(y2-y)/2) : 
                    tab_fleche[1] = 1
                else : tab_fleche[1] = 0
                
                
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)
        index+=1
    
    #dessine les triangles
    for i in tab_fleche :
        dessineTriangle(frame, cap, i)

    cv2.imshow('video', frame)
    
    #print(cv2.waitKey(1))
    
    # taper "q" pour quitter le programme
    if cv2.waitKey(1)&0xFF==ord('q'):
        #print("quitter")
        #continuation = False
        break
    
    # taper "e" pour faire une image
    if cv2.waitKey(1)&0xFF==ord('e'):
        #enregistrement de l'image
        print("Enregistrment de l'image")
        break
        
    
cap.release()
cv2.destroyAllWindows()

