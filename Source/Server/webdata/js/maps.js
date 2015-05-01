var selectedArea = null;
var Bing = require('node-bing-api')({ accKey: "C9+uvX1xxYhWjL5IUdy4GlA3UoekeDxfb9tFTMR4TKk" });

function loadXMLDoc(radius, x, y) {
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
            //#raw
            $("#results").html('');
            //#end raw
            for (var i = 0; i < temp.length; i++) {
                //#raw
                $("#results").append(temp[i] + "<br />");
                //#end raw
                
               
            }
            
            Bing.news("xbox", function(error, res, body){
            console.log(body);
          },
          {
            top: 10,  // Number of results (max 50)
            skip: 3,   // Skip first 3 results
            newssortby: "Date" //Choices are Date, Relevance
            newscategory: "rt_Business" //Choices are rt_Business,rt_Entertainment,rt_Health,rt_Politics,rt_Sports,rt_US,rt_World,rt_ScienceAndTechnology
          });
        }
    }

    xmlhttp.open("POST","",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("lat="+x+"&lon="+y+"&radius="+radius);
} 

function initialize() {
    var mapOptions = {
        center: new google.maps.LatLng(52.3740300, 4.8896900),
        zoom: 8
    };

    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    var drawingManager = new google.maps.drawing.DrawingManager({
                                                                                                        drawingMode: google.maps.drawing.OverlayType.CIRCLE,
                                                                                                        drawingControl: false,
                                                                                                        markerOptions: {
                                                                                                            icon: 'images/beachflag.png'
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
    //#raw
    $('#map-canvas').on('mousedown', function() {
    //#end raw
        if ( selectedArea ) {
            selectedArea.setMap(null);
            google.maps.event.clearInstanceListeners(selectedArea);
        }

        selectedArea = null;
    });

    google.maps.event.addListener(drawingManager, 'circlecomplete', function(circle) {
        selectedArea = circle;
    });
    
    google.maps.event.addListener(drawingManager, 'overlaycomplete', function(event) {
            if (event.type == google.maps.drawing.OverlayType.CIRCLE) {
                var center = event.overlay.getCenter();
                var radius = event.overlay.getRadius();
                //DEBUG
                console.log("Radius: "+radius/1000.0+" KM");
                console.log("Lat: "+center.lat()+" Lon: "+center.lng());
                //Request to server
                loadXMLDoc(radius / 1000.0, center.lat(), center.lng());
            }
        });
}

google.maps.event.addDomListener(window, 'load', initialize);
