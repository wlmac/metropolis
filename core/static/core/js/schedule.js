const DateTime = luxon.DateTime;
const Duration = luxon.Duration;
let scheduleData = [];
let scheduleIsPersonal = false;

function formatHours(hours) {
    return `${hours} ${hours == 1 ? "hour" : "hours"}`;
}

function formatMinutes(minutes) {
    return `${minutes} ${minutes == 1 ? "minute" : "minutes"}`;
}

function formatSeconds(seconds) {
    return `${seconds} ${seconds == 1 ? "second" : "seconds"}`;
}

function formatHMS(hours, minutes, seconds) {
    if (hours > 0) { // e.g. 2 hours 25 minutes
        return `${formatHours(hours)} ${formatMinutes(minutes)}`
    } else if (minutes >= 10) { // e.g. 15 minutes
        return `${formatMinutes(minutes)}`
    } else if (minutes > 0) { // e.g. 5 minutes 26 seconds
        return `${formatMinutes(minutes)} ${formatSeconds(seconds)}`
    } else { // e.g. 26 seconds
        return `${formatSeconds(seconds)}`
    }
}

function formatTimeIntervalDuration(startTime, endTime) {
    let duration_milliseconds = startTime.until(endTime).toDuration().toMillis();
    let duration = Duration.fromObject({ hours: 0, minutes: 0, seconds: 0, milliseconds: duration_milliseconds }).normalize();
    return formatHMS(duration.hours, duration.minutes, duration.seconds);
}

function getDateTimeNow() {
    return DateTime.now();
}

function setup() {
    fetch('/api/term/current')
        .then(response => response.json())
        .then(data => {
            fetch(`/api/term/${data.id}/schedule/week`)
                .then(response => response.json())
                .then(data => {
                    scheduleData = data;
                    fetch(`/api/me/schedule/week`)
                        .then(response => {
                            if (!response.ok) throw new Error(`Status ${response.status} received`);
                            return response.json();
                        })
                        .then(data => {
                            const todayDate = getDateTimeNow().toISODate();
                            if (todayDate in data && data[todayDate].length > 0) {
                                scheduleData = data;
                                scheduleIsPersonal = true;
                            }
                            update();
                        })
                        .catch(err => {
                            console.error('Fetch me_schedule_week request failed', err);
                        });
                })
        })
        .catch(err => {
            console.error('Fetch term_current request failed', err);
        });
}

function update() {
    let currentCourse;
    let description;
    let todayData;

    const now = getDateTimeNow();

    if (now.toISODate() in scheduleData) {
        todayData = scheduleData[now.toISODate()];
        let courseData;

        for (const course of todayData) {
            if (course.course && now <= DateTime.fromISO(course.time.end)) {
                courseData = course;
                break;
            }
        }

        if (courseData) {
            currentCourse = courseData.course;

            if (now < DateTime.fromISO(courseData.time.start)) {
                description = `Starting in ${formatTimeIntervalDuration(now, DateTime.fromISO(courseData.time.start))}`;
            } else {
                description = `Ending in ${formatTimeIntervalDuration(now, DateTime.fromISO(courseData.time.end))}`;
            }
        } else {
            if (todayData.length > 0) {
                currentCourse = 'School Over';
                description = 'Enjoy your evening!';
            } else {
                currentCourse = 'No School';
                description = 'Enjoy your day!';
            }
        }
    } else {
        currentCourse = "Unknown";
        description = "We were unable to fetch your schedule.";
    }

    $(".schedule-course").text(currentCourse);
    $(".schedule-description").text(description);

    if (todayData) {
        if (todayData.length > 0) $(".schedule-cycle").text(todayData[0].cycle);
        let todayCoursesEl = $(".schedule-today-courses").empty();
        for (let i = 0; i < todayData.length; i++) {
            if (todayData[i].course) {
                let courseDescription;
                if (scheduleIsPersonal) courseDescription = `${todayData[i].description.course} - ${todayData[i].course}`;
                else courseDescription = `${todayData[i].description.course}`;

                let courseEl = $("<span class='schedule-today-course'></span>").text(courseDescription);
                if (todayData[i].course === currentCourse) courseEl.attr("data-active", true);
                todayCoursesEl.append(courseEl);
                if (i < todayData.length) todayCoursesEl.append($("<br>"));
            }
        }
    }
}

$(document).ready(function () {
    setup();
    setInterval(update, 1000);
});
