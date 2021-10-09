let calendarElement;
let calendar;
let selectedNumberColor = "var(--dark-blue)"
let selectedDate = null
let maxAspectRatio = 1.7

// constants; should be gotten from database but sadge no database so frick
let events = [];

$(document).ready(function () {
    calendarElement = document.getElementById("calendar")

    calendar = new FullCalendar.Calendar(calendarElement, {
        headerToolbar: {right: "today prev,next"},
        views: {
            timeGridWeek: {
                slotMinTime: "6:00:00",
                slotMaxTime: "17:00:00"
            },
            dayGridMonth: {
                // format each day when it loads
                dayCellDidMount: function (dayRenderInfo) {
                    reformatDay(dayRenderInfo.el)
                },
                aspectRatio: maxAspectRatio
            }
        },
        // select the current date whenever we change views
        viewDidMount: function () {
            calendar.select(new Date().setHours(0, 0, 0, 0))
            if (maxAspectRatio * $(calendarElement).innerHeight() < $(calendarElement).innerWidth()) {
                calendar.setOption("height", null)
                calendar.updateSize()
            }
        },
        selectable: true,
        selectAllow: function (selectInfo) {
            // only allow select to select one day
            if (selectInfo.end.getTime() - selectInfo.start.getTime() <= (24 * 60 * 60 * 1000)) {
                return true;
            }
        },
        select: function (info) {
            // when a day is selected, we set the selectedDate
            selectedDate = info.start
            selectedDate = new Date(selectedDate.setHours(0, 0, 0, 0))
            let eventsToday = eventsOnDay(selectedDate);

            // place the cards at the bottom
            placeCards(eventsToday, selectedDate)
            highlightSelectedNumber()
        },
        unselect: function () {
            selectedDate = null
            highlightSelectedNumber()
        },
        events: function (fetchInfo, successCallback, failureCallback) {
            // get events via url
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
        height: "auto",
        selectLongPressDelay: 0,
        initialView: "dayGridMonth"
    });
    // start off by selecting today
    calendar.select(new Date())
    calendar.render()

    // after everything's loaded, we highlight the selected number (which should be today)
    highlightSelectedNumber()
})

function formatAllDays() {
    // if we're in the calendar view
    if (calendar.currentViewType === "dayGridMonth") {
        // format each day cell
        $(".fc-daygrid-day").each(function (ind, el) {
            reformatDay(el)
        })
    }
}

function reformatDay(dayElement) {
    let el = dayElement.querySelector(".fc-daygrid-day-top")
    let container = document.createElement("div")
    container.classList.add("fc-daygrid-day-number-circle")

    // place the number of the current day inside the container div
    container.appendChild(el.querySelector(".fc-daygrid-day-number"))

    // reset the top, and append the container
    el.innerHTML = ""
    el.appendChild(container)

    // make the container a square
    $(container).width($(container).height())
}

function highlightSelectedNumber() {
    if (calendar.currentData.currentViewType === "dayGridMonth") {
        // unselect every cell
        $(".fc-daygrid-day").each(function (ind, el) {
            $(el.querySelector(".fc-daygrid-day-number-circle")).css("backgroundColor", "")
            $(el.querySelector(".fc-daygrid-day-number")).attr("selected", false)
        })

        if (selectedDate !== null) {
            // get the selected element
            let selectedEl = $("[data-date='" + selectedDate.toISOString().split("T")[0] + "']")[0]
            if (selectedEl != null) {
                let topEl = selectedEl.querySelector(".fc-daygrid-day-top")
                if (topEl.children.length !== 1 || !topEl.children[0].classList.contains(".fc-daygrid-day-number-circle")) {
                    // something weird is going on so we must fix it
                    reformatDay(selectedEl)
                }

                // change the background color of the circle
                $(topEl.querySelector(".fc-daygrid-day-number-circle")).css("backgroundColor", selectedNumberColor)
                $(topEl.querySelector(".fc-daygrid-day-number")).attr("selected", true)
            }
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
            textColor: "#434343",
        })
    }
    return parsed
}

// get the events on a particular day
function eventsOnDay(day) {
    let today = day;
    let eventsOnDay = []
    let tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000)
    for (let curEvent of events) {
        let eventStart = new Date(curEvent.start_date)
        let eventEnd = new Date(curEvent.end_date)
        if (eventStart < tomorrow && eventEnd >= today) {
            eventsOnDay.push(curEvent);
        }
    }
    return eventsOnDay;
}

// place all of the relevant cards at the bottom
function placeCards(eventsToday, date) {
    let cards = document.querySelector("#eventDetails").querySelectorAll(".dayEvent")

    // for the first min(cards.length, eventsToday.length) cards, we simply replace them
    for (let i = 0; i < cards.length && i < eventsToday.length; i++) {
        $(cards[i]).stop().fadeOut(100, function () {
            let working = initializeCard(eventsToday[i], date).firstElementChild
            $(working).hide()
            $(this).replaceWith(working)
            $(working).fadeIn(100)
        })
    }

    // if there are extra events, then we fade the extra events in after adding them
    for (let i = cards.length; i < eventsToday.length; i++) {
        let working = initializeCard(eventsToday[i], date)
        $(working.firstElementChild).hide()
        $(working.firstElementChild).fadeIn(100)
        document.querySelector("#eventDetails").appendChild(working)
    }

    // if there are extra cards already on the screen, then we must remove them after fading them out
    for (let i = eventsToday.length; i < cards.length; i++) {
        $(cards[i]).stop().fadeOut(100, function () {
            $(this).remove()
        })
    }

    // if there are no events, then we tell them there are no events
    if (eventsToday.length === 0) {
        $(".no-event-inform").stop().fadeIn(100)
    } else {
        $(".no-event-inform").stop().fadeOut(100)
    }

    // replace the header of the "details" section at the bottom
    $("#details #detailsCurrentDay").html(date.toLocaleDateString(undefined, {
        day: "numeric",
        year: "numeric",
        weekday: "long",
        month: "long"
    }));
}

function initializeCard(curEvent, date, working = null) {
    // if the working card is null, then we must create a new card
    if (working == null) working = document.querySelector("#card").content.cloneNode(true)

    // get the start and end dates for the current event
    let eventStart = new Date(curEvent.start_date);
    let eventEnd = new Date(curEvent.end_date)

    // if the start date is different from the current date, then we must also add the date information
    let [startTime, startAMPM] = eventStart < date ? dateTimeRepresentation(eventStart) : timeRepresentation(eventStart)

    // if the end date is different from the current date, then we must also add the date instead of just the time
    let [endTime, endAMPM] = eventEnd >= new Date(date.getTime() + 24 * 60 * 60 * 1000) ?
        dateTimeRepresentation(eventEnd) : timeRepresentation(eventEnd);

    // insert stuff
    working.querySelector("#event_start").innerHTML = startTime;
    working.querySelector("#event_end").innerHTML = endTime;
    working.querySelector("#event_start_ampm").innerHTML = startAMPM
    working.querySelector("#event_end_ampm").innerHTML = endAMPM
    working.querySelector(".event_title").innerHTML = curEvent.name
    working.querySelector(".event_description").innerHTML = curEvent.description
    // the background color will be the same as the color of the first tag
    working.querySelector(".leftPanel").style = "background-color: " + (curEvent.tags.length > 0 ? curEvent.tags[0].color : "lightblue")
    working.querySelector(".event_host_name").innerHTML = curEvent.organization.name
    // since we cap the height of the event, which it's clicked, we can expand it
    $(working.querySelector(".event_description")).click(function () {
        $(this).toggleClass("truncate-100")
    })

    for (let tag of curEvent.tags) {
        // for each tag in the event, we create a corresponding p and add it to the card
        let tagEl = document.createElement("p")
        tagEl.classList.add("tag")
        tagEl.innerHTML = tag.name
        tagEl.style.backgroundColor = tag.color
        working.querySelector(".tag-section").appendChild(tagEl)
    }

    // return the card
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
