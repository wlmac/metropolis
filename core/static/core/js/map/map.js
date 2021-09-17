mapboxgl.accessToken = JSON.parse(
  document.getElementById("mapbox-apikey").textContent
)["apikey"];
const map = new mapboxgl.Map({
  container: "map", // container ID
  style: "mapbox://styles/nikisu/cktk76xy90rgm17s7q7pg0g55", // style URL
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
        coordinates: [-79.46243325527307, 43.753970965485735],
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
        coordinates: [-79.46221099031513, 43.75317237412631],
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
        coordinates: [-79.4624108175995, 43.75314428115445],
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
        coordinates: [-79.46218818873812, 43.75305128362666],
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
        coordinates: [-79.46238399545628, 43.753030941531875],
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
        coordinates: [-79.46256102100658, 43.75326634251712],
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
        coordinates: [-79.462327663467, 43.75335158721401],
      },
      properties: {
        title: "Room 119",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46234644222046, 43.753461051808415],
      },
      properties: {
        title: "Room 121",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46236521768313, 43.75354726659225],
      },
      properties: {
        title: "Room 123",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46238265202406, 43.75363735643279],
      },
      properties: {
        title: "Room 125",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.462198032334, 43.75360889118667],
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
        coordinates: [-79.46207609586855, 43.75347184182684],
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
        coordinates: [-79.46208442599088, 43.75363465159106],
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
        coordinates: [-79.46199855338851, 43.753670911751186],
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
        coordinates: [-79.46195099685673, 43.753506785659],
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
        coordinates: [-79.46193094840253, 43.75359351676818],
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
        coordinates: [-79.46188333944669, 43.75353345567834],
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
        coordinates: [-79.46191351470047, 43.75364049932426],
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
        coordinates: [-79.46172911873167, 43.75361606821852],
      },
      properties: {
        title: "large gym (127)",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4621022029668, 43.75382222066108],
      },
      properties: {
        title: "Room 118T",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46215856297853, 43.753759532291014],
      },
      properties: {
        title: "Room 118C",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46195278569445, 43.75379119907919],
      },
      properties: {
        title: "Room 118E",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4618069554343, 43.75382092588782],
      },
      properties: {
        title: "Room 114",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46167722609954, 43.7537957223808],
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
        coordinates: [-79.46145355825836, 43.753934020553146],
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
        coordinates: [-79.46121179888955, 43.75373700003314],
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
        coordinates: [-79.46105544571898, 43.75333204884339],
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
        coordinates: [-79.46107005200406, 43.75322380678202],
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
        coordinates: [-79.46104008434995, 43.753229743456245],
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
        coordinates: [-79.46100721719883, 43.75323148904425],
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
        coordinates: [-79.46098063358639, 43.753235329484454],
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
        coordinates: [-79.46100511477736, 43.75357005485046],
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
        coordinates: [-79.4611868324436, 43.75348515432293],
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
        coordinates: [-79.4613271203871, 43.7535216196801],
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
        coordinates: [-79.4612725332962, 43.75326367491422],
      },
      properties: {
        title: "Room 108b",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46127074403375, 43.75321326924049],
      },
      properties: {
        title: "Room 108a",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46128058522986, 43.75315898346079],
      },
      properties: {
        title: "Room 106",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46125649284252, 43.75304288437272],
      },
      properties: {
        title: "Room 104",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46122382537122, 43.752906633057165],
      },
      properties: {
        title: "Room 102",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46136354515774, 43.752898126964254],
      },
      properties: {
        title: "Room 101",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46139777712486, 43.753043114903306],
      },
      properties: {
        title: "Room 103",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46140380351744, 43.75312579142903],
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
        coordinates: [-79.46145048325354, 43.753248299164255],
      },
      properties: {
        title: "Room 107",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4614761683771, 43.75338955719843],
      },
      properties: {
        title: "Room 109",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46164036883964, 43.75341958509614],
      },
      properties: {
        title: "Room 111",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4617811841459, 43.75340328772481],
      },
      properties: {
        title: "Room 113",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4618675399702, 43.75338755291526],
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
        coordinates: [-79.4619749024224, 43.753384181329636],
      },
      properties: {
        title: "Room 117",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46238565237367, 43.75363361197046],
      },
      properties: {
        title: "Room 231",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46236964343728, 43.75353590861371],
      },
      properties: {
        title: "Room 229",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46235355018324, 43.7534516311066],
      },
      properties: {
        title: "Room 227",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46233057723609, 43.753381976637144],
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
        coordinates: [-79.46232115842207, 43.75333592207335],
      },
      properties: {
        title: "Room 225",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46218059901656, 43.75335319315036],
      },
      properties: {
        title: "Room 223",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46211394375436, 43.75346309583611],
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
        coordinates: [-79.46199367203847, 43.753379882216166],
      },
      properties: {
        title: "Room 222",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46186832688937, 43.75339349079542],
      },
      properties: {
        title: "Room 221",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46175240183594, 43.75340709778331],
      },
      properties: {
        title: "Room 220",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46163140622886, 43.75342489140834],
      },
      properties: {
        title: "Room 219",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46148515501359, 43.75340071235618],
      },
      properties: {
        title: "Room 213",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46146486998195, 43.75331017352619],
      },
      properties: {
        title: "Room 211",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46144603105236, 43.753222249695966],
      },
      properties: {
        title: "Room 209",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46142791795658, 43.753137991624214],
      },
      properties: {
        title: "Room 207",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46139302860175, 43.75298885245036],
      },
      properties: {
        title: "Room 203",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46136767069875, 43.75288156880836],
      },
      properties: {
        title: "Room 201",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46122821655393, 43.752901057246845],
      },
      properties: {
        title: "Room 202",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4612506789127, 43.75298740995075],
      },
      properties: {
        title: "Room 204",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46126661842634, 43.75306957486865],
      },
      properties: {
        title: "Room 206",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46128545635727, 43.75315802234198],
      },
      properties: {
        title: "Room 208",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46130284491909, 43.75324332707672],
      },
      properties: {
        title: "Room 210",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46132168256682, 43.75332549164267],
      },
      properties: {
        title: "Room 212",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46134559208431, 43.75341393834546],
      },
      properties: {
        title: "Room 214",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46154185196188, 43.75361634427],
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
        coordinates: [-79.46144650667092, 43.75375052923056],
      },
      properties: {
        title: "dark room (216A)",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4615603074014, 43.75358834987574],
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
        coordinates: [-79.4614354341234, 43.753830952741794],
      },
      properties: {
        title: "Room 216",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46158008591014, 43.753810213485025],
      },
      properties: {
        title: "Room 215",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46145890294959, 43.75391685074018],
      },
      properties: {
        title: "Room 218",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46160715142894, 43.75393995400347],
      },
      properties: {
        title: "Room 217",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46138769422942, 43.75345548469946],
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
        coordinates: [-79.46139276605106, 43.753478131876875],
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
        coordinates: [-79.46139737638734, 43.75350077690234],
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
        coordinates: [-79.46140705817172, 43.753543403070495],
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
        coordinates: [-79.46141581781006, 43.75359668555146],
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
        coordinates: [-79.46150331164226, 43.753973545031556],
      },
      properties: {
        title: "art office (218A)",
        floor: 2,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46100506863056, 43.75350601053009],
      },
      properties: {
        title: "library room A",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46098927243114, 43.753440973854964],
      },
      properties: {
        title: "library room B",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.461073977011, 43.75360391989807],
      },
      properties: {
        title: "Exit 1",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4612968674094, 43.7528424736621],
      },
      properties: {
        title: "Exit 2",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46154945637606, 43.75343068463039],
      },
      properties: {
        title: "Exit 3",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46207053027169, 43.753387916496564],
      },
      properties: {
        title: "Exit 4",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.462225356633, 43.75329998220087],
      },
      properties: {
        title: "Exit 5",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4623567892464, 43.75368485054281],
      },
      properties: {
        title: "Exit 6",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46225551171938, 43.753697201431095],
      },
      properties: {
        title: "Exit 7",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4616471361122, 43.753852812405086],
      },
      properties: {
        title: "Exit 7C",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46163294208165, 43.75396385435636],
      },
      properties: {
        title: "Exit 7D",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46163524982596, 43.753980964854605],
      },
      properties: {
        title: "Exit 7E",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.4616518679316, 43.75403205707923],
      },
      properties: {
        title: "Exit 7F",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46154103707552, 43.754010022029945],
      },
      properties: {
        title: "Exit 8",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46143369162724, 43.75400234476848],
      },
      properties: {
        title: "Exit 8A",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46139309605415, 43.75381129680861],
      },
      properties: {
        title: "Exit 8B",
        floor: 1,
      },
    },
    {
      type: "Feature",
      geometry: {
        type: "Point",
        coordinates: [-79.46109108651713, 43.75380139567167],
      },
      properties: {
        title: "Exit 8C",
        floor: 1,
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
  marker: {
    color: 'red'
  },
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
// map.dragRotate.disable();
// map.touchZoomRotate.disableRotation();

map.on("load", () => {
  map.addSource("floorOne", {
    type: "image",
    url: "../static/core/img/FloorOne1.jpg",
    coordinates: [
      [-79.46270547634776, 43.75413886166868], //TL
      [-79.46072668772469, 43.75413886166868], //TR
      [-79.46072668772469, 43.75274955916902], //BR
      [-79.46270547634776, 43.75274955916902], //BL
    ],
  });

  map.addSource("floorTwo", {
    type: "image",
    url: "../static/core/img/FloorTwo1.jpg",
    coordinates: [
      [-79.46270547634776, 43.75413886166868], //TL
      [-79.46072668772469, 43.75413886166868], //TR
      [-79.46072668772469, 43.75274955916902], //BR
      [-79.46270547634776, 43.75274955916902], //BL
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
  //   coordinates.innerHTML = `latitude: ${lngLat.lat}, longitude: ${lngLat.lng}`;
  // }

  // marker.on("dragend", onDragEnd);

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

// const marker2 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46234537003488, 43.75327269027164])
//   .addTo(map);

// const marker3 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46244215769487, 43.75367965635641])
//   .addTo(map);

// const marker4 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46217382097582, 43.75371134269406])
//   .addTo(map);

// const marker5 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46191588301589, 43.753869889376745])
//   .addTo(map);

// const marker6 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46142684616693, 43.75403664808019])
//   .addTo(map);

// const marker7 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46136479422033, 43.75378023469304])
//   .addTo(map);

// const marker8 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46105150065856, 43.75380760757483])
//   .addTo(map);

// const marker9 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46087276984731, 43.75322304895161])
//   .addTo(map);

// const marker10 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46123520974277, 43.753196161692586])
//   .addTo(map);

// const marker11 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46115824792733, 43.752850086508715])
//   .addTo(map);

// const marker12 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46139159900635, 43.752824988257686])
//   .addTo(map);

// const marker13 = new mapboxgl.Marker({
// })
//   .setLngLat([-79.46156040136074, 43.753388033218926])
//   .addTo(map);
