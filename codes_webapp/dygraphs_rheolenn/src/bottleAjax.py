@route('/ajax/<param>') # la meme chaine a mettre dans code JS initial requete AJAX
def bottleReponseAjax(param):
	return reponseAJAX(param)
