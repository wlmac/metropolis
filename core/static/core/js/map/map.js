// const floor = document.getElementById("floor").checked;
  // console.log(floor+" - floor");
  // console.log("hello world");

    
  

  mapboxgl.accessToken =
    "pk.eyJ1IjoibmlraXN1IiwiYSI6ImNrc3A3c2FieTAwM3kybnA3anNjY2c3MXMifQ.T_8vAyTc4PMuGUC23vIOhA";
    const map = new mapboxgl.Map({
      container: 'map', // container ID
      style: 'mapbox://styles/mapbox/streets-v11', // style URL
      center: [-79.46155348420591,43.753374130758445], // starting position [lng, lat]
      zoom: 19 // starting zoom
    });
    
    map.on('load', () => {
      map.addSource('floorOne', {
        'type': 'image',
        'url': '../static/core/img/FloorOne.png',
        "coordinates": [
            [-79.462739, 43.754109],//TL
            [-79.46076, 43.754109],//TR
            [-79.46079, 43.752709],//BR
            [-79.462759, 43.752719] //BL
        ]
      });

      map.addSource('floorTwo', {
        'type': 'image',
        'url': '../static/core/img/FloorTwo.png',
        "coordinates": [
            [-79.462559, 43.754059],//TL
            [-79.46067 , 43.754060],//TR
            [-79.46069 , 43.752730],//BR
            [-79.462569, 43.752739] //BL
        ]
      });

      map.addControl(
        new mapboxgl.GeolocateControl({
          positionOptions: {
          enableHighAccuracy: true
          },
          // When active the map will receive updates to the device's location as it changes.
          trackUserLocation: true,
          // Draw an arrow next to the location dot to indicate which direction the device is heading.
          showUserHeading: true
        })
      );
      
      map.addLayer({
            'id': 'floorOne',
            'source': 'floorOne',
            'type': 'raster',
            'layout': {
                // Make the layer visible by default.
                'visibility': 'visible'
            },
        });

        map.addLayer({
            'id': 'floorTwo',
            'source': 'floorTwo',
            'type': 'raster',
            'layout': {
                // Make the layer visible by default.
                'visibility': 'visible'
            },
        });

        var checkbox = document.querySelector("input[name=checkbox]");
        var floor = false; 

        checkbox.addEventListener('change', function() {
        if (this.checked) {
            console.log("Checkbox is checked..");
            map.setLayoutProperty('floorTwo', 'visibility', 'visible');
            map.setLayoutProperty('floorOne', 'visibility', 'none');
        } else {
            console.log("Checkbox is not checked..");
            map.setLayoutProperty('floorOne', 'visibility', 'visible');
            map.setLayoutProperty('floorTwo', 'visibility', 'none');
        }
        });

        
        

      });

   