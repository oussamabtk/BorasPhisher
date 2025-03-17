var map = L.map('map', {
    zoomControl: false // Désactiver les boutons de zoom par défaut
}).setView([48.9041, 2.4846], 11); // Paris

// Fond de carte bleu avec noms de villes et rues (CartoDB Positron Labels)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: 'Apple maps'
}).addTo(map);

// Créer une icône de téléphone avec une bordure
var telephoneIcon = L.divIcon({
    className: 'phone-icon', // Classe CSS pour la bordure
    html: '<img src="static/img/online-sourcelist__2x.png" width="40" height="40" />', // Image de l'icône
    iconSize: [40, 40], // Taille de l'icône
    iconAnchor: [16, 32], // Ancrage de l'icône
    popupAnchor: [0, -32] // Position de la popup par rapport à l'icône
});
// .bindPopup("<b>Votre Iphone</b>").openPopup()
// Ajouter le marqueur avec l'icône de téléphone et une popup
L.marker([48.9041, 2.4846], { icon: telephoneIcon }).addTo(map);

// Ajouter les boutons de zoom personnalisés et les positionner en bas à droite
L.control.zoom({
    position: 'bottomright'
}).addTo(map);

// <!------------------- boussel ------------------------------------->

// Créer un contrôle personnalisé (div)
var CustomControl = L.Control.extend({
    options: { position: 'bottomright' }, // Position du div sur la carte
    
    onAdd: function(map) {
        var div = L.DomUtil.create('div', 'custom-div custom-control');
        div.innerHTML = "N";
        return div;
    }
});

// Ajouter le div personnalisé à la carte
map.addControl(new CustomControl());


// /////////////////////// popup //////////////////////////////////////////

setTimeout(() => {
    document.getElementById("popup").style.display = "block";
}, 5000);
