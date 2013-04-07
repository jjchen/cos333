var map;
var idled = false;
var oms;
var image = '{% static "frontend/paw_print.png" %}';
var flower = '{% static "frontend/small_flower.png" %}';

function initialize() {
   var center = new google.maps.LatLng(40.344725, -74.655629);

   var mapOptions = {
      center: center,
      zoom: 17,
      mapTypeId: google.maps.MapTypeId.ROADMAP
   };
   map = new google.maps.Map(document.getElementById("map-canvas"),
      mapOptions);
   oms = new OverlappingMarkerSpiderfier(map, {
      keepSpiderfied: true
   });

   var iw = new google.maps.InfoWindow();
   oms.addListener('click', function (marker) {
      iw.setContent(marker.desc);
      iw.open(map, marker);
   });

   oms.addListener('spiderfy', function (markers) {
      iw.close();
      for (i = 0; i < markers.length; i++) {
         markers[i].setIcon(image);
      }
   });

   oms.addListener('unspiderfy', function (markers) {
      iw.close();
      for (i = 0; i < markers.length; i++) {
         markers[i].setIcon(flower);
      }
   });

   google.maps.event.addListener(map, 'idle', function () {
      if (!idled) {
         var overlapped = oms.markersNearAnyOtherMarker();
         for (i = 0; i < overlapped.length; i++) {
            overlapped[i].setIcon(flower);
         }
      }
      idled = true;
   });

   {% if events_list %}
   showEventsOnMap(); 
   {% endif %}
}
google.maps.event.addDomListener(window, 'load', initialize);

function showEventsOnMap() {

   var i = 0; 
   {% for event in events_list %} 
   {% if event.lat %}
   var position = new google.maps.LatLng({{event.lat}}, {{event.lon}});

   var marker = new google.maps.Marker({
      map: map,
      position: position,
      icon: image
   });

   var contentString = '<div class="infoWindow_content">' +
      '<h3 class="infoWindow_heading">{{event.name}}</h3>' +
      '<div id="infoWindow_body">' +
      '<p>Time: 10:00pm April 2, 2013</p>' +
      '<p>Location: {{event.location}}</p>' +
      '</div>' +
      '</div>';

   marker.desc = contentString;

   oms.addMarker(marker); 
   {% endif %} 
   {% endfor %}
}


function showContent(id) {
   //alert(id);
   var elem = document.getElementById('content_wrapper');
   for (i = 0; i < elem.children.length; i++) {
      if (elem.children[i].id != id) {
         elem.children[i].className = 'hidden';
      } else {
         elem.children[i].className = (elem.children[i].className == 'hidden') ? 'visible' : 'hidden';
      }
   }
}