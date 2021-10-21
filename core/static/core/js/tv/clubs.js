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
    $(".description").html(marked(club.extra_content));
    var elem = $("#scrollable")
    elem.scrollTop(0);
    var time = Math.min(60000, elem.prop("scrollHeight")*16);
    setTimeout(function() {elem.animate({scrollTop: elem.prop("scrollHeight")}, time)}, 30000);
    setTimeout(function(){}, 89000-time)
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