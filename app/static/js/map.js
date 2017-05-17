
    /* global $ */
      var poly;
      var map;
      var infoWindow;
      var outerCoords= [];
      var innerCoords= [];
      var innerCoords2=[];
      var markers=[];
      var path = [];
      var polygon;
      
      var i = 0;
      
      $(window).on('load',function(){
        $('#modal1').show();
        
        // Hides the modal when the close button is clicked     
        $(".accept").click(function() {
           $('.modal').hide();
        });
        
        // Accepts and records the outer bounds of the search space
        $('#outerSelected').click(function(){
          $('#navigable').toggleClass('active');
          $('#unnavigable').toggleClass('active');
          
          $('#modal2').show();
          $('#outerSelected').hide();
          $('.navigator').show()
        })
        
        // Accepts and records the inner bounds of the search space
        $('#done').click(function(){
          $('#navigable').toggleClass('active');
          $('#unnavigable').toggleClass('active');
        })
        
        $('#add').click(function(){
          //Initialize another innercoords list
          i++
        })
        
    // Hides the modal when the screen is clicked        
        $(window).on('click', function(event) {
        if (event.target == $('.modal')) {
            $('.modal').hide();
            }
        });
      });

      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 14,
          center: {lat: 18.0078, lng: -76.8654},  // Center the map on Kingston, Jamaica.
          mapTypeId: 'terrain'
        });

        poly = new google.maps.Polyline({map: map, path: [], strokeColor: '#11b200', strokeOpacity: 1.0, strokeWeight: 1});
        /////////////////////////////////   Button Listeners    /////////////////////////////////////////////////////
        
        $('#unnavigable').click(function(){
          $('#navigable').toggleClass('active');
          $('#unnavigable').toggleClass('active');
        });
        
        $('#navigable').click(function(){
          $('#unnavigable').toggleClass('active');
          $('#navigable').toggleClass('active');
        });
        
        
        google.maps.Map.prototype.clearMarkers = function() {
          for(var i=0; i < markers.length; i++){
              markers[i].setMap(null);
          }
          markers = new Array();
        };
        map.addListener('click', addLatLng);
        //poly.addListener('bounds_changed', showNewRect);
        ///////////////////////////////////////////////////////////////////////////////////////////////////////////
      };

      
      // Handles click events on a map, and adds a new point to the Polyline.
      function addLatLng(event) {
        // var path = poly.getPath();
        //console.log(path.getArray().toString());  this converts the paths to string. Useful for python config.
        
        if ($('#navigable').hasClass('active')) {
          
          var c = {'lat': event.latLng.lat(), 'lng': event.latLng.lng()}
           
          outerCoords.push(c);
          console.log("outerCoords");
          console.log(c);
        
        } else if($('#unnavigable').hasClass('active') && i==0) {
          
          // innerCoords.push(event.latLng);
          
          c = {'lat': event.latLng.lat(), 'lng': event.latLng.lng()};
           
          innerCoords.push(c);
          console.log("innerCoords");
          console.log(c);
        } else if($('#unnavigable').hasClass('active') && i==1) {
          c = {'lat': event.latLng.lat(), 'lng': event.latLng.lng()};
           
          innerCoords2.push(c);
          console.log("innerCoords2");
          console.log(c);
        } else {
          c = {'lat': event.latLng.lat(), 'lng': event.latLng.lng()};
           
          innerCoords3.push(c);
          console.log("innerCoords3");
          console.log(c);
        }
        
        // Add a new marker at the new plotted point on the polyline.
        var marker = new google.maps.Marker({
          position: event.latLng,
          title: '#' + poly.getPath().getLength(),
          map: map,
          draggable: true,
        });
        markers.push(marker);
      }
      
      function showNewRect(event) {
        console.log("here");
        var ne = poly.getBounds().getNorthEast();
        var sw = poly.getBounds().getSouthWest();

        var contentString = '<b>Rectangle moved.</b><br>' +
            'New north-east corner: ' + ne.lat() + ', ' + ne.lng() + '<br>' +
            'New south-west corner: ' + sw.lat() + ', ' + sw.lng();

        // Set the info window's content and position.
        infoWindow.setContent(contentString);
        infoWindow.setPosition(ne);

        infoWindow.open(map);
      }
      
      
      
      // map.data.setStyle({
      //     editable: true,
      //     fillColor: '#55d157',
      //     fillOpacity: 0.35
      //   });
        
     $('#done').click(function() {
          //polygon.setMap(map);
          
        //   polygon.getPaths().forEach(function(path, index){

        //   google.maps.event.addListener(path, 'insert_at', function(){
        //     // New point
        //   });
        
        //   google.maps.event.addListener(path, 'remove_at', function(){
        //     // Point was removed
        //   });
        
        //   google.maps.event.addListener(path, 'set_at', function(){
        //     // Point was moved
            
        //   });
        
        // });
        
        // google.maps.event.addListener(polygon, 'dragend', function(){
        //   // Polygon was dragged
        // });
          if (innerCoords.length > 0 && innerCoords2.length > 0){
            google.maps.Map.prototype.clearMarkers;
              map.data.add({geometry: new google.maps.Data.Polygon([outerCoords,innerCoords, innerCoords2])});
              //sends request to backend
              $.ajax({
                  type: 'POST',
                  url: '/api/processing',
                  data: JSON.stringify ({outer: outerCoords, inner: innerCoords, inner2: innerCoords2}),
                  success: function(data) { initAnimation(data) },
                  contentType: "application/json",
                  dataType: 'json'
              });
    
               // resets polygon
               
          } else if (innerCoords2.length == 0 && innerCoords.length > 0){
            google.maps.Map.prototype.clearMarkers;
            map.data.add({geometry: new google.maps.Data.Polygon([outerCoords,innerCoords])});
              //sends request to backend
              $.ajax({
                  type: 'POST',
                  url: '/api/processing',
                  data: JSON.stringify ({outer: outerCoords, inner: innerCoords}),
                  success: function(data) { alert(); },
                  contentType: "application/json",
                  dataType: 'json'
              });
          }
      });

    function initAnimation(path){
        var speed = 200; // km/h

        var delay = 100;
        startPos = path[0]
        var startPt = new google.maps.LatLng(startPos[0],startPos[1])
        map.setCenter(startPt)
        map.setZoom(30)
        var drone_icon = {
            url: "https://d30y9cdsu7xlg0.cloudfront.net/png/156824-200.png", // url
            scaledSize: new google.maps.Size(30, 30), // scaled size
            origin: new google.maps.Point(0,0), // origin
            anchor: new google.maps.Point(0, 0) // anchor
        };
        drone_marker = new google.maps.Marker({
           position: new google.maps.LatLng(startPos[0], startPos[1]),
           icon: drone_icon,
           map: map
        });

        animateMarker(map,drone_marker,path, speed,delay);
    }

    function animateMarker(map,marker, coords, km_h,delay)
    {
        var target = 0;
        var km_h = km_h || 200;
        

        function goToPoint()
        {
            var lat = marker.position.lat();
            var lng = marker.position.lng();
            var step = (km_h * 1000 * delay) / 3600000; // in meters

            var dest = new google.maps.LatLng(
            coords[target][0], coords[target][1]);

            var distance =
                google.maps.geometry.spherical.computeDistanceBetween(
            dest, marker.position); // in meters

            var numStep = distance / step;
            var i = 0;
            var deltaLat = (coords[target][0] - lat) / numStep;
            var deltaLng = (coords[target][1] - lng) / numStep;

            console.log("Lat " + lat+"" + "Lng " + lng+"");
            function moveMarker()
            {
                lat += deltaLat;
                lng += deltaLng;
                i += step;

                if (i < distance)
                {
                    marker.setPosition(new google.maps.LatLng(lat, lng));
                    setTimeout(moveMarker, delay);
                }
                else
                {
                    

                     
                    marker.setPosition(dest);
                    target++;
                    //if (target == coords.length){ target = 0; }

                    var flightPlanCoordinates=[]
                    var point1 = new google.maps.LatLng(lat,lng);
                    var point2  = new google.maps.LatLng(coords[target][0], coords[target][1]);
                    flightPlanCoordinates.push(point1);
                    flightPlanCoordinates.push(point2);     


                    var flightPath = new google.maps.Polyline({
                        path: flightPlanCoordinates,
                        geodesic: true,
                        strokeColor: '#FF0000',
                        strokeOpacity: 3.0,
                        strokeWeight: 4
                    });
                    flightPath.setMap(map);  
                    if(target< coords.length){
                        setTimeout(goToPoint, delay);
                    }else{
                        alert("All Done");
                    }
                

                }
            }
            moveMarker();
        }
        goToPoint();
    }



      
      
