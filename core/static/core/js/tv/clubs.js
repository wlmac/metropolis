var clubs;
var i = 0;

function setSlide() {
    $("#fade").delay(250).fadeTo(250, 0);
    club = clubs[i];
    $(".club-logo").children().attr("src", club.icon);
    $(".club-name").text(club.name);
    $(".tag-section").empty();
    for(var tag of club.tags) {
        $(".tag-section").append(`<p class="tag" style="background-color: ${tag.color};">${tag.name}</p>`);
    }
    $(".bio").text(club.bio);
    $(".club-execs").empty();
    for(var exec of club.execs) {
        var name;
        new Promise((resolve, reject) => {
            $.getJSON(window.location.origin+"/api/user/"+exec.slug, function(data) {
                name = data.first_name + " " + data.last_name;
                resolve();
            });
        }).then(() => {
            $(".club-execs").append(`<p>${name}</p>`);
        });
    }
    $(".description").html(marked(club.extra_content));
    var elem = $("#scrollable1")
    var time = Math.min(60000, elem.prop("scrollHeight")*16);
    elem.scrollTop(0);
    setTimeout(function() {elem.animate({scrollTop: elem.prop("scrollHeight")}, time)}, 30000);
    elem = $("#scrollable2")
    time = Math.min(60000, elem.prop("scrollHeight")*32);
    elem.scrollTop(0);
    setTimeout(function() {elem.animate({scrollTop: elem.prop("scrollHeight")}, time)}, 30000);
    $("#fade").delay(119000).fadeTo(250, 1);
    i++;
    i %= clubs.length;
}

function slides() {
    $.getJSON(window.location.origin+"/api/organizations", function(data) {
        clubs = data;
    });
    setTimeout(setSlide, 100);
    setInterval(setSlide, 120000);
}