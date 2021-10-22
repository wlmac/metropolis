var clubs;
var i = 0;
var img = {
    6: 1,
    9: 1,
    5: 1,
    30: 1,
    14: 2,
    43: 2,
    15: 2,
    21: 2,
    23: 2,
    36: 2,
    26: 2,
    41: 2,
    22: 3,
    16: 3,
    28: 3,
    38: 3,
    48: 3,
    35: 3,
    37: 3,
    34: 3,
    13: 3,
    52: 3,
    56: 3,
    59: 3,
    57: 4,
    11: 4,
    33: 4,
    20: 4,
    49: 4,
    10: 4,
    25: 4,
    17: 4,
    39: 4,
    12: 4,
    //Dance Council (4)
    24: 4,
    //Dance Team (5)
    3: 5,
    44: 5,
    46: 5,
    40: 5,
    29: 5,
    //blank
    //blank
    50: 5,
    55: 5,
    54: 5,
    53: 5,
    4: 6,
    31: 6,
    45: 6,
    7: 6, //dupe
    51: 6,
    32: 6,
    47: 6,
    58: 6,
    27: 6,
    //Business Council?? (6)
    //BILT (6)
}

function setSlide() {
    //$("#fade").delay(250).fadeTo(250, 0);
    club = clubs[i];
    $(".club-logo").children().attr("src", club.icon);
    $(".club-name").text(club.name);
    $(".tag-section").empty();
    for (var tag of club.tags) {
        $(".tag-section").append(`<p class="tag" style="background-color: ${tag.color};">${tag.name}</p>`);
    }
    $(".bio").text(club.bio);
    if(club.id == 60) {
        $(".location").children().attr("src", "");
    } else if(img[club.id] == undefined) {
        $(".location").children().attr("src", "/static/core/img/booths/0.png");
    } else {
        $(".location").children().attr("src", `/static/core/img/booths/${img[club.id]}.png`);
    }
    $(".description").html(marked(club.extra_content));
    $(".club-execs").empty();
    var execlist = [];
    var promiselist = [];
    for (var exec of club.execs) {
        var fname;
        var lname;
        promiselist.push(new Promise((resolve, reject) => {
            $.getJSON(window.location.origin + "/api/user/" + exec.slug, function (data) {
                fname = data.first_name;
                lname = data.last_name;
                resolve();
            });
        }).then(() => {
            execlist.push({ fname: fname, lname: lname });
        }));
    }
    Promise.all(promiselist).then(() => {
        execlist.sort((a, b) => (a.fname > b.fname) ? 1 : (a.fname === b.fname) ? ((a.lname > b.lname) ? 1 : -1) : -1);
        for (let k = 0; k < execlist.length; k++) {
            $(".club-execs").append(`<p>${execlist[k].fname + " " + execlist[k].lname}</p>`);
        }
        var execs = $("#scrollable1")
        var extra = $("#scrollable2")
        var time = 12000
        execs.scrollTop(0);
        extra.scrollTop(0);
        setTimeout(function () {
            execs.animate({scrollTop: execs.prop("scrollHeight") }, time);
            extra.animate({scrollTop: extra.prop("scrollHeight") }, time);
        }, 8000);
        //$("#fade").delay(29000).fadeTo(250, 1);
        i++;
        i %= clubs.length;
    })
}

function slides() {
    $.getJSON(window.location.origin + "/api/organizations", function (data) {
        clubs = data;
        setTimeout(setSlide, 100);
        setInterval(setSlide, 30000);
    });
}