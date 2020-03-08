# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 2020

@author: Pierre-Marie EDLINGER
"""
import cv2
import RutaipCommonFunctions as Rtp
from datetime import datetime
import time

time.sleep(5)

TEMPSEXERCICE = 5

#création d'un répertoire + nommage du fichier final
Rtp.creationRepertoireImage()    
cheminImage = './Images/images_TestYeux.jpg'  

#Ouverture de la camera
cap = Rtp.choixCamera()

# initialize the eyes recognizer
face_cascade = cv2.CascadeClassifier("./Haarcascade/haarcascade_eye.xml")

now = datetime.now()

testFait = False

Rtp.joueSon("./Sons/CloseEyes.mp3")

while True:
    # read the image from the cam
    ret, frame = cap.read()
    
    later = datetime.now()
    difference = (later - now).total_seconds()
    
    # converting to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detect all the eyes in the image
    faces = face_cascade.detectMultiScale(gray, 3, 5)
    
    #demander de fermer les yeux puis attendre TEMPSEXERCICE secondes avant de compter
    
    if testFait==False:
        Rtp.afficheTexte(frame, "Fermez lez yeux.")
    
    if (difference >= TEMPSEXERCICE)&(testFait==False):
        testFait=True

        cv2.imwrite(cheminImage,frame)
        #puis de donner un résultat
        print(str(len(faces)))
        
        #s'il y a un seul oeil d'ouvert
        if len(faces)==1:
            #regarder où est situé l'oeil par rapport au centre de l'image
            for x, y, width, height in faces:
                if x > 320:
                    print("Oeil gauche ouvert")
                else:
                    print("Oeil droit ouvert")
        
        Rtp.joueSon("./Sons/OpenEyes.mp3") 
    
    # for every eye, draw a blue rectangle
    # for x, y, width, height in faces:
    #     cv2.rectangle(frame, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
    cv2.imshow("image", frame)
    
    #On quitte lorsque la touche "q" est pressée
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
