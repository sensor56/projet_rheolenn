var dygraphs = null; // variable globale pour objet graphique Dygraphs

$(document).ready(function(){
	
	// initialisation du graphique Dygraphs
	dygraphs = new Dygraph( // creation de l'objet graphique
		document.getElementById("graphDiv"),  // div conteneur - utiliser le meme nom ++ 
		
		"Date,Temperature\n" +                // serie de donnees de test
		"2008-05-07,75\n" +
		"2008-05-08,70\n" +
		"2008-05-09,80\n" +
		"2008-05-10,55\n" + 
		"2008-05-11,82\n" + 
		"2008-05-12,76\n" + 
		"2008-05-13,90\n" + 
		"2008-05-14,95\n" , // fin serie de donnees 
		
		{ } // les options du graphique - aucune ici
		
	); // fin new Dygraph

	
}); // fin function + fin ready + fin $
