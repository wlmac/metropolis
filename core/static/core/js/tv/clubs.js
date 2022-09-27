import clubStasRaw from "./club-data.json" assert { type: "json" };

function flattenClubStasRaw(clubStasRaw) {
    const res = {}
    for (let groupName in clubStasRaw.groups) {
        const group = clubStasRaw.groups[groupName]
        for (let clubId in group) {
            const station = group[clubId]
            res[clubId] = { station, group: groupName }
        }
    }
    return res
}

const clubStas = flattenClubStasRaw(clubStasRaw)

let clubs
let i = 0
let prevClub
const userCache = {}

function setSlide() {
    //$("#fade").delay(250).fadeTo(250, 0);
    const club = clubs[i]
    document.getElementById("club-logo").src = club.icon
    document.getElementById("club-name").textContent = club.name
    document.getElementById("tag-section").textContent = ""
    for (var tag of club.tags) {
        const elem = document.createElement("span")
        elem.classList.add("tag")
        elem.style.backgroundColor = tag.color
        elem.textContent = tag.name
        document.getElementById("tag-section").appendChild(elem)
    }
    document.getElementById("bio").textContent = club.bio
    document.getElementById("scrollable2").innerHTML = DOMPurify.sanitize(marked.parse(club.extra_content));
    document.getElementById("scrollable1").textContent = ''
    QRCode.toCanvas(document.getElementById("qrcode"), new URL(`/club/${club.slug}`, window.location.origin).href)
    let clubSta = clubStas[club.id]
    const map = document.getElementById("location").getSVGDocument();
    for (let elem of map.getElementsByClassName(`desk-${clubSta.group}-${clubSta.station}`)) {
        elem.classList.add("selected")
    }
    if (prevClub) {
        clubSta = clubStas[prevClub.id]
        for (let elem of map.getElementsByClassName(`desk-${clubSta.group}-${clubSta.station}`)) {
            elem.classList.remove("selected")
        }
    }
    var execlist = [];
    var promiselist = [];
    for (var exec of club.execs) {
        var fname;
        var lname;
        if (exec.slug in userCache) {
            const user = userCache[exec.slug]
            execlist.push({ fname: user.first_name, lname: user.last_name })
        } else {
            promiselist.push(new Promise((resolve, reject) => {
                console.log(`requesting ${exec.slug}`)
                $.getJSON(window.location.origin + "/api/user/" + exec.slug, function (data) {
                    fname = data.first_name
                    lname = data.last_name
                    userCache[exec.slug] = data
                    resolve()
                });
            }).then(() => {
                execlist.push({ fname: fname, lname: lname })
            }));
        }
    }
    Promise.all(promiselist).then(() => {
        execlist.sort((a, b) => (a.fname > b.fname) ? 1 : (a.fname === b.fname) ? ((a.lname > b.lname) ? 1 : -1) : -1);
        for (let exec of execlist) {
            const elem = document.createElement("p")
            elem.textContent = `${exec.fname} ${exec.lname}`
            document.getElementById("scrollable1").appendChild(elem)
        }
        var execs = $("#scrollable1")
        var extra = $("#scrollable2")
        var time = 1000
        execs.scrollTop(0);
        extra.scrollTop(0);
        setTimeout(function () {
            execs.animate({scrollTop: execs.prop("scrollHeight") }, time);
            extra.animate({scrollTop: extra.prop("scrollHeight") }, time);
        }, 7000);
        //$("#fade").delay(29000).fadeTo(250, 1);
        i++;
        i %= clubs.length;
    })
    prevClub = club
}

function slides() {
    $.getJSON(window.location.origin + "/api/organizations", function (data) {
        clubs = data;
        setTimeout(setSlide, 100);
        setInterval(setSlide, 10000);
    });
}

window.onload = slides;
