mapboxgl.accessToken = JSON.parse(
  document.getElementById("mapbox-apikey").textContent
)["apikey"];
// Without a real API key (local dev), fall back to a plain background so the floor plans still render.
const hasMapboxKey =
  mapboxgl.accessToken && mapboxgl.accessToken !== "change me";
const map = new mapboxgl.Map({
  container: "map", // container ID
  style: hasMapboxKey
    ? "mapbox://styles/nikisu/cktk76xy90rgm17s7q7pg0g55" // style URL
    : {
        version: 8,
        sources: {},
        layers: [
          {
            id: "background",
            type: "background",
            paint: { "background-color": "#dde5df" },
          },
        ],
      },
  center: [-79.46155348420591, 43.753374130758445], // starting position [lng, lat]
  zoom: 19, // starting zoom
});
const coordinates = document.getElementById("coordinates");
//-79.46118496290478, 43.75367336221862
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
        coordinates: [-79.46234560663818, 43.752886330082404],
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
        coordinates: [-79.46215462170524, 43.752906750712775],
      },
      properties: {
        title: "Portable 8",
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
        title: "fitness room (124c)",
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
        title: "dance studio (144)",
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
        title: "Library A",
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
        title: "Library B",
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
    {
      type: "Feature",
      properties: {
        title:'Stage',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46198968848333,43.75325517632149],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 13',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46219738125589,43.75323295523572],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 12',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46207866115284,43.75318521982399],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 11',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46165706009798,43.75321935736699],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 10',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.4618750685682,43.75311118946689],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 14',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46209468956859,43.753125035135554],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 15',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46207501005615,43.753063291649454],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 08',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46204669592589,43.75298912538665],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 07',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46193911779909,43.75295355028311],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 06',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46181749497252,43.752941266286854],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 05',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46170511120118,43.75294733544803],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 04',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46146134490077,43.75285072422923],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 03',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46147604027834,43.75293562803412],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 02',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46150013755523,43.753062392390746],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 01',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46151085321212,43.753155288730596],
      },
    },
    {
      type: "Feature",
      properties: {
        title:'Booth 09',
        floor: 1,
      },
      geometry: {
        type: "Point",
        coordinates: [-79.46168273591726,43.7530478330533],
      },
    },
  ],
  type: "FeatureCollection",
};

// map.dragRotate.disable();
// map.touchZoomRotate.disableRotation();

map.on("load", () => {
  // *-web.jpg are FloorOne/FloorTwo.jpg shrunk to 4096px (the max WebGL texture size on many phones); regenerate them when the originals change
  map.addSource("floorOne", {
    type: "image",
    url: "../static/core/img/FloorOne-web.jpg",
    coordinates: [
      [-79.46270547634776, 43.75413886166868], //TL
      [-79.46072668772469, 43.75413886166868], //TR
      [-79.46072668772469, 43.75274955916902], //BR
      [-79.46270547634776, 43.75274955916902], //BL
    ],
  });

  map.addSource("floorTwo", {
    type: "image",
    url: "../static/core/img/FloorTwo-web.jpg",
    coordinates: [
      [-79.46270547634776, 43.75413886166868], //TL
      [-79.46072668772469, 43.75413886166868], //TR
      [-79.46072668772469, 43.75274955916902], //BR
      [-79.46270547634776, 43.75274955916902], //BL
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
      visibility: "none",
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
            description:
              ' <b> Mackenzie Science Club </b><p><a href="https://maclyonsden.com/club/msc" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4613942054596, 43.75355665507274],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 2,
            description:
              '<b>ACED Team</b><p><a href="https://maclyonsden.com/club/aced" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46135445939534, 43.75356090732248],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 3,
            description:
              '<b>MCPT</b><p><a href="https://maclyonsden.com/club/mcpt" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46140496158867, 43.75360322941137],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 4,
            description:
              '<b>HOSA Team</b><p><a href="https://maclyonsden.com/club/hosa" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46136381338786, 43.75360627182371],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 5,
            description:
              '<b>Animanga Club</b><p><a href="https://maclyonsden.com/club/animanga-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46128489186641, 43.75364329694912],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 6,
            description:
              '<b>Cubing Club</b><p><a href="https://maclyonsden.com/club/cubing-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46128608332647, 43.75365481503346],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 7,
            description:
              '<b>Linguistics Club</b><p><a href="https://maclyonsden.com/club/linguistics" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4612909873974, 43.75367164651922],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 8,
            description:
              '<b>Chess Club</b><p><a href="https://maclyonsden.com/club/chess-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46129246204951, 43.75368139874675],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 9,
            description:
              '<b>Book Club</b><p><a href="https://maclyonsden.com/club/book-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46129614052039, 43.75369893721205],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 10,
            description:
              '<b>3D Design Club</b><p><a href="https://maclyonsden.com/club/3d-design-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46129823092178, 43.753710973343345],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 11,
            description:
              '<b>History Club</b><p><a href="https://maclyonsden.com/club/history-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46130174953414, 43.75372861925064],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 12,
            description:
              '<b>French Club</b><p><a href="https://maclyonsden.com/club/french-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46130560495627, 43.75373952230913],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 13,
            description:
              '<b>The Lyon</b><p><a href="https://maclyonsden.com/club/the-lyon" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46125581707167, 43.75362888910291],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 14,
            description:
              '<b>Tree Huggers</b><p><a href="https://maclyonsden.com/club/treehuggers" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46124157189129, 43.75363030445041],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 15,
            description:
              '<b>Mac Radio Annoucners</b><p><a href="https://maclyonsden.com/club/mac-radio-announcers" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46121714530972, 43.753632722096654],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 16,
            description:
              '<b>Let\'s Talk Now Club</b><p><a href="https://maclyonsden.com/club/lets-talk-now" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46120288834399, 43.7536349018703],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 17,
            description:
              '<b>UNICEF</b><p><a href="https://maclyonsden.com/club/unicef" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46117691331494, 43.753637686444335],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 18,
            description:
              '<b>Rainbow Club</b><p><a href="https://maclyonsden.com/club/rainbow-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46116265520898, 43.75363938250496],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 19,
            description:
              '<b>UNI-talk</b><p><a href="https://maclyonsden.com/club/UNI-talk" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46113823553753, 43.75364216826375],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 20,
            description:
              '<b>Wellness @ Mac</b><p><a href="https://maclyonsden.com/club/wellness-at-mac" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112314101545, 43.75364398532042],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 21,
            description:
              '<b>Gardening Club</b><p><a href="https://maclyonsden.com/club/gardening-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46109867295455, 43.75364676961962],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 22,
            description:
              '<b>Key Club</b><p><a href="https://maclyonsden.com/club/key-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46108357843245, 43.75364846567999],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 23,
            description:
              '<b>Careers in Design</b><p><a href="https://maclyonsden.com/club/careers-in-design" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46105850701775, 43.753651482449214],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 24,
            description:
              '<b>The Flounder</b><p><a href="https://maclyonsden.com/club/flounder" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46104391452232, 43.753652694705266],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 25,
            description:
              '<b>Cybersecurity Club</b><p><a href="https://maclyonsden.com/club/cybersecurity-club" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46126130154995, 43.75369496490765],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 26,
            description:
              '<b>Mackenzie Engineeering Club</b><p><a href="https://maclyonsden.com/club/MEC" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46125836307769, 43.75368385665968],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 27,
            description:
              '<b>MEDLIFE</b><p><a href="https://maclyonsden.com/club/medlife" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46123535767697, 43.7536597356675],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 28,
            description:
              '<b>Baycrest-Mackenzie Partnership</b><p><a href="https://maclyonsden.com/club/mackenzie-baycrest-partnership" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46121946489153, 43.75366139859827],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 29,
            description:
              '<b>Women in STEM</b><p><a href="https://maclyonsden.com/club/women-in-stem" target="_blank" title="Opens in a new window">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46119664892562, 43.75366456109961],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 30,
            description:
              '<b>Math Club</b><p><a href="https://maclyonsden.com/club/math-club" target="_blank" title="Math Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46118165938897, 43.7536663936842],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 31,
            description:
              '<b>Physics Club</b><p><a href="https://maclyonsden.com/club/physics-club" target="_blank" title="Physics Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46116413872673, 43.75369319879434],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 32,
            description:
              '<b>Chemistry Club</b><p><a href="https://maclyonsden.com/club/chemistry-club" target="_blank" title="Chemistry Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46116782229596, 43.75370450389764],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 33,
            description:
              '<b>Muslim Culture Club</b><p><a href="https://maclyonsden.com/club/muslim-culture-club" target="_blank" title="Muslim Culture Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46119500554012, 43.75372414542039],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 34,
            description:
              '<b>Biology Club</b><p><a href="https://maclyonsden.com/club/bio-club" target="_blank" title="Biology Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46120953770222, 43.75372133179536],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 35,
            description: "helk",
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [79.46123327399353, 43.75371816841607],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 36,
            description:
              '<b>Jewish Culture Club</b><p><a href="https://maclyonsden.com/club/jewish-culture-club" target="_blank" title="Jewish Culture Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46124826422738, 43.75371650221419],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 37,
            description:
              '<b>Dance Team</b><p><a href="https://www.instagram.com/wlmac.danceteam/" target="_blank" title="Dance Teal">@wlmac.danceteam</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46114243759361, 43.75370838709108],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 38,
            description:
              '<b>Central Arts Council</b><p><a href="https://maclyonsden.com/club/artscouncil" target="_blank" title="Central Arts Council">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46113955168924, 43.75369793518965],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 39,
            description:
              '<b>Mackenzie Calligraphy Club</b><p><a href="https://maclyonsden.com/club/mackenzie-calligraphy-club" target="_blank" title="Mackenzie Calligraphy Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46111398384248, 43.753675016730824],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 40,
            description:
              '<b>Creator’s Joy</b><p><a href="https://maclyonsden.com/club/creators-joy" target="_blank" title="Creator’s Joy">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46109894955666, 43.75367648606982],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 41,
            description:
              '<b>Creative Arts Alliance</b><p><a href="https://maclyonsden.com/club/creative-arts-alliance" target="_blank" title="Creative Arts Alliance">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46107682531661, 43.75367831739524],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 42,
            description:
              '<b>Creative Writing Club</b><p><a href="https://maclyonsden.com/club/mackenzie-creative-writing-club" target="_blank" title="Creative Writing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4610616059595, 43.75367998259105],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 43,
            description:
              "kgjhy",
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [79.46107528243958, 43.753688731082434],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 44,
            description:
              "jhfjhg",
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [79.46107528243958, 43.753688731082434],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 45,
            description:
              '<b>Visual Arts Council</b><p><a href="https://maclyonsden.com/club/visual-arts-council" target="_blank" title="Visual Arts Council">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4610749649739, 43.75373709635679],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 46,
            description:
              '<b>Drama Council</b><p><a href="https://maclyonsden.com/club/drama-concil" target="_blank" title="Drama Council">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46108924570751, 43.753734932774734],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 47,
            description:
              '<b>Composing Club</b><p><a href="https://maclyonsden.com/club/composing-club" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46111252113948, 43.753732934566415],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 48,
            description: '<b>Music Council</b></b><p><a href="https://maclyonsden.com/club/music-council" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112774136735, 43.753731102865345],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 49,
            description:
            '<b>Model United Nations</b></b><p><a href="https://maclyonsden.com/club/mun" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46127993280194, 43.75374969548815],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 50,
            description:
            '<b>Mackenzie Athletic Council</b></b><p><a href="https://maclyonsden.com/club/athletic-council" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46126622741446, 43.75375153977589],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 51,
            description: '<b>Mock Trials</b></b><p><a href="https://maclyonsden.com/club/mock-trials" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46124041855968, 43.75375353773157],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 52,
            description:
            '<b>Business Council</b></b><p><a href="https://maclyonsden.com/club/business-council" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46122634812941, 43.7537552030515],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 53,
            description: '<b>NBA Fan Club</b></b><p><a href="https://maclyonsden.com/club/nba-fan-club" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46119984807186, 43.7537563689765],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 54,
            description: '<b>Debate Club</b></b><p><a href="https://maclyonsden.com/club/debate-club" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46118508608991, 43.753758865571655],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 55,
            description:
            '<b>Kinesiology and Fitness</b></b><p><a href="https://maclyonsden.com/club/kinesiology-and-fitness" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46115973722371, 43.75376186231631],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 56,
            description: '<b>Esports Club</b></b><p><a href="https://maclyonsden.com/club/esports-club" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46114658851327, 43.753762862867404],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 57,
            description: '<b>TED Club</b></b><p><a href="https://maclyonsden.com/club/ted-club" target="_blank" title="Composing Club">Club Page</a></p>',
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112131852031, 43.75376500594942],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 58,
            description: "sdfsd",
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112131852031, 43.75376500594942],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 59,
            description: "<b>BILT</b><p>No Information Avalible</p>",
            icon: "embassy",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46112131852031, 43.75376500594942],
          },
        },
      ],
    },
  });


  map.addSource("mactoberfest", {
    type: "geojson",
    data: {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          properties: {
            id: 1,
            description:
              'Stage',
            icon: "castle",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46198968848333,43.75325517632149],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 13,
            description:
              '<b>Booth 12</b><p>Drama Council (Goodie Bags + Rice Crispies + Improv Costume Contest)</p> ',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46219738125589,43.75323295523572],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 12,
            description:
              '<b>Booth 11</b> <p>Gardening Club (Cookies)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46207866115284,43.75318521982399],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 11,
            description:
              '<b>Booth 10</b> <p>Music Council (Musical Chairs)</p>',
            icon: "bowling-alley",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46165706009798,43.75321935736699],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 10,
            description:
              '<b>Booth 09</b> <p>MCPT (Games)</p>',
            icon: "bowling-alley",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.4618750685682,43.75311118946689],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 14,
            description:
              '<b>Booth 13</b> <p>Photo Booth</p>',
            icon: "bowling-alley",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46209468956859,43.753125035135554],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 15,
            description:
              '<b>Booth 14</b> <p>DJ</p>',
            icon: "music",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46207501005615,43.753063291649454],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 8,
            description:
              '<b>Booth 07</b> <p>Let\' Talk Now (Timbits)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46193911779909,43.75295355028311],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 7,
            description:
              '<b>Booth 06</b> <p>MSC (Chips, Cotton Candy, Tic Tac)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46181749497252,43.752941266286854],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 6,
            description:
              '<b>Booth 05</b> <p>UNICEF (Junior Chickens + Dounuts)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46170511120118,43.75294733544803],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 5,
            description:
              '<b>Booth 04 </b> <p>Creator\'s Joy (Juice Boxes)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46159780966113,43.7528969650275],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 4,
            description:
              '<b>Booth 03 </b> <p>Book Club (Bookmarks + Baked Goods)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46147604027834,43.75293562803412],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 2,
            description:
              '<b>Booth 02 </b> <p> Dance Team (Popcorn)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46150013755523,43.753062392390746],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 1,
            description:
              '<b>Booth 01 </b> <p>Athletic Council (Hot Chocolate)</p>',
            icon: "fast-food",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46151085321212,43.753155288730596],
          },
        },
        {
          type: "Feature",
          properties: {
            id: 9,
            description:
              '<b>Booth 08 </b> <p>Dance Council (Instax Photo Booth)</p>',
            icon: "bowling-alley",
          },
          geometry: {
            type: "Point",
            coordinates: [-79.46168273591726,43.7530478330533],
          },
        },
      ],
    },
  });


// Add a layer showing the places.
// map.addLayer({
//   id: "mactoberfest",
//   type: "symbol",
//   source: "mactoberfest",
//   layout: {
//     "icon-image": "{icon}",
//     "icon-allow-overlap": true,
//     visibility: "none",
//   },
// });

// When a click event occurs on a feature in the places layer, open a popup at the
// location of the feature, with description HTML from its properties.
map.on("click", "mactoberfest", (e) => {
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
map.on("mouseenter", "mactoberfest", () => {
  map.getCanvas().style.cursor = "pointer";
});

// Change it back to a pointer when it leaves.
map.on("mouseleave", "mactoberfest", () => {
  map.getCanvas().style.cursor = "";
});


  // // Add a layer showing the places.
  // map.addLayer({
  //   id: "booths",
  //   type: "symbol",
  //   source: "booths",
  //   layout: {
  //     "icon-image": "{icon}",
  //     "icon-allow-overlap": true,
  //     visibility: "none",
  //   },
  // });

  // // When a click event occurs on a feature in the places layer, open a popup at the
  // // location of the feature, with description HTML from its properties.
  // map.on("click", "booths", (e) => {
  //   // Copy coordinates array.
  //   const coordinates = e.features[0].geometry.coordinates.slice();
  //   const description = e.features[0].properties.description;

  //   // Ensure that if the map is zoomed out such that multiple
  //   // copies of the feature are visible, the popup appears
  //   // over the copy being pointed to.
  //   // while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
  //   //   coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
  //   // }

  //   new mapboxgl.Popup().setLngLat(coordinates).setHTML(description).addTo(map);
  // });

  // // Change the cursor to a pointer when the mouse is over the places layer.
  // map.on("mouseenter", "booths", () => {
  //   map.getCanvas().style.cursor = "pointer";
  // });

  // // Change it back to a pointer when it leaves.
  // map.on("mouseleave", "booths", () => {
  //   map.getCanvas().style.cursor = "";
  // });

  // const marker = new mapboxgl.Marker({
  //   draggable: true,
  // })
  //   .setLngLat([-79.46118496290478, 43.75367336221862])
  //   .addTo(map);

  // function onDragEnd() {
  //   const lngLat = marker.getLngLat();
  //   coordinates.style.display = "block";
  //   coordinates.innerHTML = `${lngLat.lng},${lngLat.lat}`;
  // }

  // marker.on("dragend", onDragEnd);

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

  initClubSchedule();
});

// ---- Club meetings by weekday ----

const DAYS = ["mon", "tue", "wed", "thu", "fri"];
const FREQ_LABELS = {
  weekly: "Weekly",
  biweekly: "Every other week",
  monthly: "Monthly",
  occasional: "Occasionally",
};
const roomsByTitle = Object.fromEntries(
  customData.features.map((f) => [f.properties.title, f])
);
let currentFloor = 1;
let currentDay = DAYS[new Date().getDay() - 1] || "mon";
let clubsVisible = false;
const CLUBS_URL = JSON.parse(document.getElementById("clubs-url").textContent);
let countMarkers = [];
// fill for every highlighted room, solid outline for regular meetings, dashed for the rest
const CLUB_ROOM_LAYERS = [
  {
    id: "club-rooms",
    type: "fill",
    paint: {
      "fill-color": "#f2b705",
      "fill-opacity": ["case", ["get", "dim"], 0.05, ["get", "regular"], 0.4, 0.15],
    },
  },
  {
    id: "club-rooms-outline",
    type: "line",
    filter: ["get", "regular"],
    paint: { "line-color": "#e0a800", "line-width": 3, "line-opacity": ["case", ["get", "dim"], 0.25, 1] },
  },
  {
    id: "club-rooms-outline-occasional",
    type: "line",
    filter: ["!", ["get", "regular"]],
    paint: {
      "line-color": "#e0a800",
      "line-width": 3,
      "line-dasharray": [2, 1.5],
      "line-opacity": ["case", ["get", "dim"], 0.25, 1],
    },
  },
];
let clubPopup = null;
let selectedClub = null; // picked in the search; other clubs' rooms fade

function isDimmed(room) {
  return !!selectedClub && !room.meetings.some((m) => m.club == selectedClub);
}

function setFloor(floor) {
  currentFloor = floor;
  document.querySelectorAll("[data-floor]").forEach((tab) => {
    const active = tab.dataset.floor == floor;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", active);
  });
  // before the map's load event the layers don't exist yet; initClubSchedule applies the floor then
  if (map.getLayer("floorOne")) {
    map.setLayoutProperty("floorOne", "visibility", floor == 1 ? "visible" : "none");
    map.setLayoutProperty("floorTwo", "visibility", floor == 2 ? "visible" : "none");
  }
  for (const layer of CLUB_ROOM_LAYERS) {
    if (map.getLayer(layer.id)) map.setFilter(layer.id, floorFilter(layer.filter));
  }
  if (map.getLayer("search-room")) map.setFilter("search-room", floorFilter());
  renderCountMarkers();
}

function floorFilter(filter) {
  const onFloor = ["==", ["get", "floor"], currentFloor];
  return filter ? ["all", onFloor, filter] : onFloor;
}

// north-east corner of the room outline, where the club count badge sits
function badgeCorner(title, fallback) {
  const ring = ROOM_OUTLINES[title];
  if (!ring) return fallback;
  return ring.reduce((best, p) =>
    p[0] * Math.cos((p[1] * Math.PI) / 180) + p[1] >
    best[0] * Math.cos((best[1] * Math.PI) / 180) + best[1]
      ? p
      : best
  );
}

function roomDisplayName(title) {
  return title
    .replace(/^Room /, "Rm ")
    .replace(/\b[a-z]/g, (c) => c.toUpperCase());
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

// Group the day's meetings by room: { title, floor, coordinates, meetings, regular }
function roomsForDay(day) {
  const rooms = new Map();
  const month = new Date().getMonth() + 1;
  for (const meeting of CLUB_SCHEDULE[day]) {
    if (meeting.months && !meeting.months.includes(month)) continue;
    const key = meeting.room || "";
    if (!rooms.has(key)) {
      const feature = roomsByTitle[meeting.room];
      rooms.set(key, {
        title: meeting.room,
        floor: feature ? feature.properties.floor : null,
        coordinates: feature ? feature.geometry.coordinates : null,
        meetings: [],
        regular: false,
      });
    }
    const room = rooms.get(key);
    room.meetings.push(meeting);
    if (meeting.freq == "weekly" && meeting.time == "lunch") room.regular = true;
  }
  return [...rooms.values()];
}

function meetingsHtml(meetings) {
  return meetings
    .map((m) => {
      const details = [m.time == "lunch" ? "Lunch" : "After school", FREQ_LABELS[m.freq]];
      if (m.note) details.push(m.note);
      return `<li><a class="club-name" href="${CLUBS_URL}">${escapeHtml(m.club)}</a>
        <span class="club-details">${escapeHtml(details.join(" · "))}</span></li>`;
    })
    .join("");
}

function showRoomPopup(room, lngLat = room.coordinates) {
  if (clubPopup) clubPopup.remove();
  clubPopup = new mapboxgl.Popup({ className: "club-popup", maxWidth: "280px" })
    .setLngLat(lngLat)
    .setHTML(
      `<div class="club-popup-room">${escapeHtml(roomDisplayName(room.title))}</div>
       <ul>${meetingsHtml(room.meetings)}</ul>`
    )
    .addTo(map);
}

// The day's rooms in list order; rooms on the map get a number shared by their map badge and card.
function numberedRoomsForDay(day) {
  const rooms = roomsForDay(day).sort((a, b) => {
    // rooms on the map first (floor 1 then 2, numbered rooms before named spaces), then off-map locations
    const rank = (r) => (r.coordinates ? r.floor * 2 + (/^Room /.test(r.title) ? 0 : 1) : 9);
    return rank(a) - rank(b) || (a.title || "~").localeCompare(b.title || "~", undefined, { numeric: true });
  });
  let number = 0;
  for (const room of rooms) room.number = room.coordinates ? ++number : null;
  return rooms;
}

function renderCountMarkers() {
  countMarkers.forEach((m) => m.remove());
  countMarkers = [];
  if (!clubsVisible) return;
  for (const room of numberedRoomsForDay(currentDay)) {
    if (!room.coordinates || room.floor != currentFloor) continue;
    const el = document.createElement("button");
    el.className =
      "club-count" + (isDimmed(room) ? " club-count-dim" : "");
    el.textContent = room.number;
    el.title = `${room.number}. ${roomDisplayName(room.title)}`;
    el.addEventListener("click", (e) => {
      e.stopPropagation();
      showRoomPopup(room);
    });
    countMarkers.push(
      new mapboxgl.Marker({ element: el, offset: [-4, 4] })
        .setLngLat(badgeCorner(room.title, room.coordinates))
        .addTo(map)
    );
  }
}

function renderClubList() {
  const list = document.getElementById("club-list");
  const rooms = numberedRoomsForDay(currentDay);
  list.innerHTML = rooms
    .map((room, i) => {
      let where;
      if (room.coordinates) where = roomDisplayName(room.title);
      else if (room.title) where = `${escapeHtml(room.title)} <span class="club-list-floor">Not on map</span>`;
      else where = `Location not given`;
      return `<div class="club-list-room${room.coordinates ? " clickable" : ""}${isDimmed(room) ? " dim" : ""}" data-index="${i}">
          <div class="club-list-where">${
            room.number ? `<span class="club-count">${room.number}</span>` : ""
          }${where}</div>
          <ul>${meetingsHtml(room.meetings)}</ul>
        </div>`;
    })
    .join("");
  list.querySelectorAll(".club-list-room.clickable").forEach((el) => {
    el.addEventListener("click", (e) => {
      if (e.target.closest("a")) return; // club name links go to the clubs list
      const room = rooms[el.dataset.index];
      setFloor(room.floor);
      map.flyTo({ center: room.coordinates, zoom: 19.5, padding: panelPadding() });
      showRoomPopup(room);
      document.getElementById("map").scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });
}

function setDay(day) {
  currentDay = day;
  document.querySelectorAll("[data-day]").forEach((tab) => {
    const active = tab.dataset.day == day;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", active);
  });

  const rooms = roomsForDay(day).filter((r) => r.coordinates);
  map.getSource("club-rooms")?.setData({
    type: "FeatureCollection",
    features: rooms
      .filter((room) => ROOM_OUTLINES[room.title])
      .map((room) => ({
        type: "Feature",
        geometry: { type: "Polygon", coordinates: [ROOM_OUTLINES[room.title]] },
        properties: { title: room.title, floor: room.floor, regular: room.regular, dim: isDimmed(room) },
      })),
  });

  if (clubPopup) clubPopup.remove();
  renderCountMarkers();
  renderClubList();
}

function initClubSchedule() {
  map.addSource("club-rooms", {
    type: "geojson",
    data: { type: "FeatureCollection", features: [] },
  });
  for (const layer of CLUB_ROOM_LAYERS) {
    map.addLayer({ ...layer, source: "club-rooms", filter: floorFilter(layer.filter) });
  }

  map.addSource("search-room", { type: "geojson", data: { type: "FeatureCollection", features: [] } });
  map.addLayer({
    id: "search-room",
    type: "line",
    source: "search-room",
    filter: floorFilter(),
    paint: { "line-color": "#d32f2f", "line-width": 4 },
  });

  map.on("click", "club-rooms", (e) => {
    const title = e.features[0].properties.title;
    const room = roomsForDay(currentDay).find((r) => r.title == title);
    if (room) showRoomPopup(room, e.lngLat);
  });
  map.on("mouseenter", "club-rooms", () => {
    map.getCanvas().style.cursor = "pointer";
  });
  map.on("mouseleave", "club-rooms", () => {
    map.getCanvas().style.cursor = "";
  });

  // apply whatever was picked while the map was still loading
  setFloor(currentFloor);
  setClubsVisible(clubsVisible);
}

function setClubsVisible(visible) {
  clubsVisible = visible;
  document.getElementById("club-controls").hidden = !visible;
  document.getElementById("club-list").hidden = !visible;
  for (const layer of CLUB_ROOM_LAYERS) {
    if (map.getLayer(layer.id)) map.setLayoutProperty(layer.id, "visibility", visible ? "visible" : "none");
  }
  if (!visible && clubPopup) clubPopup.remove();
  setDay(currentDay);
}

// Controls work straight away; the map layers catch up in initClubSchedule once the map loads.
document.querySelectorAll("[data-day]").forEach((tab) => {
  tab.addEventListener("click", () => setDay(tab.dataset.day));
});
document.querySelectorAll("[data-floor]").forEach((tab) => {
  tab.addEventListener("click", () => setFloor(Number(tab.dataset.floor)));
});
const clubToggle = document.getElementById("club-toggle");
clubToggle.addEventListener("change", () => {
  if (!clubToggle.checked && selectedClub) selectClub(null);
  setClubsVisible(clubToggle.checked);
});
setClubsVisible(clubToggle.checked);

// ---- Search: rooms, portables and clubs ----

// other names people search by
const SEARCH_ALIASES = {
  "MSC (Mackenzie Science Club)": ["Mackenzie Science Club"],
  "Model United Nations": ["Model UN", "MUN"],
  "large gym (127)": ["gymnasium"],
  "small gym (124)": ["gymnasium"],
  "cafeteria/cafetorium": ["cafe"],
};
// suggested before anything is typed
const POPULAR_CLUBS = ["MSC (Mackenzie Science Club)", "HOSA", "MCPT", "Model United Nations"];

// "Room 113", "rm 113" and "113" all become "113"
function normalizeSearch(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .replace(/^(room|rm) /, "");
}

const SEARCH_ENTRIES = [
  ...customData.features
    .filter((f) => !f.properties.title.startsWith("Booth")) // old Mactoberfest booths
    .map((f) => ({
      type: f.properties.title.startsWith("Portable") ? "Portable" : "Room",
      name: f.properties.title,
      feature: f,
    })),
  ...[...new Set(DAYS.flatMap((d) => CLUB_SCHEDULE[d].map((m) => m.club)))].map((name) => ({ type: "Club", name })),
].map((entry) => ({ ...entry, keys: [entry.name, ...(SEARCH_ALIASES[entry.name] || [])].map(normalizeSearch) }));

// 0 exact, 1 starts with, 2 a word starts with, 3 contains; Infinity = no match
function matchScore(keys, q) {
  let best = Infinity;
  for (const key of keys) {
    if (key == q) best = Math.min(best, 0);
    else if (key.startsWith(q)) best = Math.min(best, 1);
    else if (key.split(" ").some((w) => w.startsWith(q))) best = Math.min(best, 2);
    else if (key.includes(q)) best = Math.min(best, 3);
  }
  return best;
}

function searchMap(query) {
  const q = normalizeSearch(query);
  if (!q) return POPULAR_CLUBS.map((name) => SEARCH_ENTRIES.find((e) => e.name == name)).filter(Boolean);
  return SEARCH_ENTRIES.map((entry) => ({ entry, score: matchScore(entry.keys, q) }))
    .filter((r) => r.score < Infinity)
    .sort((a, b) => a.score - b.score || a.entry.name.localeCompare(b.entry.name, undefined, { numeric: true }))
    .slice(0, 8)
    .map((r) => r.entry);
}

function clubMeetsOn(club, day) {
  const month = new Date().getMonth() + 1;
  return CLUB_SCHEDULE[day].some((m) => m.club == club && (!m.months || m.months.includes(month)));
}

function setSearchRoom(feature) {
  const ring = feature && ROOM_OUTLINES[feature.properties.title];
  map.getSource("search-room")?.setData({
    type: "FeatureCollection",
    features: ring
      ? [{ type: "Feature", geometry: { type: "Polygon", coordinates: [ring] }, properties: { floor: feature.properties.floor } }]
      : [],
  });
}

// keeps zoomed-to rooms out from under the floating panel (beside it on wide maps, below it on narrow ones)
function panelPadding() {
  const panel = document.querySelector(".map-panel");
  return map.getContainer().clientWidth < 600
    ? { top: panel.offsetHeight + 30, bottom: 60, left: 30, right: 30 }
    : { top: 50, bottom: 60, left: panel.offsetWidth + 40, right: 50 };
}

function selectRoom(feature) {
  if (selectedClub) selectClub(null);
  const title = feature.properties.title;
  setFloor(feature.properties.floor);
  setSearchRoom(feature);
  map.flyTo({ center: feature.geometry.coordinates, zoom: 20, padding: panelPadding() });
  const room = clubsVisible && roomsForDay(currentDay).find((r) => r.title == title);
  if (room) return showRoomPopup(room);
  if (clubPopup) clubPopup.remove();
  clubPopup = new mapboxgl.Popup({ className: "club-popup" })
    .setLngLat(feature.geometry.coordinates)
    .setHTML(`<div class="club-popup-room">${escapeHtml(roomDisplayName(title))}</div>`)
    .addTo(map);
}

function selectClub(club) {
  selectedClub = club;
  document.getElementById("club-chip").hidden = !club;
  document.querySelectorAll("[data-day]").forEach((tab) => {
    tab.classList.toggle("club-day", !!club && clubMeetsOn(club, tab.dataset.day));
  });
  if (!club) return setDay(currentDay);

  setSearchRoom(null);
  // today if the club meets today, otherwise its next meeting day (weekends roll over to Monday)
  const today = new Date().getDay() - 1;
  const days = DAYS.filter((d) => clubMeetsOn(club, d));
  currentDay = days.find((d) => DAYS.indexOf(d) >= today) || days[0] || currentDay;
  clubToggle.checked = true;
  setClubsVisible(true);

  const onMap = roomsForDay(currentDay).filter((r) => r.coordinates && r.meetings.some((m) => m.club == club));
  document.getElementById("club-chip-name").textContent = onMap.length ? club : `${club} · not on the map`;
  if (!onMap.length) return;
  const floor = onMap.some((r) => r.floor == 1) ? 1 : 2;
  setFloor(floor);
  const bounds = new mapboxgl.LngLatBounds();
  for (const room of onMap.filter((r) => r.floor == floor)) {
    for (const point of ROOM_OUTLINES[room.title] || [room.coordinates]) bounds.extend(point);
  }
  map.fitBounds(bounds, { padding: panelPadding(), maxZoom: 20 });
}

const searchInput = document.getElementById("map-search");
const searchList = document.getElementById("map-search-results");
let searchResults = [];
let activeResult = -1;

function renderSearch() {
  searchList.innerHTML = searchResults
    .map(
      (entry, i) =>
        `<li role="option" id="map-search-${i}" data-index="${i}" aria-selected="${i == activeResult}">
          <span>${escapeHtml(entry.type == "Club" ? entry.name : roomDisplayName(entry.name))}</span>
          <span class="map-search-type">${entry.type}</span></li>`
    )
    .join("");
  searchList.hidden = !searchResults.length;
  searchInput.setAttribute("aria-expanded", !searchList.hidden);
  searchInput.setAttribute("aria-activedescendant", activeResult >= 0 ? `map-search-${activeResult}` : "");
}

function closeSearch() {
  searchList.hidden = true;
  searchInput.setAttribute("aria-expanded", false);
}

function chooseResult(entry) {
  searchInput.value = entry.type == "Club" ? entry.name : roomDisplayName(entry.name);
  closeSearch();
  searchInput.blur(); // closes the keyboard on phones
  if (entry.type == "Club") selectClub(entry.name);
  else selectRoom(entry.feature);
}

searchInput.addEventListener("focus", () => {
  searchResults = searchMap(searchInput.value);
  activeResult = -1;
  renderSearch();
});
searchInput.addEventListener("input", (e) => {
  const typed = searchInput.value;
  searchResults = searchMap(typed);
  activeResult = searchResults.length ? 0 : -1;
  renderSearch();
  // autofill the rest of the top match, selected so the next keystroke replaces it
  const top = searchResults[0];
  if (top && e.inputType == "insertText" && top.name.toLowerCase().startsWith(typed.toLowerCase())) {
    searchInput.value = top.name;
    searchInput.setSelectionRange(typed.length, top.name.length);
  }
});
searchInput.addEventListener("keydown", (e) => {
  if (e.key == "ArrowDown" || e.key == "ArrowUp") {
    e.preventDefault();
    if (!searchResults.length) return;
    activeResult = (activeResult + (e.key == "ArrowDown" ? 1 : -1) + searchResults.length) % searchResults.length;
    renderSearch();
  } else if (e.key == "Enter") {
    e.preventDefault();
    if (searchResults.length) chooseResult(searchResults[Math.max(activeResult, 0)]);
  } else if (e.key == "Escape") {
    closeSearch();
  }
});
searchInput.addEventListener("blur", closeSearch);
// mousedown, not click: it runs before the input's blur hides the list
searchList.addEventListener("mousedown", (e) => {
  const item = e.target.closest("li");
  if (!item) return;
  e.preventDefault();
  chooseResult(searchResults[item.dataset.index]);
});
document.getElementById("club-chip-clear").addEventListener("click", () => {
  searchInput.value = "";
  selectClub(null);
});

// self-check for the search matching
console.assert(searchMap("113")[0]?.name == "Room 113", "search: room number");
console.assert(searchMap("rm 113")[0]?.name == "Room 113", "search: rm prefix");
console.assert(searchMap("hosa")[0]?.name == "HOSA", "search: club");
console.assert(searchMap("msc")[0]?.name == "MSC (Mackenzie Science Club)", "search: club acronym");
console.assert(searchMap("model un")[0]?.name == "Model United Nations", "search: alias");
console.assert(searchMap("gymnasium").some((e) => e.name == "large gym (127)"), "search: gym alias");
console.assert(searchMap("zzzz").length == 0, "search: no match");

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
