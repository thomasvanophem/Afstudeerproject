var selectedArea = null;
var map;
var markers = [];

// Converts radians to degrees
Math.degrees = function(radians) {
    return radians * 180.0 / Math.PI;
}

function RequestData(radius, x, y) {
    var xmlhttp;
    
    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            var temp = JSON.parse(xmlhttp.responseText);
            var div = document.getElementById("results");

            $("#results").html('');
            
            if temp.length == 0:
                $("#results").append("No cities found...");
            
            for (var i = 0; i < temp.length; i++) {
                // For each city search for news and add a marker to the map.         
                GetBing(temp[i][0]);
                
                var latlon = new google.maps.LatLng(Math.degrees(temp[i][1]), Math.degrees(temp[i][2]));
                var marker = new google.maps.Marker({
                                                    position: latlon,
                                                    map: map,
                                                    title: temp[i][0],
                                                    icon: 'img/marker.png'
                                                    });
                markers.push(marker);
            }
        }
    }

    //Sent the request to the server.
    xmlhttp.open("POST","",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("lat="+x+"&lon="+y+"&radius="+radius);
} 

// Remove all the markers from the map.
function remove_markers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }

    markers = [];
}

// Initialize the map
function initialize() {
    // Where do we center the map, and what zoom level do we want?
    var mapOptions = {
        center: new google.maps.LatLng(52.3740300, 4.8896900),
        zoom: 8
    };

    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    /*
    //RESEARCH
    var selection
    var selectionOptions = {
      fillColor: '#D3E6D3',
      fillOpacity: 0.5,
      map: map,
      center: new google.maps.LatLng(52.0833333, 5.1333333),
      radius: 500.0 * 1000.0
    };
    // Add the circle for this city to the map.
    selection = new google.maps.Circle(selectionOptions);
    console.log("Radius: "+selection.radius / 1000.0+" KM");
    console.log("Lat: "+selection.center.lat()+" Lon: "+selection.center.lng());
    loadXMLDoc(selection.radius / 1000.0, selection.center.lat(), selection.center.lng());
    */
    var drawingManager = new google.maps.drawing.DrawingManager({
                                                                drawingMode: google.maps.drawing.OverlayType.CIRCLE,
                                                                drawingControl: false,
                                                                markerOptions: {
                                                                    icon: '/img/marker.png'
                                                                },
                                                                circleOptions: {
                                                                    fillColor: '#D3E6D3',
                                                                    fillOpacity: 0.5,
                                                                    strokeWeight: 1,
                                                                    clickable: false,
                                                                    editable: true,
                                                                    zIndex: 1
                                                                }
                                                                });
                                                                                                        
    drawingManager.setMap(map);

    // Tell the map what to do on mouse down
    $('#map-canvas').on('mousedown', function(e) {
        if (e.button == 0) {
            drawingManager.setDrawingMode(google.maps.drawing.OverlayType.CIRCLE);

            if (selectedArea) {
                remove_markers();
                selectedArea.setMap(null);
                google.maps.event.clearInstanceListeners(selectedArea);
            }

            selectedArea = null;
        } else if (e.button == 2) {
            drawingManager.setDrawingMode(google.maps.drawing.OverlayType.MARKER);
        }
    });

    // And on mouse up...
    $('#map-canvas').on('mouseup', function() {
        drawingManager.setDrawingMode(google.maps.drawing.OverlayType.CIRCLE);
    });

    google.maps.event.addListener(drawingManager, 'circlecomplete', function(circle) {
        selectedArea = circle;
    });
    
    // Call RequestData to make the request to the server
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
        if (event.type == google.maps.drawing.OverlayType.CIRCLE) {
            var center = event.overlay.getCenter();
            var radius = event.overlay.getRadius();
            //DEBUG
            console.log("Radius: "+radius/1000.0+" KM");
            console.log("Lat: "+center.lat()+" Lon: "+center.lng());
            //Request to server
            RequestData(radius / 1000.0, center.lat(), center.lng());
        }
    });
}

google.maps.event.addDomListener(window, 'load', initialize);
