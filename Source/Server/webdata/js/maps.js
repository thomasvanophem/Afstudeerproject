var selectedArea = null;
var map;
var markers = [];

var accountKey = 'C9+uvX1xxYhWjL5IUdy4GlA3UoekeDxfb9tFTMR4TKk';
var accountKeyEncoded = base64_encode(":" + accountKey);

jQuery.support.cors = true;

function setHeader(xhr) {
  //'Basic <Your Azure Marketplace Key(Remember add colon character at before the key, then use Base 64 encode it');
  xhr.setRequestHeader('Authorization', "Basic " + accountKeyEncoded);
}

function GetBing(city) {
    //Build up the URL for the request
    var requestStr = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27".concat(city, "%27&$top=10&$format=json");
    var results = [];
    
    //Return the promise from making an XMLHttpRequest to the server
    $.ajax({ 
        url: requestStr, 
        beforeSend: setHeader,
        context: this,
        type: 'GET',
        success: function(data, status) {
            results = data.d.results;
            
            if (results.length != 0) {
                $("#results").append("News for " + city + "... <br />");
                for (var i = 0; i < results.length; i++) {
                    var p = document.createElement('p');
                    var a = document.createElement('a');
                
                    a.href = results[i].Url;
                    a.innerHTML = results[i].Title;
                    a.target = "_blank";
                
                    p.appendChild(a);
                
                    $("#results").append(p);
                }

            } else {
                $("#results").append("No news for " + city + "...<br />");
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert (textStatus);
        }
    });
}
        
function base64_encode(data) {
    // http://kevin.vanzonneveld.net
    // +   original by: Tyler Akins (http://rumkin.com)
    // +   improved by: Bayron Guevara
    // +   improved by: Thunder.m
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   bugfixed by: Pellentesque Malesuada
    // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
    // +   improved by: Rafal Kukawski (http://kukawski.pl)
    // *     example 1: base64_encode('Kevin van Zonneveld');
    // *     returns 1: 'S2V2aW4gdmFuIFpvbm5ldmVsZA=='
    // mozilla has this native
    // - but breaks in 2.0.0.12!
    //if (typeof this.window['btoa'] == 'function') {
    //    return btoa(data);
    //}
    var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var o1, o2, o3, h1, h2, h3, h4, bits, i = 0, ac = 0, enc = "", tmp_arr = [];

    if (!data) {
        return data;
    }

    do { // pack three octets into four hexets
        o1 = data.charCodeAt(i++);
        o2 = data.charCodeAt(i++);
        o3 = data.charCodeAt(i++);

        bits = o1 << 16 | o2 << 8 | o3;

        h1 = bits >> 18 & 0x3f;
        h2 = bits >> 12 & 0x3f;
        h3 = bits >> 6 & 0x3f;
        h4 = bits & 0x3f;

        // use hexets to index into b64, and append result to encoded string
        tmp_arr[ac++] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
    } while (i < data.length);

    enc = tmp_arr.join('');

    var r = data.length % 3;

    return (r ? enc.slice(0, r - 3) : enc) + '==='.slice(r || 3);
}

// Converts radians to degrees
Math.degrees = function(radians) {
    return radians * 180.0 / Math.PI;
}

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

            $("#results").html('');
            
            for (var i = 0; i < temp.length; i++) {
                
                //$("#results").append(temp[i] + "<br />");
                
                //GetBing(temp[i][0]);
                
                var latlon = new google.maps.LatLng(Math.degrees(temp[i][1]), Math.degrees(temp[i][2]));
                var marker = new google.maps.Marker({
                                                    position: latlon,
                                                    map: map,
                                                    title: temp[i][0]
                                                    });
                markers.push(marker);
            }
            //GetBing();
        }
    }

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

function initialize() {
    var mapOptions = {
        center: new google.maps.LatLng(52.3740300, 4.8896900),
        zoom: 8
    };

    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    var selection
    var selectionOptions = {
      fillColor: '#D3E6D3',
      fillOpacity: 0.5,
      map: map,
      center: new google.maps.LatLng(52.0833333, 5.1333333),
      radius: 1000.0 * 1000.0
    };
    // Add the circle for this city to the map.
    selection = new google.maps.Circle(selectionOptions);
    console.log("Radius: "+selection.radius / 1000.0+" KM");
    console.log("Lat: "+selection.center.lat()+" Lon: "+selection.center.lng());
    loadXMLDoc(selection.radius / 1000.0, selection.center.lat(), selection.center.lng());

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

    $('#map-canvas').on('mouseup', function() {
        drawingManager.setDrawingMode(google.maps.drawing.OverlayType.CIRCLE);
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
