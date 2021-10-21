mapboxgl.accessToken = JSON.parse(
  document.getElementById("mapbox-apikey").textContent
)["apikey"];
const map = new mapboxgl.Map({
  container: "map", // container ID
  style: "mapbox://styles/nikisu/cktk76xy90rgm17s7q7pg0g55", // style URL
  center: [-79.46118496290478, 43.75367336221862], // starting position [lng, lat]
  zoom: 20, // starting zoom
});
const coordinates = document.getElementById("coordinates");
//-79.46155348420591, 43.753374130758445
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
    color: "red",
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
    url: "../static/core/img/FloorOne.jpg",
    coordinates: [
      [-79.46270547634776, 43.75413886166868], //TL
      [-79.46072668772469, 43.75413886166868], //TR
      [-79.46072668772469, 43.75274955916902], //BR
      [-79.46270547634776, 43.75274955916902], //BL
    ],
  });

  map.addSource("floorTwo", {
    type: "image",
    url: "../static/core/img/FloorTwo.jpg",
    coordinates: [
      [-79.46270547634776, 43.75413886166868], //TL
      [-79.46072668772469, 43.75413886166868], //TR
      [-79.46072668772469, 43.75274955916902], //BR
      [-79.46270547634776, 43.75274955916902], //BL
    ],
  });

  map.addSource("outline", {
    type: "image",
    url: "../static/core/img/booths/booths.jpg",
    coordinates: [
      [-79.46155542041252,43.7538999252219], //TL
      [-79.46100243451043,43.75394902268886], //TR
      [-79.46092763227323,43.7535715308978      ], //BR
      [-79.46146639944199,43.75351043643877], //BL
    ],
  });

  // const marker1 = new mapboxgl.Marker({})
  //   .setLngLat([-79.46155542041252,43.7538999252219])
  //   .addTo(map);

  // const marker2 = new mapboxgl.Marker({})
  //   .setLngLat([-79.46100243451043,43.75394902268886])
  //   .addTo(map);

  // const marker3 = new mapboxgl.Marker({})
  // .setLngLat([-79.46092763227323,43.7535715308978
  // ])
  // .addTo(map);

  // const marker4 = new mapboxgl.Marker({})
  // .setLngLat([-79.46146639944199,43.75351043643877])
  // .addTo(map);

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
      visibility: "visible",
    },
  });

  map.addLayer({
    id: "outline",
    source: "outline",
    type: "raster",
    layout: {
      // Make the layer visible by default.
      visibility: "visible",
    },
  });

  


  map.addSource("booths", {
    type: "geojson",
    data: {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: {
            id: 1,
            description: "<strong>MSC</strong><p> Mackenzie Science Club</p>",
            icon: "numbers-01",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46139104663334,43.75355029775528],
          },
        },
        {
          type: "Feature",
          properties: {
            id:2,
            description: "<strong>ACED</strong><p>ACED Competitive Business Case Competition Team</p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46135299052472,43.75355435346984],
          },
        },
        {
          type: "Feature",
          properties: {
            id:3,
            description: "<strong>MCPT</strong><p>Competative Case Competition Team</p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46140633146423,43.75361068280557],
          },
        },
        {
          type: "Feature",
          properties: {
            id:4,
            description: "<strong>HOSA</strong><p>Competative Health Science Case Competition Team</p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4613670276142,43.75361473851564],
          },
        },
        {
          type: "Feature",
          properties: {
            id:5,
            description: "<strong>Animanga Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46129996155962,43.753643128437574],
          },
        },
        {
          type: "Feature",
          properties: {
            id:6,
            description: "<strong>Cubing Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46130245704249,43.75365484492664],
          },
        },
        {
          type: "Feature",
          properties: {
            id:7,
            description: "<strong>Linguistics Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46131284434375,43.753675256273254
            ],
          },
        },
        {
          type: "Feature",
          properties: {
            id:8,
            description: "<strong>Chess Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46130994346608,43.753682784256455],
          },
        },
        {
          type: "Feature",
          properties: {
            id:9,
            description: "<strong>Book Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4613133747549,43.7536996830265],
          },
        },
        {
          type: "Feature",
          properties: {
            id:10,
            description: "<strong>3D Design Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46131587023714,43.753711399504084],
          },
        },
        {
          type: "Feature",
          properties: {
            id:11,
            description: "<strong>History Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46132023733188,43.75372807294906],
          },
        },
        {
          type: "Feature",
          properties: {
            id:12,
            description: "<strong>French Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4613295288922,43.75374470140514],
          },
        },
        {
          type: "Feature",
          properties: {
            id:13,
            description: "<strong>The Lyon </strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4612594868843,43.75362152388968],
          },
        },
        {
          type: "Feature",
          properties: {
            id:14,
            description: "<strong>Tree Huggers</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46124459518745,43.75362426423425],
          },
        },
        {
          type: "Feature",
          properties: {
            id:15,
            description: "<strong>Mac Radio Announcers</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4612215119736,43.753626292088825],
          },
        },
        {
          type: "Feature",
          properties: {
            id:16,
            description: "<strong>Let's Talk Now</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46120653907884,43.75362831994332],
          },
        },
        {
          type: "Feature",
          properties: {
            id:17,
            description: "<strong>Unicef</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46118158425318,43.753631023749705],
          },
        },
        {
          type: "Feature",
          properties: {
            id:18,
            description: "<strong>Rainbow Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46118158425318,43.753631023749705],
          },
        },
        {
          type: "Feature",
          properties: {
            id:19,
            description: "<strong>UNI-talk</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46114320601062,43.75363531841228],
          },
        },
        {
          type: "Feature",
          properties: {
            id:20,
            description: "<strong>Wellness @ Mac</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112855524916,43.75363710731256],
          },
        },
        {
          type: "Feature",
          properties: {
            id:21,
            description: "<strong>Gardening Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46110484816555,43.75363981111806],
          },
        },
        {
          type: "Feature",
          properties: {
            id:22,
            description: "<strong>Key Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46108956394,43.75364138851637],
          },
        },
        {
          type: "Feature",
          properties: {
            id:23,
            description: "<strong>Careers in Design</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4610658568558,43.75364499359026],
          },
        },
        {
          type: "Feature",
          properties: {
            id:24,
            description: "<strong>The Flounder</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46105026013957,43.75364657084009],
          },
        },
        {
          type: "Feature",
          properties: {
            id:25,
            description: "<strong>Cybersecurity Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46126130154995,43.75369496490765],
          },
        },
        {
          type: "Feature",
          properties: {
            id:26,
            description: "<strong>Mackenzie Engineering Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46125836307769,43.75368385665968],
          },
        },
        {
          type: "Feature",
          properties: {
            id:27,
            description: "<strong>MEDLIFE</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46124441016529,43.75366921436563],
          },
        },
        {
          type: "Feature",
          properties: {
            id:28,
            description: "<strong>Baycrest-Mackenzie Partnership</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46122940420271,43.75367073564328],
          },
        },
        {
          type: "Feature",
          properties: {
            id:29,
            description: "<strong>Women in STEM</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4612072901529,43.753673017559294],
          },
        },
        {
          type: "Feature",
          properties: {
            id:30,
            description: "<strong>Math Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46119307397782,43.75367510931548],
          },
        },
        {
          type: "Feature",
          properties: {
            id:31,
            description: "<strong>Physics Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46118543936576,43.75369241384283],
          },
        },
        {
          type: "Feature",
          properties: {
            id:32,
            description: "<strong>Chemistry Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46118807199032,43.75370306277998],
          },
        },
        {
          type: "Feature",
          properties: {
            id:33,
            description: "<strong>Muslim Culture Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46120334121555,43.75371827554389],
          },
        },
        {
          type: "Feature",
          properties: {
            id:34,
            description: "<strong>Biology Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46121729412793,43.753717134586736],
          },
        }, 
        {
          type: "Feature",
          properties: {
            id:35,
            description: "helk",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46121729412793,43.753717134586736],
          },
        },
        {
          type: "Feature",
          properties: {
            id:36,
            description: "<strong>Jewish Culture Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46121729412793,43.753717134586736],
          },
        },
        {
          type: "Feature",
          properties: {
            id:37,
            description: "<strong>Dance Team</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46114243759361,43.75370838709108],
          },
        },
        {
          type: "Feature",
          properties: {
            id:38,
            description: "<strong>Central Arts Council</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46113955168924,43.75369793518965],
          },
        },
        {
          type: "Feature",
          properties: {
            id:39,
            description: "<strong>Mackenzie Calligraphy Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112637950988,43.75368290855562],
          },
        },
        {
          type: "Feature",
          properties: {
            id:40,
            description: "<strong>Creator's Joy</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46111215219064,43.75368435623707],
          },
        },
        {
          type: "Feature",
          properties: {
            id:41,
            description: "<strong>Creative Arts Alliance</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46108975491188,43.75368682998976],
          },
        },
        {
          type: "Feature",
          properties: {
            id:42,
            description: "<strong>Creative Writing Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46107528243958,43.753688731082434],
          },
        },
        {
          type: "Feature",
          properties: {
            id:0,
            description: "<strong>Creative Writing Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46107528243958,43.753688731082434],
          },
        },
        {
          type: "Feature",
          properties: {
            id:0,
            description: "<strong>Creative Writing Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46107528243958,43.753688731082434],
          },
        },
        {
          type: "Feature",
          properties: {
            id:45,
            description: "<strong>Visual Arts Council</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46108557150073,43.753732314346166],
          },
        },
        {
          type: "Feature",
          properties: {
            id:46,
            description: "<strong>Drama Council</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46110005465303,43.753730562998385],
          },
        },
        {
          type: "Feature",
          properties: {
            id:47,
            description: "<strong>Drama Council</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112243893013,43.7537278999271],
          },
        },
        {
          type: "Feature",
          properties: {
            id:48,
            description: "<strong>Music Council</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46113638441307,43.75372637965694],
          },
        },
        {
          type: "Feature",
          properties: {
            id:49,
            description: "<strong>Model United Nations</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46129202108443,43.75376040150047],
          },
        },
        {
          type: "Feature",
          properties: {
            id:50,
            description: "<strong>Mackenzie Athletic Council</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46127728470296,43.75376227341238],
          },
        },
        {
          type: "Feature",
          properties: {
            id:51,
            description: "<strong>Mock Trials</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46125459716995,43.753765375457164],
          },
        },
        {
          type: "Feature",
          properties: {
            id:52,
            description: "<strong>Business Council</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46123927418843,43.75376667480484],
          },
        },
        {
          type: "Feature",
          properties: {
            id:53,
            description: "<strong>NBA Fan Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46121514474375,43.75376932842528
            ],
          },
        },
        {
          type: "Feature",
          properties: {
            id:54,
            description: "<strong>Debate Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46120000767044,43.75377131683837],
          },
        },
        {
          type: "Feature",
          properties: {
            id:55,
            description: "<strong>Kinesiology and Fitness</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46117567584362,43.75377313994014],
          },
        },
        {
          type: "Feature",
          properties: {
            id:56,
            description: "<strong>Esports Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46117567584362,43.75377313994014],
          },
        },
        {
          type: "Feature",
          properties: {
            id:57,
            description: "<strong>TED Club</strong><p> Description </p>",
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46116122798746,43.75377496318825],
          },
        },
      ],
    },
  });

  // Add a layer showing the places.
  map.addLayer({
    id: "booths",
    type: "symbol",
    source: "booths",
    layout: {
      "icon-image": "{icon}",
      "icon-allow-overlap": true,
      visibility: "visible",
    },
  });

  // When a click event occurs on a feature in the places layer, open a popup at the
  // location of the feature, with description HTML from its properties.
  map.on("click", "booths", (e) => {
    // Copy coordinates array.
    const coordinates = e.features[0].geometry.coordinates.slice();
    const description = e.features[0].properties.description;

    // Ensure that if the map is zoomed out such that multiple
    // copies of the feature are visible, the popup appears
    // over the copy being pointed to.
    // while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
    //   coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
    // }

    new mapboxgl.Popup().setLngLat(coordinates).setHTML(description).addTo(map);
  });

  // Change the cursor to a pointer when the mouse is over the places layer.
  map.on("mouseenter", "booths", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  // Change it back to a pointer when it leaves.
  map.on("mouseleave", "booths", () => {
    map.getCanvas().style.cursor = "";
  });

  const marker = new mapboxgl.Marker({
    draggable: true,
  })
    .setLngLat([-79.46118496290478, 43.75367336221862])
    .addTo(map);

  function onDragEnd() {
    const lngLat = marker.getLngLat();
    coordinates.style.display = "block";
    coordinates.innerHTML = `${lngLat.lng},${lngLat.lat}`;
  }

  marker.on("dragend", onDragEnd);

  // const marker13 = new mapboxgl.Marker({})
  //   .setLngLat([-79.46134268787472, 43.753754470296485])
  //   .addTo(map);

  // const marker14 = new mapboxgl.Marker({})
  //   .setLngLat([-79.46131549845754, 43.75363584806391])
  //   .addTo(map);

  // const marker15 = new mapboxgl.Marker({})
  //   .setLngLat([-79.46105121758568, 43.75381653094615])
  //   .addTo(map);

  // const marker16 = new mapboxgl.Marker({})
  // .setLngLat([-79.46101097724825,43.75363977606122])
  // .addTo(map);

  var checkbox = document.querySelector("input[name=checkbox]");

  checkbox.addEventListener("change", function () {
    if (this.checked) {
      console.log("Checkbox is checked..");
      map.setLayoutProperty("floorTwo", "visibility", "visible");
      map.setLayoutProperty("floorOne", "visibility", "none");
      map.setLayoutProperty("booths", "visibility", "none");
    } else {
      console.log("Checkbox is not checked..");
      map.setLayoutProperty("floorOne", "visibility", "visible");
      map.setLayoutProperty("floorTwo", "visibility", "none");
      map.setLayoutProperty("booths", "visibility", "visible");
    }
  });

  geocoder.on("result", ({ result }) => {
    console.log(result.properties.title);
    if (result.properties.floor == 1) {
      checkbox.checked = false;
      map.setLayoutProperty("floorOne", "visibility", "visible");
      map.setLayoutProperty("floorTwo", "visibility", "none");
      map.setLayoutProperty("booths", "visibility", "visible");
    } else {
      checkbox.checked = true;
      map.setLayoutProperty("floorTwo", "visibility", "visible");
      map.setLayoutProperty("floorOne", "visibility", "none");
      map.setLayoutProperty("booths", "visibility", "none");
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


