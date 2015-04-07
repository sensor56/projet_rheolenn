
function manageReponseAjaxServeur(dataIn){
	
	//dataIn=parseInt(dataIn); 
	$("#textarea").append("ajax : "+ dataIn+"\n"); 
	$("#textarea").get(0).setSelectionRange($("#textarea").get(0).selectionEnd-1,$("#textarea").get(0).selectionEnd-1); // se place en derniere ligne -1 pour avant saut de ligne 

} // fin fonction de gestion de la reponse AJAX 

