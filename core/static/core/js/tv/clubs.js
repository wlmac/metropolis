var clubs;
var i = 0;

function setSlide() {
    $("#fade").delay(250).fadeTo(250, 0);
    club = clubs[i];
    $(".club-logo").children().attr("src", club.icon);
    $(".club-name").text(club.name);
    $(".tag-section").empty();
    for (var tag of club.tags) {
        $(".tag-section").append(`<p class="tag" style="background-color: ${tag.color};">${tag.name}</p>`);
    }
    $(".bio").text(club.bio);
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
        $(".description").html(marked(club.extra_content));
        var elem = $("#scrollable1")
        var time = Math.min(60000, elem.prop("scrollHeight") * 16);
        elem.scrollTop(0);
        setTimeout(function () { elem.animate({ scrollTop: elem.prop("scrollHeight") }, time) }, 30000);
        elem = $("#scrollable2")
        time = Math.min(60000, elem.prop("scrollHeight") * 32);
        elem.scrollTop(0);
        setTimeout(function () { elem.animate({ scrollTop: elem.prop("scrollHeight") }, time) }, 30000);
        $("#fade").delay(119000).fadeTo(250, 1);
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