// This code generates a "Raw Searcher" to handle search queries. The Raw 
// Searcher requires you to handle and draw the search results manually.
google.load('search', '1');

var selectedArea = null;
var newsSearch;

function searchComplete() {
    // Check that we got results
    //document.getElementById('content').innerHTML = '';
    
    if (newsSearch.results && newsSearch.results.length > 0) {
        for (var i = 0; i < newsSearch.results.length; i++) {
            // Create HTML elements for search results
            var p = document.createElement('p');
            var a = document.createElement('a');
            //alert(p);
            a.href=newsSearch.results[i].unescapedUrl;
            a.innerHTML = newsSearch.results[i].title;
            a.target="_blank";
            // Append search results to the HTML nodes
            p.appendChild(a);
            //document.body.appendChild(p);
            $("#results").append(p);
        }
    }

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
            //#raw
            $("#results").html('');
            //#end raw
            for (var i = 0; i < temp.length; i++) {
                //#raw
                $("#results").append(temp[i] + "<br />");
                //#end raw
                
                // Create a News Search instance.
                newsSearch = new google.search.NewsSearch();

                // Set searchComplete as the callback function when a search is 
                // complete.  The newsSearch object will have results in it.
                newsSearch.setSearchCompleteCallback(this, searchComplete, null);
                newsSearch.setResultSetSize(8)
                // Specify search quer(ies)
                newsSearch.execute(temp[i]);
                //searchComplete();
                // Include the required Google branding
                //google.search.Search.getBranding('branding');
            }
            google.search.Search.getBranding('branding');
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
