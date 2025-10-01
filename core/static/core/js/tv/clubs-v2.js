import clubOrder from "./club-order.json" with { type: "json" };

function setQR(clubId) {
    $('#qrcode').empty();
    let qrCode = new QRCodeStyling({
        width: 260,
        height: 260,
        type: "png",
        data: new URL(`/c/${clubId}`, window.location.origin).toString(),
        image: `${window.location.origin}/static/core/img/logo/logo-transparent-192.png`,
        dotsOptions: {
            color: "#161723",
            type: "rounded"
        },
        backgroundOptions: {
            color: "#ffffff",
        },
        cornersSquareOptions: {
            color: "#161723",
        },
        cornersDotOptions: { color: "#161723" },
        imageOptions: {
            crossOrigin: "anonymous",
            hideBackgroundDots: true,
        },
        qrOptions: {
            errorCorrectionLevel: 'H'
        }
    })

    qrCode.append(document.getElementById("qrcode"));
}

function setProgressBar() {
    let bar = document.getElementById("progress-bar");
    bar.style.transition = "none";
    bar.style.width = "100%";

    void bar.offsetWidth;

    bar.style.transition = `width ${slideDelayMs/1000}s linear`;
    bar.style.width = "0%";
}

let clubs
let i = 0
let prevClub
let timeout;
let timeout2;
const slideDelayMs = 15 * 1000
const baseUrl = "https://docs.google.com/presentation/d/e/2PACX-1vQNq8m65FMtqEoG_KuMvbEz9cXJgPpru5Nnkw-ymUuhxUIUw1T7-NDiAt31ypQhTvdsnurDxG_lTkA0/pubembed?start=false&loop=false&rm=minimal"

function setSlide() {
    i %= clubs.length;
    let club = clubs[i]
    let slideIndex = clubOrder.indexOf(club.id);
    console.log("Club: ", club)
    if (slideIndex < 0) {
        console.warn(`Skipping: No slide mapping for club ${club.name} (${club.id})`);
        i++
        clearTimeout(timeout);
        clearTimeout(timeout2);
        setSlide()
        return
    }

    setProgressBar()

    // Name + Logo
    document.getElementById("club-logo").src = club.icon
    document.getElementById("club-name").textContent = club.name

    // Tags
    document.getElementById("tag-section").textContent = ""
    for (var tag of club.tags) {
        let elem = document.createElement("span")
        elem.classList.add("tag")
        elem.style.backgroundColor = tag.color
        elem.textContent = tag.name
        document.getElementById("tag-section").appendChild(elem)
    }

    // Bio
    let bio = club.bio.trim().replace(/(?:\r\n|\r|\n)/g, " ")//.replace(/(.{199})..+/, "$1…"); //truncate to 200 chars
    document.getElementById("bio").textContent = bio
    document.getElementById("extra-content").innerHTML = DOMPurify.sanitize(marked.parse(club.extra_content))

    // Google slides map
    document.getElementById("map").src = baseUrl + "&delayms=" + slideDelayMs + "&slide=" + (slideIndex + 1);

    // QR Code
    setQR(club.id)

    timeout = setTimeout(setSlide, slideDelayMs);
    i++;
    prevClub = club
}


function slides() {
    $.getJSON(window.location.origin + "/api/organizations", function (data) {
        clubs = data;
        timeout = setTimeout(setSlide, 100);
        //note: changed to recursive setTimeout in setSlide
    });
}

window.onload = slides;

document.body.onkeyup = function(e) {
    if(e.key == " " || e.code == "Space") {
        clearTimeout(timeout2);
        clearTimeout(timeout);
        setSlide();
    }
}
