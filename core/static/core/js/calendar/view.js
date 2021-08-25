let calendarElement;
let calendar;
let selectedNumberColor = "#005bd5"
let selectedDate = null

// constants; should be gotten from database but sadge no database so frick
let events = [];

$(document).ready(function () {
    calendarElement = document.getElementById("calendar")

    calendar = new FullCalendar.Calendar(calendarElement, {
        headerToolbar: {right: "today dayGridMonth,timeGridWeek prev,next"},
        views: {
            timeGridWeek: {
                slotMinTime: "6:00:00",
                slotMaxTime: "17:00:00"
            },
            dayGridMonth: {
                dayCellDidMount: function (dayRenderInfo) {
                    reformatDay(dayRenderInfo.el)
                }
            }
        },
        viewDidMount: function () {
            calendar.select(new Date().setHours(0, 0, 0, 0))
        },
        selectAllow: function (selectInfo) {
            if (selectInfo.end.getTime() - selectInfo.start.getTime() <= (24 * 60 * 60 * 1000)) {
                return true;
            }
        },
        select: function (info) {
            selectedDate = info.start
            selectedDate = new Date(selectedDate.setHours(0, 0, 0, 0))
            let eventsToday = eventsOnDay(selectedDate);
            placeCards(eventsToday, selectedDate)
        },
        unselect: function () {
            selectedDate = null
        },
        events: function (fetchInfo, successCallback, failureCallback) {
            const url = "/api/events?start=" + fetchInfo.startStr + "&end=" + fetchInfo.endStr
            $.get(url, function (data, status) {
                if (status !== "success") {
                    failureCallback("Returned status " + status)
                } else {
                    events = data
                    successCallback(parseEvents(events))
                    if (selectedDate != null) {
                        calendar.select(selectedDate)
                    }
                }
            })
        },
        selectable: true,
        aspectRatio: 1.6,
        initialView: "dayGridMonth"
    });

    document.addEventListener("click", function () {
        highlightSelectedNumber()
    })
    calendar.select(new Date())
    calendar.render()
    highlightSelectedNumber()
})

function formatAllDays() {
    if (calendar.currentViewType === "dayGridMonth") {
        $(".fc-daygrid-day").each(function (ind, el) {
            reformatDay(el)
        })
    }
}

function reformatDay(dayElement) {
    let el = dayElement.querySelector(".fc-daygrid-day-top")
    let container = document.createElement("div")
    container.classList.add("fc-daygrid-day-number-circle")
    container.appendChild(el.querySelector(".fc-daygrid-day-number"))
    el.innerHTML = ""
    el.appendChild(container)
    $(container).width($(container).height())
}

function highlightSelectedNumber() {
    if (calendar.currentData.currentViewType === "dayGridMonth") {
        $(".fc-daygrid-day").each(function (ind, el) {
            $(el.querySelector(".fc-daygrid-day-number-circle")).css("backgroundColor", "")
            $(el.querySelector(".fc-daygrid-day-number")).css("color", "")
        })
        if (selectedDate !== null) {
            let selectedEl = $("[data-date='" + selectedDate.toISOString().split("T")[0] + "']")[0]
            let topEl = selectedEl.querySelector(".fc-daygrid-day-top")
            if (topEl.children.length !== 1 || !topEl.children[0].classList.contains(".fc-daygrid-day-number-circle")) {
                // something weird is going on so we must fix it :blobaww:
                reformatDay(selectedEl)
            }
            $(topEl.querySelector(".fc-daygrid-day-number-circle")).css("backgroundColor", selectedNumberColor)
            $(topEl.querySelector(".fc-daygrid-day-number")).css("color", "white")
        }
    }
}

// convert the events into smth that fullCalendar uses
function parseEvents(toParse) {
    const parsed = [];
    for (let curEvent of toParse) {
        parsed.push({
            title: curEvent.name,
            start: curEvent.start_date, // get rid of the "time" element
            end: curEvent.end_date,
            color: curEvent.tags.length > 0 ? curEvent.tags[0].color : "lightblue",
        })
    }
    return parsed
}

// get the events on a particular day
function eventsOnDay(day) {
    let today = day;
    let eventsOnDay = []
    for (let curEvent of events) {
        let eventStart = new Date(curEvent.start_date)
        let eventEnd = new Date(curEvent.end_date)
        let tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000)
        if (eventStart < tomorrow && eventEnd >= today) {
            eventsOnDay.push(curEvent);
        }
    }
    return eventsOnDay;
}

// place all of the relevant cards at the bottom
function placeCards(eventsToday, date) {
    let cards = document.querySelector("#eventDetails").querySelectorAll(".dayEvent")

    for (let i = 0; i < cards.length && i < eventsToday.length; i++) {
        $(cards[i]).stop().fadeOut(100, function () {
            let working = initializeCard(eventsToday[i], date).firstElementChild
            $(working).hide()
            $(this).replaceWith(working)
            $(working).fadeIn(100)
        })
    }
    for (let i = cards.length; i < eventsToday.length; i++) {
        let working = initializeCard(eventsToday[i], date)
        $(working.firstElementChild).hide()
        $(working.firstElementChild).fadeIn(100)
        document.querySelector("#eventDetails").appendChild(working)
    }
    for (let i = eventsToday.length; i < cards.length; i++) {
        $(cards[i]).stop().fadeOut(100, function () {
            $(this).remove()
        })
    }

    $("#details #detailsCurrentDay").html(date.toLocaleDateString(undefined, {
        day: "numeric",
        year: "numeric",
        "weekday": "long",
        month: "long"
    }));
    $("#details").fadeIn(75);
}

function initializeCard(curEvent, date, working = null) {
    if (working == null) working = document.querySelector("#card").content.cloneNode(true)
    let eventStart = new Date(curEvent.start_date);
    let eventEnd = new Date(curEvent.end_date)
    let [startTime, startAMPM] = eventStart < date ? dateTimeRepresentation(eventStart) : timeRepresentation(eventStart)

    let [endTime, endAMPM] = eventEnd >= new Date(date.getTime() + 24 * 60 * 60 * 1000) ?
        dateTimeRepresentation(eventEnd) : timeRepresentation(eventEnd);

    working.querySelector("#event_start").innerHTML = startTime;
    working.querySelector("#event_end").innerHTML = endTime;
    working.querySelector("#event_start_ampm").innerHTML = startAMPM
    working.querySelector("#event_end_ampm").innerHTML = endAMPM
    working.querySelector("#event_title").innerHTML = curEvent.name
    working.querySelector("#event_description").innerHTML = curEvent.description
    working.querySelector(".leftPanel").style = "background-color: " + (curEvent.tags.length > 0 ? curEvent.tags[0].color : "blue")
    working.querySelector("#event_host_name").innerHTML = curEvent.organization

    for (let tag of curEvent.tags) {
        let tagEl = document.createElement("span")
        tagEl.classList.add("eventTag")
        tagEl.innerHTML = tag.name
        tagEl.style.backgroundColor = tag.color
        working.querySelector(".detailPanel").appendChild(tagEl)
    }

    return working
}

// format the time of the date
function timeRepresentation(date) {
    let hours = date.getHours();
    let minutes = date.getMinutes();
    const ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes;
    const strTime = hours + ':' + minutes;
    return [strTime, ampm];
}

// get the string representing both the date and the time
function dateTimeRepresentation(date) {
    let dateFormat = new Intl.DateTimeFormat().format(date)
    let [time, ampm] = timeRepresentation(date)
    return [dateFormat + " " + time, ampm];
}