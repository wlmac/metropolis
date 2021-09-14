mapboxgl.accessToken = JSON.parse(
  document.getElementById("mapbox-apikey").textContent
)["apikey"];
const map = new mapboxgl.Map({
  container: "map", // container ID
  style: "mapbox://styles/nikisu/ckthu5pbc28d318oacchk9ntr", // style URL
  center: [-79.46155348420591, 43.753374130758445], // starting position [lng, lat]
  zoom: 19, // starting zoom
});
const coordinates = document.getElementById("coordinates");

const customData = {
  features: [
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46176003664733, 43.753628645506545],
      },
      properties: {
        id: "127",
        title: "large gym",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46221198886633, 43.753628887683234],
      },
      properties: {
        id: "124",
        title: "small gym",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46201786398888, 43.75369500188763],
      },
      properties: {
        id: "girls change room",
        title: "girls change room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46196589618921, 43.753544367952976],
      },
      properties: {
        id: "boys change room",
        title: "boys change room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46210503578186, 43.75365915976391],
      },
      properties: {
        id: "team change room",
        title: "team change room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46209900081158, 43.75347171479428],
      },
      properties: {
        id: "124c",
        title: "fitness centre",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46106695372214, 43.75376776088882],
      },
      properties: {
        id: "127A",
        title: "gym office A",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46106695372214, 43.75376776088882],
      },
      properties: {
        id: "127E",
        title: "gym office E",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4610619917512, 43.753364914490895],
      },
      properties: {
        id: "134",
        title: "library",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46122158318758, 43.75377927922907],
      },
      properties: {
        id: "135",
        title: "cafeteria",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4611944258213, 43.75351118968812],
      },
      properties: {
        id: "student services",
        title: "student services",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46105394512415, 43.75326005142254],
      },
      properties: {
        id: "sac room",
        title: "sac room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46099828928709, 43.75327046508419],
      },
      properties: {
        id: "cyw",
        title: "cyw",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46099828928709, 43.75327046508419],
      },
      properties: {
        id: "library office",
        title: "library office",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46124169975518, 43.75329008151169],
      },
      properties: {
        id: "108",
        title: "sepecial ed resource",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46133021265268, 43.75355163326401],
      },
      properties: {
        id: "116",
        title: "main office",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4614740461111, 43.75398343333141],
      },
      properties: {
        id: "dance room",
        title: "dance room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46136139333248, 43.75292947726766],
      },
      properties: {
        id: "101",
        title: "101",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46121588349342, 43.75293674265332],
      },
      properties: {
        id: "102",
        title: "102",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46139559149742, 43.753060254074676],
      },
      properties: {
        id: "103",
        title: "103",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4612480700016, 43.75306848816038],
      },
      properties: {
        id: "104",
        title: "104",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4614153727889, 43.753142352702],
      },
      properties: {
        id: "105",
        title: "science office",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4612842798233, 43.75318449177667],
      },
      properties: {
        id: "106",
        title: "106",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46144588291645, 43.753270222906025],
      },
      properties: {
        id: "107",
        title: "107",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46147873997688, 43.75342836503427],
      },
      properties: {
        id: "109",
        title: "109",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46165274828672, 43.753447254877685],
      },
      properties: {
        id: "111",
        title: "111",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4617922231555, 43.75343369293942],
      },
      properties: {
        id: "113",
        title: "113",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46187872439623, 43.753418920110306],
      },
      properties: {
        id: "115",
        title: "business office",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46199540048838, 43.75340535816562],
      },
      properties: {
        id: "117",
        title: "117",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46234039962292, 43.753376539022945],
      },
      properties: {
        id: "119",
        title: "119",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46236722171308, 43.75347558963164],
      },
      properties: {
        id: "121",
        title: "121",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46238800883293, 43.75356858565292],
      },
      properties: {
        id: "123",
        title: "123",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46241114288567, 43.753660854999985],
      },
      properties: {
        id: "125",
        title: "125",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46182776242493, 43.75385483812394],
      },
      properties: {
        id: "114",
        title: "114",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46212381124496, 43.75383376882629],
      },
      properties: {
        id: "118",
        title: "118",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46240242570639, 43.75365116793612],
      },
      properties: {
        id: "231",
        title: "231",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46239538490772, 43.753565195175526],
      },
      properties: {
        id: "229",
        title: "229",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46237158030272, 43.75347970664606],
      },
      properties: {
        id: "227",
        title: "227",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46234744042158, 43.75340390509994],
      },
      properties: {
        id: "226",
        title: "co-op office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46233838796616, 43.75336055529078],
      },
      properties: {
        id: "225",
        title: "225",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46219958364964, 43.75337629684523],
      },
      properties: {
        id: "223",
        title: "223",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46212079375984, 43.753481886241815],
      },
      properties: {
        id: "233",
        title: "computer science office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46199808269739, 43.753405600343235],
      },
      properties: {
        id: "222",
        title: "222",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46187168359755, 43.753421341885826],
      },
      properties: {
        id: "221",
        title: "221",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46175031363964, 43.753432724229434],
      },
      properties: {
        id: "220",
        title: "220",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46162827312946, 43.75344701270023],
      },
      properties: {
        id: "219",
        title: "219",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46147739887238, 43.75342884938928],
      },
      properties: {
        id: "213",
        title: "213",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46133323013783, 43.75344677052279],
      },
      properties: {
        id: "214",
        title: "214",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46145694702864, 43.75333948581914],
      },
      properties: {
        id: "211",
        title: "211",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46131143718958, 43.75335522737912],
      },
      properties: {
        id: "212",
        title: "212",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46144085377455, 43.75325254389789],
      },
      properties: {
        id: "209",
        title: "209",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46129769086838, 43.75327651953781],
      },
      properties: {
        id: "210",
        title: "210",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46141436696053, 43.75316729710038],
      },
      properties: {
        id: "207",
        title: "207",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46127321571112, 43.7531849761337],
      },
      properties: {
        id: "208",
        title: "208",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46137748658656, 43.75303313001969],
      },
      properties: {
        id: "203",
        title: "203",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46125041693449, 43.75310239320719],
      },
      properties: {
        id: "206",
        title: "206",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46123063564302, 43.75301763055415],
      },
      properties: {
        id: "204",
        title: "204",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4613479822874, 43.75291470431406],
      },
      properties: {
        id: "201",
        title: "201",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46120783686638, 43.7529321412425],
      },
      properties: {
        id: "202",
        title: "202",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46130875498056, 43.75348697196493],
      },
      properties: {
        id: "modern lang. office",
        title: "modern languages office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46131512522697, 43.75351506452293],
      },
      properties: {
        id: "history office",
        title: "history office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4613191485405, 43.7535455788382],
      },
      properties: {
        id: "geography office",
        title: "geography office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46133255958557, 43.753589170690184],
      },
      properties: {
        id: "english office",
        title: "english office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46134228259324, 43.75362791897641],
      },
      properties: {
        id: "238",
        title: "math office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46155149489641, 43.7535988577641],
      },
      properties: {
        id: "book room",
        title: "book room",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46153406053782, 43.75363276251044],
      },
      properties: {
        id: "dark room",
        title: "dark room",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46142073720694, 43.753774920059136],
      },
      properties: {
        id: "216A",
        title: "dark room A",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46157932281494, 43.753836674936764],
      },
      properties: {
        id: "215",
        title: "215",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46143213659525, 43.753852900717554],
      },
      properties: {
        id: "216",
        title: "216",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46160983294249, 43.75397301979385],
      },
      properties: {
        id: "217",
        title: "217",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46145627647638, 43.75394347439825],
      },
      properties: {
        id: "218",
        title: "218",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46150656789541, 43.75399602644422],
      },
      properties: {
        id: "218A",
        title: "art office",
        floor: 2,
      },
    },
  ],
  type: "FeatureCollection",
};

function forwardGeocoder(query) {
  const matchingFeatures = [];
  for (const feature of customData.features) {
    // Handle queries with different capitalization
    // than the source data by calling toLowerCase().
    if (feature.properties.title.toLowerCase().includes(query.toLowerCase())) {
      // Add a tree emoji as a prefix for custom
      // data results using carmen geojson format:
      // https://github.com/mapbox/carmen/blob/master/carmen-geojson.md
      feature["place_name"] = `${feature.properties.title}`;
      feature["center"] = feature.geometry.coordinates;
      matchingFeatures.push(feature);
    }
  }
  return matchingFeatures;
}

var level = false;

// Add the control to the map.
// map.addControl(
//   new MapboxGeocoder({
//     accessToken: mapboxgl.accessToken,
//     localGeocoder: forwardGeocoder,
//     localGeocoderOnly: true,
//     zoom: 19,
//     placeholder: "Search School",
//     mapboxgl: mapboxgl,
//     render: function (item) {
//       // extract the item's maki icon or use a default
//       return `<div class='geocoder-dropdown-item'>
//       <span class='geocoder-dropdown-text'>
//       ${item.properties.title}
//       </span>
//       </div>`;
//     },
//   })
// );

const geocoder = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  localGeocoder: forwardGeocoder,
  localGeocoderOnly: true,
  zoom: 19,
  placeholder: "Search School",
  mapboxgl: mapboxgl,
  render: function (item) {
    // extract the item's maki icon or use a default
    return `<div class='geocoder-dropdown-item'>
    <span class='geocoder-dropdown-text'>
    ${item.properties.title}
    </span>
    </div>`;
  },
})

map.addControl(geocoder)

map.on("load", () => {
  map.addSource("floorOne", {
    type: "image",
    url: "../static/core/img/FloorOne.jpg",
    coordinates: [
      [-79.46280231730522, 43.75418610402343], //TL
      [-79.46065948803763, 43.75418610402343], //TR
      [-79.46065948803763, 43.75267989803223], //BR
      [-79.46280231730522, 43.75267989803223], //BL
    ],
  });

  map.addSource("floorTwo", {
    type: "image",
    url: "../static/core/img/FloorTwo.jpg",
    coordinates: [
      [-79.46280231730522, 43.75418610402343], //TL
      [-79.46065948803763, 43.75418610402343], //TR
      [-79.46065948803763, 43.75267989803223], //BR
      [-79.46280231730522, 43.75267989803223], //BL
    ],
  });

  map.addControl(
    new mapboxgl.GeolocateControl({
      positionOptions: {
        enableHighAccuracy: true,
      },
      // When active the map will receive updates to the device's location as it changes.
      trackUserLocation: true,
      // Draw an arrow next to the location dot to indicate which direction the device is heading.
      showUserHeading: true,
    })
  );

  map.addLayer({
    id: "floorOne",
    source: "floorOne",
    type: "raster",
    layout: {
      // Make the layer visible by default.
      visibility: "visible",
    },
  });

  map.addLayer({
    id: "floorTwo",
    source: "floorTwo",
    type: "raster",
    layout: {
      // Make the layer visible by default.
      visibility: "none",
    },
  });

  const marker = new mapboxgl.Marker({
    draggable: true,
  })
    .setLngLat([-79.46155348420591, 43.753374130758445])
    .addTo(map);

  function onDragEnd() {
    const lngLat = marker.getLngLat();
    coordinates.style.display = "block";
    coordinates.innerHTML = `Longitude: ${lngLat.lng}<br />Latitude: ${lngLat.lat}`;
  }

  marker.on("dragend", onDragEnd);

  var checkbox = document.querySelector("input[name=checkbox]");

  checkbox.addEventListener("change", function () {
    if (this.checked) {
      console.log("Checkbox is checked..");
      map.setLayoutProperty("floorTwo", "visibility", "visible");
      map.setLayoutProperty("floorOne", "visibility", "none");
    } else {
      console.log("Checkbox is not checked..");
      map.setLayoutProperty("floorOne", "visibility", "visible");
      map.setLayoutProperty("floorTwo", "visibility", "none");
    }
  });

  geocoder.on('result', ({ result }) => {
    console.log(result.properties.title);
    if(result.properties.floor==1){
      checkbox.checked = false;
      map.setLayoutProperty("floorOne", "visibility", "visible");
      map.setLayoutProperty("floorTwo", "visibility", "none");
    }else{
      checkbox.checked = true;
      map.setLayoutProperty("floorTwo", "visibility", "visible");
      map.setLayoutProperty("floorOne", "visibility", "none");        
    }
    
  });
});
