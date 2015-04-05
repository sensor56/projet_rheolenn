#!/usr/bin/python
# -*- coding: utf-8 -*-

# code Python obtenu avec l'IDE Pyduino - www.mon-club-elec.fr 

from pyduino_pcduino import * # importe les fonctions Arduino pour Python


from bottle import route, run, template, static_file # importe classes utile du module Bottle
# dependances : 
# sudo apt-get install python-bottle
# sudo apt-get install python-cherrypy3 (pour serveur multithread)

# entete declarative
noLoop=True # bloque loop

ipLocale=Ethernet.localIP() # auto - utilise l'ip de l'interface eth0 du systeme
#ipLocale="127.0.0.1"

port=8080 # attention port doit etre au dessus de 1024 sinon permission refusee par securite - 8080 pour http

#---- les routes doivent etre definies avant lancement bottle

#--- gestion requetes HTML --- 
@route('/')
def bottleHtmlInitial():
	return pageInitialeHTMLJS()

#-- route pour gestion fichier statique pour libairie js locale 
@route('/static/<filename:path>')
def send_static(filename):
	return static_file(filename, root='./static/') # utilisation chemin relatif
	# le rep /static doit exister dans rép app *.py--
	#return static_file(filename, root=currentdir()+'static/') # si utilisation chemin absolu

#--- setup ---
def setup():
	
	print "dir="+currentdir()+'static/' # debug
	
	run(host=ipLocale,port=port, server='cherrypy') # bottle lance automatiquement le wsgiserver de cherrypy (multithread)


#--- fin setup

# -- loop --
def loop():
	return

# -- fin loop --

#--- fonction fournissant la page HTML ---
def pageInitialeHTMLJS():

	pageHTML=( # debut page HTML
"""
<!DOCTYPE HTML> 

		<!-- Debut de la page HTML  --> 
     <html> 
      
     	<!-- Debut entete --> 
 	    <head> 
 	    
			<meta charset="utf-8" /> <!-- Encodage de la page  --> 
			<title>Titre</title> <!-- Titre de la page --> 

"""
+includeJS()+
"""

			<!-- Debut du code Javascript  --> 
 			<script language="javascript" type="text/javascript"> 

"""
+codeJS()+
"""

			</script> 
			<!-- Fin du code Javascript -->     

 	    </head> 
 	    <!-- Fin entete --> 
	    
	 <!-- Debut Corps de page HTML --> 
	<body > 
"""
+bodyHTML()+
"""
     	</body> 
     	<!-- Fin de corps de page HTML  --> 
     	 
     </html> 
     <!-- Fin de la page HTML  --> 
"""
)  # fin page HTML
	return pageHTML # la fonction renvoie la page HTML

#------ fonction retournant le body de la page HTML ---- 
def bodyHTML():
	
	bodyHTML="""
	
	<canvas id="smoothieCanvas" width="300" height="100"></canvas> <!-- canvas pour graphique smoothie -->   

 
"""
	
	return bodyHTML
	
	
#------ fonction fournissant les fichiers JS a inclure -----
def includeJS():
	includeJS="""
	
        <script src="static/smoothie.js" type="text/javascript" ></script>

	
"""
	return includeJS
	
	
#------ fonction fournissant le code Javascript / jQuery de la page HTML----
def codeJS():
	codeJS=(
"""
                        // variables globales
  		         var randomSerie = new TimeSeries(); // crée un objet série de date - fournit par lib smoothie
                        var smoothieGraph = new SmoothieChart(); // crée un objet graphique smoothie - fournit par lib smoothie
                         window.onload = function () { // au chargement de la page        
                                        
 
                                        // initialisation du graphique smoothie
                                        smoothieGraph.addTimeSeries(randomSerie, { strokeStyle: 'rgba(0, 255, 0, 1)', fillStyle: 'rgba(0, 255, 0, 0.2)', lineWidth: 2 });
                                        smoothieGraph.streamTo(document.getElementById("smoothieCanvas"), 500); // définition canva et vitesse défilement

                               	 setInterval(function() { refreshSmoothieGraph()}, 500); // fixe délai actualisation

                                        // le résultat final est le fruit du mixage entre vitesse de défilement et délai actualisation valeur
                                                                                                        
                        } // fin onload    
                        // fonction d'actualisation de la série de valeur à intervalle régulier
                        function refreshSmoothieGraph(){
                                randomSerie.append(new Date().getTime(), Math.random() * 4096); // ajoute donnée à la série de données - ici aléatoire                  
                        }

""")
	
	return codeJS

#--- fin du code Javascript / jQuery  --- 


#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
