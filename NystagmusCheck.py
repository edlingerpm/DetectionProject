# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 13:52:17 2020

@author: Pierre-Marie
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 2020

@author: Pierre-Marie EDLINGER
"""
import cv2
import numpy as np
from datetime import datetime
import RutaipCommonFunctions as Rtp
import time
import pygame

TEMPSCOMMENCEMENT = 10
TEMPSATTENTE = 2

SURFACESIGNIFICATIVE = 15000

#Ouverture de la camera
cap = Rtp.choixCamera()

#Aucune frame n'a encore été capturée, prevFrame est donc initialisé à None
prevFrame = None
premiereFrame = None
derniereFrame = None
# i=1
# j=1
Continuer = True
ComparaisonFaite = False
ABouge=False
decompteFait=False


DerniereImageEnregistree = False

#création d'un répertoire
Rtp.creationRepertoireImage()    
cheminImage = './Images/'

pygame.init()

# Rtp.joueSon("./Sons/Test3Secondes.mp3")
Rtp.joueSon("./Sons/ApprochRightEye.mp3")

#time.sleep(5)

now = datetime.now()

while True:
    (grabbed,frame) = cap.read()
    
    later = datetime.now()
    difference = (later - now).total_seconds()
    
    # print(str(difference))
    
    if (difference>=4)&(decompteFait==False):
        # print("NOW")
        Rtp.joueSon("./Sons/Test3Secondes.mp3")
        decompteFait = True
    
    #Si la frame n'est pas lu correctement dans le buffer, on quitte la boucle
    if not grabbed:
        break
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(25,25), 0)
    
    # affichage du texte qui dit qu'il reste TEMPSCOMMENCEMENT secondes
    if difference <= TEMPSCOMMENCEMENT :
        Rtp.afficheTexte(frame, "Start in "+ str(TEMPSCOMMENCEMENT-int(difference)) +" seconds")
    else:    
        #on garde en mémoire la 1ère image
        if premiereFrame is None:
            premiereFrame = gray
            #enregistrement de l'image
            ret, frame=cap.read()
            print("enregistrement 1ere image")
            cv2.imwrite(cheminImage+"Nystagmus 1.jpg",frame)
            
        
        #print(str(int(difference)))
        
        #on garde en mémoire la dernière image
        if (int(difference) == TEMPSATTENTE+TEMPSCOMMENCEMENT)&(DerniereImageEnregistree==False):
            derniereFrame = gray
            ret, frame=cap.read()
            print("enregistrement dernière image")
            cv2.imwrite(cheminImage+"Nystagmus 2.jpg",frame)
            DerniereImageEnregistree = True
            
        # lorsqu'on a dépassé le chrono
        if difference < TEMPSATTENTE+TEMPSCOMMENCEMENT:
            Rtp.afficheTexte(frame, "Don't move. Still "+ str((TEMPSATTENTE+TEMPSCOMMENCEMENT)-int(difference)) +" seconds")
    
    cv2.imshow('contour',frame)


    if prevFrame is None:
        prevFrame = gray

            
    if (DerniereImageEnregistree)&(ComparaisonFaite==False) :
        ComparaisonFaite=True
        #print("ICI")
    #On fait la difference absolue de l'image actuelle et la precedente
    #On fait un seuillage binaire sur cette nouvelle image
    #Puis on la dilate pour pouvoir plus facilement trouver les contours par la suite
    #    frameDelta = cv2.absdiff(prevFrame,gray)
        frameDelta = cv2.absdiff(premiereFrame,derniereFrame)
        thresh = cv2.threshold(frameDelta, 7, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones((11,11),np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)
    
        #Recherche des contours des objets de l'image dilate
        (img,contr,hrchy) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
        #Ce mask va nous servir a encadrer l'objet de la couleur de celui ci
        mask = np.zeros(frame.shape[:2],np.uint8)

        for c in contr:
            #Tous les petits objets sont ignorés avec cette ligne
            if cv2.contourArea(c) < SURFACESIGNIFICATIVE:
                continue
            if cv2.contourArea(c) >= SURFACESIGNIFICATIVE:
                print("You moved.")
                ABouge=True    
            
        if (ABouge==False):
            print("You didn't moved.")
                  
        Rtp.joueSon("./Sons/ThankYou.mp3")
            
    #On affiche la video avec les rectangles
    cv2.imshow('contour',frame)

    #l'image actuelle devient la future image precedente
    prevFrame = gray

    #Quitte la capture video lorsque la touche q est appuyée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()