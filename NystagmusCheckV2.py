# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 2020

@author: Pierre-Marie EDLINGER
"""
import cv2
import numpy as np
from datetime import datetime
import RutaipCommonFunctions as Rtp

TEMPSCOMMENCEMENT = 5
TEMPSATTENTE = 2

SURFACESIGNIFICATIVE = 15000

def test(typeTest, camera):
    #Aucune frame n'a encore été capturée, prevFrame est donc initialisée à None
    prevFrame = None
    premiereFrame = None
    derniereFrame = None
    #Continuer = True
    ComparaisonFaite = False
    ABouge=False
    
    now = datetime.now()
    
    DerniereImageEnregistree = False
    
    #0: oeil vers la droite; 1: oeil vers la gauche; oeil vers le centre
    if typeTest == 1:
        Rtp.joueSon("./Sons/NystagmusDroite.mp3")
    else :
        if typeTest == 2:
            Rtp.joueSon("./Sons/NystagmusGauche.mp3")
        else :
            Rtp.joueSon("./Sons/NystagmusCentre.mp3")

    while True:
        (grabbed,frame) = camera.read()
        #Si la frame n'est pas lu correctement dans le buffer, on quitte la boucle
        if not grabbed:
            break
        
        later = datetime.now()
        difference = (later - now).total_seconds()
        
        
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(25,25), 0)
        
        # affichage du texte qui dit qu'il reste TEMPSCOMMENCEMENT secondes
        if difference <= TEMPSCOMMENCEMENT :
            Rtp.afficheTexte(frame, "Debut dans "+ str(TEMPSCOMMENCEMENT-int(difference)) +" secondes")
        else:    
            #on garde en mémoire la 1ère image
            if premiereFrame is None:
                premiereFrame = gray
                #enregistrement de l'image
                ret, frame=camera.read()
                print("enregistrement 1ère image")
                cv2.imwrite(cheminImage+"Nystagmus 1.jpg",frame)
            
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
        
        cv2.imshow('Nystagmus',frame)
    
    
        if prevFrame is None:
            prevFrame = gray
    
                
        if (DerniereImageEnregistree)&(ComparaisonFaite==False) :
            ComparaisonFaite=True
            #print("ICI")
        #On fait la difference absolue de l'image actuelle et la precedente
        #On fait un seuillage binaire sur cette nouvelle image
        #Puis on la dilate pour pouvoir plus facilement trouver les contours par la suite
            frameDelta = cv2.absdiff(premiereFrame,derniereFrame)
            thresh = cv2.threshold(frameDelta, 7, 255, cv2.THRESH_BINARY)[1]
            kernel = np.ones((11,11),np.uint8)
            thresh = cv2.dilate(thresh, kernel, iterations=2)
        
            #Recherche des contours des objets de l'image dilate
            (img,contr,hrchy) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
            #Ce mask va nous servir a encadrer l'objet de la couleur de celui ci
            #mask = np.zeros(frame.shape[:2],np.uint8)
    
            for c in contr:
                #Tous les petits objets sont ignorés avec cette ligne
                if cv2.contourArea(c) < SURFACESIGNIFICATIVE:
                    continue
                if cv2.contourArea(c) >= SURFACESIGNIFICATIVE:
                    #print("L'oeil a bougé.")
                    ABouge=True    
                
            # if (ABouge==False):
            #     print("L'oeil n'a pas bougé.")
                
            return ABouge
                
        #On affiche la video avec les rectangles
        #cv2.imshow('contour',frame)
    
        #l'image actuelle devient la future image précédente
        prevFrame = gray
        
        #Quitte la capture video lorsque la touche q est appuyée
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
    


#Ouverture de la camera
cap = Rtp.choixCamera()


#création d'un répertoire
Rtp.creationRepertoireImage()    
cheminImage = './Images/'

# oeil qui regarde à droite
if test(1, cap)==False:
    print("L'oeil vers la droite n'a pas bougé.")
    # oeil qui regarde à gauche
    if test(2, cap)==False:
        print("L'oeil vers la gauche n'a pas bougé.")
        # oeil qui regarde vers le centre
        if test(3, cap)==False:
            print("L'oeil vers le centre n'a pas bougé.")
        else: print("Nystagmus oeil au centre")
    else: print("Nystagmus oeil vers la gauche")
else: print("Nystagmus oeil vers la droite")

#while True:
    # (grabbed,frame) = cap.read()
    # #Si la frame n'est pas lu correctement dans le buffer, on quitte la boucle
    # if not grabbed:
    #     break
    
    # later = datetime.now()
    # difference = (later - now).total_seconds()
    
    
    # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray,(25,25), 0)
    
    # # affichage du texte qui dit qu'il reste TEMPSCOMMENCEMENT secondes
    # if difference <= TEMPSCOMMENCEMENT :
    #     Rtp.afficheTexte(frame, "Debut dans "+ str(TEMPSCOMMENCEMENT-int(difference)) +" secondes")
    # else:    
    #     #on garde en mémoire la 1ère image
    #     if premiereFrame is None:
    #         premiereFrame = gray
    #         #enregistrement de l'image
    #         ret, frame=cap.read()
    #         print("enregistrement 1ère image")
    #         cv2.imwrite(cheminImage+"Nystagmus 1.jpg",frame)
        
    #     #on garde en mémoire la dernière image
    #     if (int(difference) == TEMPSATTENTE+TEMPSCOMMENCEMENT)&(DerniereImageEnregistree==False):
    #         derniereFrame = gray
    #         ret, frame=cap.read()
    #         print("enregistrement dernière image")
    #         cv2.imwrite(cheminImage+"Nystagmus 2.jpg",frame)
    #         DerniereImageEnregistree = True
            
    #     # lorsqu'on a dépassé le chrono
    #     if difference < TEMPSATTENTE+TEMPSCOMMENCEMENT:
    #         Rtp.afficheTexte(frame, "Don't move. Still "+ str((TEMPSATTENTE+TEMPSCOMMENCEMENT)-int(difference)) +" seconds")
    
    # cv2.imshow('Nystagmus',frame)


    # if prevFrame is None:
    #     prevFrame = gray

            
    # if (DerniereImageEnregistree)&(ComparaisonFaite==False) :
    #     ComparaisonFaite=True
    #     #print("ICI")
    # #On fait la difference absolue de l'image actuelle et la precedente
    # #On fait un seuillage binaire sur cette nouvelle image
    # #Puis on la dilate pour pouvoir plus facilement trouver les contours par la suite
    #     frameDelta = cv2.absdiff(premiereFrame,derniereFrame)
    #     thresh = cv2.threshold(frameDelta, 7, 255, cv2.THRESH_BINARY)[1]
    #     kernel = np.ones((11,11),np.uint8)
    #     thresh = cv2.dilate(thresh, kernel, iterations=2)
    
    #     #Recherche des contours des objets de l'image dilate
    #     (img,contr,hrchy) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    #     #Ce mask va nous servir a encadrer l'objet de la couleur de celui ci
    #     #mask = np.zeros(frame.shape[:2],np.uint8)

    #     for c in contr:
    #         #Tous les petits objets sont ignorés avec cette ligne
    #         if cv2.contourArea(c) < SURFACESIGNIFICATIVE:
    #             continue
    #         if cv2.contourArea(c) >= SURFACESIGNIFICATIVE:
    #             print("L'oeil a bougé.")
    #             ABouge=True    
            
    #     if (ABouge==False):
    #         print("L'oeil n'a pas bougé.")
            
    # #On affiche la video avec les rectangles
    # cv2.imshow('contour',frame)

    # #l'image actuelle devient la future image précédente
    # prevFrame = gray

    # #Quitte la capture video lorsque la touche q est appuyée
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    
cap.release()
cv2.destroyAllWindows()