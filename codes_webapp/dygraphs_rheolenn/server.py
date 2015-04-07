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

serverDir=mainPath()+dataPath(TEXT) # le répertoire à servir

#---- les routes doivent etre definies avant lancement bottle

#--- gestion requetes HTML --- 
@route('/')
def bottleHtmlInitial():
	return pageInitialeHTMLJS()

#--- gestion requetes AJAX --- 
@route('/ajax/file(<param>)') # la meme chaine a mettre dans code JS initial requete AJAX
def bottleReponseAjax(param):
	#return reponseAJAX(param)
	return static_file(param, root=serverDir) # utilisation chemin pour renvoyer fichier complet


#-- route pour gestion fichier statique pour libairie js locale 
@route('/static/<filename:path>')
def send_static(filename):
	return static_file(filename, root='./static/') # utilisation chemin relatif
	# le rep /static doit exister dans rép app *.py--
	#return static_file(filename, root=currentdir()+'static/') # si utilisation chemin absolu

#--- setup ---
def setup():
	
	#print "dir="+os.getcwd()+"/"+'static/' # debug
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
	
	<div id="sidebarDiv" style="width: 25%; height: 200px;" ></div>
	<br>
	<div id="graphDiv" style="width: 100%; height: 250px;" ></div>
	<br>
	<div id="gridDiv" style="width: 100%; height: 250px;" ></div>
	<br>
	<textarea rows="10" cols="50" placeholder="Sélectionner un fichier" id="textarea"></textarea>
"""
	
	return bodyHTML
	
	
#------ fonction fournissant les fichiers JS a inclure -----
def includeJS():
	includeJS="""
	
<script src="static/jquery.min.js" type="text/javascript"></script>

<link href="static/w2ui/w2ui.min.css" rel="stylesheet" type="text/css" />
<script src="static/w2ui/w2ui.min.js" type="text/javascript" ></script>

<script src="static/dygraphs/dygraph-combined.js" type="text/javascript" ></script>

	
"""
	return includeJS
	
	
#------ fonction fournissant le code Javascript / jQuery de la page HTML----
def codeJS():
	
	filepath=serverDir
	filename="testdata.txt"
	
	
	codeJS=(
"""
			
	//var dygraphs = null; // variable globale pour objet graphique Dygraphs

$(document).ready(function(){
//$(window).onload(function(){
	
	// initialisation du graphique Dygraphs
	dygraphs = new Dygraph( // creation de l'objet graphique
		document.getElementById("graphDiv"),  // div conteneur - utiliser le meme nom ++ 
		
		"Date,TBal, Tpan, Diff, Circ\\n" +                // serie de donnees de test
" """
+dataFromFile(filepath+filename)+
""" ", // fin serie de donnees 
		
		{ valueRange: [0,30]} // les options du graphique - aucune ici
		
	); // fin new Dygraph

	//--------------------------------------------------------------------------------------
	
		$('#sidebarDiv').w2sidebar({ // integre le sidebar dans le div dedie + parametrage du sidebar
		name: 'sidebard',
		img: null,
		nodes: [ 
			{ id: 'level-1', text: 'Liste des Fichiers :', img: 'icon-folder', expanded: true, group: true,
			  nodes: [ \n"""+
nodesFiles()
					 +"""]
			}
		], // fin nodes
		
		onClick: function (event) {
			//alert('id: ' + event.target);
			//$("#textarea").val(event.target); 
			
			param="file("+event.target+")"
			//$("#textarea").val(param); // debug
			$.get("ajax/"+param, manageReponseAjaxServeur); // envoi d'une requete AJAX
			
		} // fin onclick
		
	}); // w2sidebar
	
	
	//--------------------------------------------------------------------------------------
	
	// initialisation tableau w2ui grid
	$('#gridDiv').w2grid({ // integre le grid dans le div dedie + parametrage du Grid
		name: 'grid',
		header: 'Données horodatées',
		show: { 
			toolbar: true,
			footer: true
		}, // fin show
		multiSearch: true,
		searches: [
			{ field: 'recid', caption: 'ID ', type: 'int' },
			{ field: 'date', caption: 'Date', type: 'date' },
			{ field: 'heure', caption: 'Heure', type: 'text' },
			{ field: 'Tbal', caption: 'Valeur'},
		], // fin search
		columns: [
			//{ field: 'recid', caption: 'ID', size: '20px'},
			//{ field: 'date', caption: 'Date', size: '120px', render: 'date' },
			{ field: 'date', caption: 'Date', size: '120px'},
			{ field: 'heure', caption: 'Heure', size: '20%' },
			{ field: 'TBal', caption: 'TBallon', size: '30%' },
			{ field: 'TPan', caption: 'TPanneau', size: '30%' },
			{ field: 'Diff', caption: 'Diff', size: '30%' },
			{ field: 'Circ', caption: 'Circulateur', size: '30%' }
		], // fin columns
		records: [ // les records doit utiliser le memes champs que columns
			"""
			+dataJSONFromFile(filepath+filename)+
			"""
		] // fin records
	}); // w2grid

	//--------------------------------------------------------------------------------------
	
}); // fin function + fin ready + fin $

"""
+
manageReponseAjaxServeur()
+
"""

""")
	
	return codeJS

#--- fin du code Javascript / jQuery  --- 

#===================== Envoi Reponse AJAX ==================

#--- fonction fournissant la page de reponse AJAX

def reponseAJAX(paramIn):
	
	# fonction inutile ici sur requete fichier statique : on renvoie le fichier directement avec bottle
	# voir la route ajax/file(filename)
	
	print "paramIn="+paramIn # debug
	# la reponse
	reponseAjax=( # debutreponse AJAX
paramIn
)  # fin reponse AJAX

	return reponseAjax



#========== fonction de gestion de la reponse du serveur aux requetes AJAX =========
def manageReponseAjaxServeur():
	manageReponseAjaxServeur=(
"""
//-- fonction de gestion de la réponse AJAX -- 


function manageReponseAjaxServeur(dataIn){
	
	//dataIn=parseInt(dataIn); 
	//$("#textarea").append("ajax : "+ dataIn+"\\n"); 
	//$("#textarea").get(0).setSelectionRange($("#textarea").get(0).selectionEnd-1,$("#textarea").get(0).selectionEnd-1); // se place en derniere ligne -1 pour avant saut de ligne 
	
	$("#textarea").val("ajax : "+ dataIn+"\\n");
	
	//--- MAJ du Dygraphs avec les data brutes 
	dygraphs.updateOptions( { 'file': dataIn } ); // met a jour les donnees du graphique
	dygraphs.resetZoom(); // RAZ le zoom pour les nouvelles data
	
	
	//--- mise en forme du fichier texte reçu en réponse Ajax pour le w2grid
	// line txt to JSON txt : 2014-07-27 23:59:00,236 ln ==> { "recid": "1", "date": "06/10/2014", "heure": "12:05:32", "val1": "235"}
	
	dataLines=dataIn.split('\\n'); // sépare les lignes
	
	//$("#textarea").val(dataLines); // debug
	$("#textarea").val(""); // efface
	
	var lengthArray=dataLines.length; 
	//alert(lengthArray); // debug
	
	
	for (var i=0; i<lengthArray-1; i++) {
		//$("#textarea").val($("#textarea").val()+dataLines[i]+"\\n");  // debug
		
		data=dataLines[i].split(',');
		datatime=data[0].split(' ');
		//$("#textarea").val($("#textarea").val()+datatime+ data[1]+"\\n");  // debug
		
		dataLines[i]='{ "recid": "'+i.toString()+'", "date": "'+datatime[0]+'", "heure": "'+datatime[1]+'", "TBal": "'+data[1]+'","TPan": "'+data[2]+'","Diff": "'+data[3]+'","Circ": "'+data[4]+'"}';
		//$("#textarea").val($("#textarea").val()+dataLines[i]+"\\n");  // debug
	} // fin for 
	
	
	dataJSON=dataLines.toString();
	dataJSON=dataJSON.slice(0,-1); // enleve , de fin 
	dataJSON="["+dataJSON+"]"
	
	//$("#textarea").val(dataJSON); // debug
	
	
	try{
		//Some code here
		dataAjax=$.parseJSON(dataJSON); // le parser JSON est très capricieux... bien respecter formatage attendu
	}
	catch(e)
	{
		//Handle errors here
		alert("erreur JSON")
	}
	
	//$("#textarea").append(dataAjax); // debug

	w2ui['grid'].clear(); // utiliser le nom du tableau pas du div
	
	w2ui['grid'].add(dataAjax); // datIn est un string JSON qu'il faut convertir en array

} // fin fonction de gestion de la reponse AJAX 



""")
	
	return manageReponseAjaxServeur
	

#==== fonction utiles ====

def nodesFiles(): # fonction renvoyant liste des fichiers au format attendu par w2sidebar
	
	# { id: 'level-1-1', text: 'Level 1.1', icon: 'fa-home' },
	
	out="" # str renvoyé
	
	files=listfiles(serverDir)

	if files:
		for filename in files[:-1]:
			print filename
			
			out=out+"{ id: '"+filename+"', text: '"+filename+"', img: 'icon-page' },\n"
		
		filename=files[-1]
		out=out+"{ id: '"+filename+"', text: '"+filename+"', img: 'icon-page' }\n" # derniere ligne sans virgule
	
	print out # debug
	
	return out
	

def dataFromFile(filepathnameIn):
	
	dataOut=""
	
	#filepath=""
	#filename="testdata.txt"
	
	#print filepath+filename
	
	print filepathnameIn
	
	"""
	filedata=open(filepath+filename, 'r') # ouvre fichier en lecture
	filelines=filedata.readlines()
	filedata.close() # ferme fichier
	
	dataOut=str(filelines)[1:-1] # enlève les [ ] de début et de fin de la chaine - la conversion str de la list ajoute les ,
	"""
	
	filedata=open(filepathnameIn, 'r') # ouvre fichier en lecture
	filecontent=filedata.read()
	filedata.close() # ferme fichier
	
	print filecontent
	filecontent=filecontent.replace("\n", "\\n") # pour support javascript
	
	return filecontent

def dataJSONFromFile(filepathnameIn):
	
	dataOut=""
	
	#filepath=""
	#filename="testdata.txt"
	
	print filepathnameIn
	
	filedata=open(filepathnameIn, 'r') # ouvre fichier en lecture
	filelines=filedata.readlines()
	filedata.close() # ferme fichier
	
	#print filelines # debug
	
	# line to JSON : 2014-07-27 23:59:00,236\n ==> { recid: 1, date: '06/10/2014', heure: "12:05:32", val1: '235'},
	for index,line in enumerate(filelines[:-1]): # défile les lignes sauf la dernière avec index
		
		dataOut=dataOut+lineToJSON(index+1,line)+"," 
		
	# dernière ligne
	dataOut=dataOut+lineToJSON(len(filelines),filelines[-1]) # sans ,
	
	#print dataOut # debug
	
	return dataOut
	

def lineToJSON(indexIn,lineIn):
	fields=lineIn.split(",")
	#print fields
	datefield,heurefield=fields[0].split(' ')
	tbalfield=fields[1]
	tpanfield=fields[2]
	difffield=fields[3]
	circfield=fields[4][:-2] # enlève le saut de ligne

	#print datefield, heurefield, val1field
	
	dataline=(
	'{ "recid": "'+str(indexIn)
	+'", "date": "'+datefield
	+'", "heure": "'+heurefield
	+'", "TBal": "'+tbalfield
	+'", "TPan": "'+tpanfield
	+'", "Diff": "'+difffield
	+'", "Circ": "'+circfield
	+'"}')
	
	print dataline
	
	# la syntaxe JSON est très capricieuse et doit être respectée ++ 
	# encadrer par des ' ' et mettre des " " pour tous les éléments... 
	# ne pas mettre de saut de ligne
	# encadre plusieurs { .. } par des [ ]
	
	return dataline

#--- obligatoire pour lancement du code -- 
if __name__=="__main__": # pour rendre le code executable 
	setup() # appelle la fonction setup
	while not noLoop: loop() # appelle fonction loop sans fin
