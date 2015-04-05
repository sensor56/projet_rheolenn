#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - nov 2012 - Tous droits réservés
# GPLv3 - www.mon-club-elec.fr

# modules a importer 
from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..
import os,sys

from tuto_pyqt_bases_modele import * # fichier obtenu à partir QtDesigner et pyuic4

class myApp(QWidget, Ui_Form): # la classe reçoit le Qwidget principal ET la classe définie dans *.py obtenu avec pyuic4
	def __init__(self, parent=None):
		QWidget.__init__(self) # initialise le Qwidget principal 
		self.setupUi(parent) # Obligatoire 

		#Ici, placer le code actif de votre application 
		
		print u"Application qui ne fait rien !"
		
		#======================= DEBUT SECTION DU CODE ACTIF DE VOTRE APPLICATION PyQt =====================

		#-- variables utiles --

		#Ici, personnalisez vos widgets si nécessaire en utilisant les noms définis dans QtDesigner
		
		#Réalisez les connexions supplémentaires entre signaux et slots
		# les widgets sont désignés sous la forme self.nom en utilisant les noms définis dans QtDesigner
		#self.connect(self.pushButton, SIGNAL("clicked()"), self.pushButtonClicked) # connecte le signal Clicked de l'objet bouton à l'appel de la fonction voulue 
		
		# code actif initial 
		#...
		
	#-- fin __init__
	
	# --- les fonctions appelées, utilisées par les signaux 
	#def pushButtonClicked(self):
		#print("Bouton appuyé")

	#--- autres fonctions actives  de la classe principale 
	# …

	#======================= FIN SECTION DU CODE ACTIF DE VOTRE APPLICATION PyQt =====================


def main(args):
	a=QApplication(args) # crée l'objet application 
	f=QWidget() # crée le QWidget racine
	c=myApp(f) # appelle la classe contenant le code de l'application 
	f.show() # affiche la fenêtre QWidget
	r=a.exec_() # lance l'exécution de l'application 
	return r

if __name__=="__main__": # pour rendre le code exécutable 
	main(sys.argv) # appelle la fonction main

