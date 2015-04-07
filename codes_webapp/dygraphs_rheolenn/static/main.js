$(document).ready(function(){
	
		$('#sidebarDiv').w2sidebar({ // integre le sidebar dans le div dedie + parametrage du sidebar
		name: 'sidebard',
		img: null,
		nodes: [ 
			{ id: 'level-1', text: 'Level 1', img: 'icon-folder', expanded: true, group: true,
			  nodes: [ { id: 'level-1-1', text: 'Level 1.1', icon: 'fa-home' },
					   { id: 'level-1-2', text: 'Level 1.2', icon: 'fa-star' },
					   { id: 'level-1-3', text: 'Level 1.3', icon: 'fa-check' }
					 ]
			},
			{ id: 'level-2', text: 'Level 2', img: 'icon-folder', expanded: true, group: true,
			  nodes: [ { id: 'level-2-1', text: 'Level 2.1', img: 'icon-folder', 
						 nodes: [
						   { id: 'level-2-1-1', text: 'Level 2.1.1', img: 'icon-page' },
						   { id: 'level-2-1-2', text: 'Level 2.1.2', img: 'icon-page' },
						   { id: 'level-2-1-3', text: 'Level 2.1.3', img: 'icon-page' }
					 ]},
					   { id: 'level-2-2', text: 'Level 2.2', img: 'icon-page' },
					   { id: 'level-2-3', text: 'Level 2.3', img: 'icon-page' }
					 ]
			},
			{ id: 'level-3', text: 'Level 3', img: 'icon-folder', expanded: true, group: true,
			  nodes: [ { id: 'level-3-1', text: 'Level 3.1', img: 'icon-page' },
					   { id: 'level-3-2', text: 'Level 3.2', img: 'icon-page' },
					   { id: 'level-3-3', text: 'Level 3.3', img: 'icon-page' }
					 ]
			}
		], // fin nodes
		
		onClick: function (event) {
			alert('id: ' + event.target);
		} // fin onclick
		
	}); // w2sidebar

	
}); // fin function + fin ready + fin $