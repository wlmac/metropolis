import clubStasRaw from "./club-data.json" assert {type: "json"};

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

function flattenClubStasRaw(clubStasRaw) {
    let res = {}
    for (let groupName in clubStasRaw.groups) {
        let group = clubStasRaw.groups[groupName]
        for (let clubId in group) {
            let station = group[clubId]
            res[clubId] = { station, group: groupName }
        }
    }
    return res
}

let clubStas = flattenClubStasRaw(clubStasRaw)

let clubs
let i = 0
let prevClub
let userCache = {}
let timeout;
let timeout2;

function setSlide() {
    //$("#fade").delay(250).fadeTo(250, 0);
    i %= clubs.length;
    let club = clubs[i]
    let clubSta = clubStas[club.id]
    console.log(club, clubSta)
    if (!clubSta || !(clubSta.group)) {
        console.log(`skip ${club.id} ${club.slug}`)
        i++
        clearTimeout(timeout);
        clearTimeout(timeout2);
        setSlide();
        return
    }
    document.getElementById("club-logo").src = club.icon
    document.getElementById("club-name").textContent = club.name
    document.getElementById("tag-section").textContent = ""
    for (var tag of club.tags) {
        let elem = document.createElement("span")
        elem.classList.add("tag")
        elem.style.backgroundColor = tag.color
        elem.textContent = tag.name
        document.getElementById("tag-section").appendChild(elem)
    }
    let bio = club.bio.trim().replace(/(?:\r\n|\r|\n)/g, " ").replace(/(.{199})..+/, "$1…"); //truncate to 200 chars
        //.replace(new RegExp(`^([Tt]he )?${club.name}`), "We") // whats this
    document.getElementById("bio").textContent = bio
    // document.getElementById("scrollable2").innerHTML = DOMPurify.sanitize(marked.parse(club.extra_content));
    document.getElementById("scrollable1").textContent = ''
    setQR(club.id)
    let map = document.getElementById("location").getSVGDocument();
    for (let elem of map.getElementsByClassName(`desk-${clubSta.group}-${clubSta.station}`)) {
        elem.classList.add("selected")
    }
    if (prevClub && prevClub.id !== club.id) {
        let clubSta2 = clubStas[prevClub.id]
        for (let elem of map.getElementsByClassName(`desk-${clubSta2.group}-${clubSta2.station}`)) {
            elem.classList.remove("selected")
        }
    }
    var execlist = [];
    var promiselist = [];
    for (var exec of club.execs) {
        var fname;
        var lname;
        if (exec.slug in userCache) {
            let user = userCache[exec.slug]
            execlist.push({ fname: user.first_name, lname: user.last_name })
            //console.log(`pushed ${user.first_name} to exec list 1 from ${exec.slug}`);
        } else {
            promiselist.push(new Promise((resolve, reject) => {
                let tmpslug = exec.slug;
                console.log(`requesting ${tmpslug}`)
                $.getJSON(window.location.origin + "/api/user/" + tmpslug, function (data) {
                    fname = data.first_name
                    lname = data.last_name
                    userCache[tmpslug] = data
                    resolve()
                });
            }).then(() => {
                execlist.push({ fname: fname, lname: lname })
                //console.log(`pushed ${fname} to exec list 2`);
            }));
        }
    }
    Promise.all(promiselist).then(() => {
        //console.log("Execlist");
        //console.log(execlist);
        execlist.sort((a, b) => (a.fname > b.fname) ? 1 : (a.fname === b.fname) ? ((a.lname > b.lname) ? 1 : -1) : -1);
        for (let exec of execlist) {
            let elem = document.createElement("p")
            elem.textContent = `${exec.fname} ${exec.lname}`
            document.getElementById("scrollable1").appendChild(elem)
        }
        var execs = $("#scrollable1")
        //var extra = $("#scrollable2")
        var time = 6000;
        execs.scrollTop(0);
        //extra.scrollTop(0);
        timeout2 = setTimeout(function () {
            execs.animate({ scrollTop: execs.prop("scrollHeight") }, time);
            //extra.animate({ scrollTop: extra.prop("scrollHeight") }, time);
        }, 3000);
        //$("#fade").delay(29000).fadeTo(250, 1);
        i++;
        timeout = setTimeout(setSlide, 10000);
    })
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
