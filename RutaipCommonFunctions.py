# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 2020

@author: Pierre-Marie EDLINGER
"""
import os
import cv2
import pygame

#création d'un répertoire + nommage du fichier final
def creationRepertoireImage():
    cheminImage = "./Images/"
    try:
        # Bloc à essayer - création du répertoire
        os.mkdir(cheminImage)
    except:
        # Bloc qui sera exécuté en cas d'erreur
        None  
    
def choixCamera():
    return cv2.VideoCapture(1)

def afficheTexte(image ,texteAAfficher):
    cv2.putText(image, texteAAfficher, (20,20), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2, 1)

def joueSon(nomDuSon):

    # pygame.init()

    pygame.mixer.music.load(nomDuSon)
    print(nomDuSon)

    pygame.mixer.music.play()