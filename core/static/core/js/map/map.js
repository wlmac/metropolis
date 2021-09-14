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
        coordinates: [-79.46242786599252, 43.75383226893149],
      },
      properties: {
        title: "Portable 1",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4624674664498, 43.75395384426233],
      },
      properties: {
        title: "Portable 2",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46221201860781, 43.75315570812597],
      },
      properties: {
        title: "Portable 3",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46218231537334, 43.75304127913833],
      },
      properties: {
        title: "Portable 4",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46240211926877, 43.75312710090293],
      },
      properties: {
        title: "Portable 5",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46237835668141, 43.75301696295375],
      },
      properties: {
        title: "Portable 6",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46255657608708, 43.75325583331394],
      },
      properties: {
        title: "Portable 7",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46232772000198, 43.75333912391008],
      },
      properties: {
        title: "119",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4623469764093, 43.75344730771101],
      },
      properties: {
        title: "121",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46236623281662, 43.75354003652805],
      },
      properties: {
        title: "123",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46238762882443, 43.75362735603221],
      },
      properties: {
        title: "125",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4621936537785, 43.75359207291845],
      },
      properties: {
        title: "small gym (124)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46209095294103, 43.753463025387845],
      },
      properties: {
        title: "fitness centre (124c)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46208025493297, 43.75362375520521],
      },
      properties: {
        title: "team change room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.461995740702, 43.75365930116354],
      },
      properties: {
        title: "girls change room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46194546008348, 43.7534962532234],
      },
      properties: {
        title: "boys change room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46190908686992, 43.75362993711252],
      },
      properties: {
        title: "equipment office (127D)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46187592305769, 43.75352329912107],
      },
      properties: {
        title: "gym office (127E)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46190908686992, 43.75362993711252],
      },
      properties: {
        title: "gym office (127A)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46172829042908, 43.7536059822186],
      },
      properties: {
        title: "gym office (127A)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.462114731088, 43.75378701797311],
      },
      properties: {
        title: "118T",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4621386073844, 43.753754877161555],
      },
      properties: {
        title: "118C",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4619486823008, 43.753779178752524],
      },
      properties: {
        title: "118E",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46180040894147, 43.75381567830766],
      },
      properties: {
        title: "114",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46166541489782, 43.75378851914769],
      },
      properties: {
        title: "music office",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46143822537765, 43.753929497447075],
      },
      properties: {
        title: "dance room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46119197175985, 43.753727055891716],
      },
      properties: {
        title: "cafeteria/cafetorium",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46104935599587, 43.75332157069508],
      },
      properties: {
        title: "library (134)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46105650992905, 43.75321064103045],
      },
      properties: {
        title: "special education resource",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4610222400155, 43.7532166058547],
      },
      properties: {
        title: "SAC room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46099168611664, 43.75322286891952],
      },
      properties: {
        title: "cyw",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46096278377965, 43.753224658366946],
      },
      properties: {
        title: "library office",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46098319927927, 43.75356356662772],
      },
      properties: {
        title: "staff room",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46117219109146, 43.75347458092048],
      },
      properties: {
        title: "student services",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4613063231389, 43.75351264347452],
      },
      properties: {
        title: "Main Office (116)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4612294356992, 43.75326779180898],
      },
      properties: {
        title: "108b",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46122508822467, 43.75321557131289],
      },
      properties: {
        title: "108a",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46127098499517, 43.7531449767591],
      },
      properties: {
        title: "106",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46123918940455, 43.75303129706333],
      },
      properties: {
        title: "104",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46121578443991, 43.75289734900633],
      },
      properties: {
        title: "102",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46135081308083, 43.75288499455911],
      },
      properties: {
        title: "101",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46138502033672, 43.75302804590089],
      },
      properties: {
        title: "103",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46138592052752, 43.75312232955255],
      },
      properties: {
        title: "Science Office (105)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4614352157135, 43.75323058218939],
      },
      properties: {
        title: "107",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46146178469338, 43.75338567006156],
      },
      properties: {
        title: "109",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46163268826237, 43.75340901084962],
      },
      properties: {
        title: "111",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46176978970212, 43.753393465274826],
      },
      properties: {
        title: "113",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46185667774388, 43.753374792510044],
      },
      properties: {
        title: "business office",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46192771832759, 43.753363879308466],
      },
      properties: {
        title: "117",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46238618462642, 43.75362037478658],
      },
      properties: {
        title: "231",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46236885877464, 43.753539028440656],
      },
      properties: {
        title: "229",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46234978339967, 43.75344471356212],
      },
      properties: {
        title: "227",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46232887682082, 43.75336651039095],
      },
      properties: {
        title: "co-op office (226)",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46231917019374, 43.75332606043551],
      },
      properties: {
        title: "225",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4621802907584, 43.75334385841933],
      },
      properties: {
        title: "223",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46210637115912, 43.75345388207188],
      },
      properties: {
        title: "computer office (233)",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46199063829641, 43.7533665102612],
      },
      properties: {
        title: "222",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46186383479508, 43.75338215078125],
      },
      properties: {
        title: "221",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46174810193233, 43.753395094757906],
      },
      properties: {
        title: "220",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46162863575111, 43.75341073539221],
      },
      properties: {
        title: "219",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4614748233558, 43.75339024061128],
      },
      properties: {
        title: "213",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4614501076126, 43.75330386598583],
      },
      properties: {
        title: "211",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46142994769447, 43.753214875953944],
      },
      properties: {
        title: "209",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46141277443088, 43.753129121798224],
      },
      properties: {
        title: "207",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46137891242998, 43.75298455462399],
      },
      properties: {
        title: "203",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4613572591844, 43.752873451304396],
      },
      properties: {
        title: "201",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46121240644001, 43.752886395391045],
      },
      properties: {
        title: "202",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46123225915024, 43.75297204839015],
      },
      properties: {
        title: "204",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46125540572287, 43.75305942077733],
      },
      properties: {
        title: "206",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46126511235038, 43.75314895037479],
      },
      properties: {
        title: "208",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46129252974201, 43.75322948124841],
      },
      properties: {
        title: "210",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46131119633266, 43.75331469592737],
      },
      properties: {
        title: "212",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46133229040255, 43.753404171796234],
      },
      properties: {
        title: "214",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46151895631627, 43.753604263599016],
      },
      properties: {
        title: "dark room",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4615480761975, 43.75357837573341],
      },
      properties: {
        title: "book room",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4614211433802, 43.75382646731842],
      },
      properties: {
        title: "216",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46156898277957, 43.75380273686321],
      },
      properties: {
        title: "215",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46143831664382, 43.75390790585365],
      },
      properties: {
        title: "218",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46159412840285, 43.75393149645012],
      },
      properties: {
        title: "217",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46137493956924, 43.753442172247134],
      },
      properties: {
        title: "modern languages office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46138050236257, 43.75346800307909],
      },
      properties: {
        title: "history office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46137931033562, 43.75348694568186],
      },
      properties: {
        title: "geography office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46139440934593, 43.75354233841023],
      },
      properties: {
        title: "english office",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46140156150852, 43.75358739877856],
      },
      properties: {
        title: "math office (238)",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46149383054909, 43.75396687020216],
      },
      properties: {
        title: "art office (218A)",
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
});

map.addControl(geocoder);

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

  // const marker = new mapboxgl.Marker({
  //   draggable: true,
  // })
  //   .setLngLat([-79.46155348420591, 43.753374130758445])
  //   .addTo(map);

  // function onDragEnd() {
  //   const lngLat = marker.getLngLat();
  //   coordinates.style.display = "block";
  //   coordinates.innerHTML = `Longitude: ${lngLat.lng}<br />Latitude: ${lngLat.lat}`;
  // }

  // // marker.on("dragend", onDragEnd);

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

  geocoder.on("result", ({ result }) => {
    console.log(result.properties.title);
    if (result.properties.floor == 1) {
      checkbox.checked = false;
      map.setLayoutProperty("floorOne", "visibility", "visible");
      map.setLayoutProperty("floorTwo", "visibility", "none");
    } else {
      checkbox.checked = true;
      map.setLayoutProperty("floorTwo", "visibility", "visible");
      map.setLayoutProperty("floorOne", "visibility", "none");
    }
  });
});
