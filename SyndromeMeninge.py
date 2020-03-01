# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 2020

@author: Pierre-Marie EDLINGER
"""
import cv2
import RutaipCommonFunctions as Rtp

testMenton=False
testProfilGauche=False
testProfilDroit=False
visageFaceDecele=False
profileDecele=False
retourFace=False

#création d'un répertoire + nommage du fichier final
Rtp.creationRepertoireImage()    
cheminImage = './Images/images_TestYeux.jpg'  

#Ouverture de la camera
cap = Rtp.choixCamera()

# initialize the recognizers
face_cascade=cv2.CascadeClassifier("./Haarcascade/haarcascade_frontalface_alt2.xml")
profile_cascade=cv2.CascadeClassifier("./Haarcascade/haarcascade_profileface.xml")


"""
trouver le visage de face
lui demander de baisser le menton --> le visage ne doit plus être décelé
merci, regardez en face de vous
lui demander de tourner la tête à droite --> le profil gauche doit être décelé
merci, regardez en face de vous
lui demander de tourner la tête à gauche --> un profil droit doit être décelé
merci, cet exercice a-t-il été douloureux pour vous?
Proposer fenêtre de réponse
donner résultat

"""

while True:
    # read the image from the cam
    ret, frame = cap.read()
    
    # converting to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detect all the faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # detect all the profiles in the image
    profiles = profile_cascade.detectMultiScale(gray, 1.2, 5)

    #Rtp.joueSon("./Sons/OpenEyes.mp3") 
    
    # for every face, draw a blue rectangle
    for x, y, width, height in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
    
    if len(faces)>0:
        visageFaceDecele=True
    else:
        visageFaceDecele=False
        
    # for every profile, draw a green rectangle
    for x1, y1, width1, height1 in profiles:
        cv2.rectangle(frame, (x1, y1), (x1 + width1, y1 + height1), color=(0, 255, 0), thickness=2)
        
    if len(profiles)>0:
        profileDecele=True
    else:
        profileDecele=False   
        
    
# """
# trouver le visage de face
# lui demander de baisser le menton --> le visage ne doit plus être décelé
# merci, regardez en face de vous
# lui demander de tourner la tête à droite --> le profil gauche doit être décelé
# merci, regardez en face de vous
# lui demander de tourner la tête à gauche --> un profil droit doit être décelé
# merci, cet exercice a-t-il été douloureux pour vous?
# Proposer fenêtre de réponse
# donner résultat

# """

    if (testMenton==False):
        print("testmenton")
        Rtp.joueSon("./Sons/BaisserMenton.mp3")
        if visageFaceDecele==False:
            testMenton=True
            Rtp.joueSon("./Sons/LookForward.mp3")
    else : # le test du menton a été fait, on passe aux tests suivants
        if (testProfilGauche==False):
            print("test profile gauche")
            Rtp.joueSon("./Sons/TeteADroite.mp3")
            if (profileDecele==True)&(visageFaceDecele==False):
                testProfilGauche=True
                retourFace=False
                Rtp.joueSon("./Sons/LookForward.mp3")
        else : # le test du profil gauche a été fait, on passe au profil droit
            if (testProfilDroit==False):
                print("test profile droit")
                Rtp.joueSon("./Sons/TeteAGauche.mp3")
                if (profileDecele==True)&(visageFaceDecele==False)&(retourFace==True):
                    testProfilDroit=True
    
    if (testMenton)&(testProfilGauche)&(visageFaceDecele):
        retourFace = True
        
    if (testMenton)&(testProfilGauche)&(testProfilDroit):
        #print("Demander si douleur")
        Rtp.joueSon("./Sons/Douloureux.mp3")
        if Rtp.poseQuestion("Questionnaire", "Ce test a-t-il été douloureux pour vous?"):
            print("Douloureux")
        else:
            print("Pas douloureux")
        break
        
    cv2.imshow("image", frame)
    
    #On quitte lorsque la touche "q" est pressée
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
