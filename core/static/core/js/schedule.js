const DateTime = luxon.DateTime;
const Duration = luxon.Duration;
let scheduleData = [];

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
    // load schedule data differently depending on whether the user is offline
    if (typeof index_page_data !== 'undefined') {
        // not offline: load data from index page
        scheduleData = index_page_data;
        localStorage.setItem('scheduleData', JSON.stringify(scheduleData));
    }
    else {
        // offline: load data from localStorage
        let localScheduleData = localStorage.getItem('scheduleData');
        if (localScheduleData) {
            scheduleData = JSON.parse(localScheduleData);
        }
    }
    update();
}

function update() {
    let currentCourse;
    let description;
    let todayData;
    let todayScheduleIsPersonal = false;

    const now = getDateTimeNow();

    if (now.toISODate() in scheduleData) {
        let todayScheduleData = scheduleData[now.toISODate()];
        todayData = todayScheduleData.schedule;
        todayScheduleIsPersonal = todayScheduleData.is_personal;

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
        if (todayData.length > 0) {
            $(".schedule-cycle").text(todayData[0].cycle);
        } else {
            $(".schedule-cycle").empty()
        }
        let todayCoursesEl = $(".schedule-today-courses").empty();
        for (let i = 0; i < todayData.length; i++) {
            if (todayData[i].course) {
                let courseDescription;
                if (todayScheduleIsPersonal) courseDescription = `${todayData[i].description.course} - ${todayData[i].course}`;
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
