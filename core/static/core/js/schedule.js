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
    indexPageData = $("#index-page-data").text()
    if (indexPageData) {
        // not offline: load data from index page
        scheduleData = JSON.parse(indexPageData);
        localStorage.setItem('scheduleData', indexPageData);
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
    let todayScheduleData;
    let todaySchedule;
    let todayCycle;
    let scheduleIsPersonal;

    const now = getDateTimeNow();

    if (now.toISODate() in scheduleData) {
        todayScheduleData = scheduleData[now.toISODate()];
        todaySchedule = todayScheduleData.schedule;
        todayCycle = "Day " + todayScheduleData.cycle;
        scheduleIsPersonal = todayScheduleData.is_personal;
        let courseData;

        for (const course of todaySchedule) {
            if (course.description.course && now <= DateTime.fromISO(course.time.end)) {
                courseData = course;
                break;
            }
        }

        if (courseData) {
            currentCourse = courseData.description.course;

            if (now < DateTime.fromISO(courseData.time.start)) {
                description = `Starting in ${formatTimeIntervalDuration(now, DateTime.fromISO(courseData.time.start))}`;
            } else {
                description = `Ending in ${formatTimeIntervalDuration(now, DateTime.fromISO(courseData.time.end))}`;
            }
        } else {
            if (todaySchedule.length > 0) {
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

    if(scheduleIsPersonal) {
        $(".schedule-course").text(currentCourse);
    } else if(currentCourse === "School Over" || currentCourse === "No School") {
        $(".schedule-course").text(currentCourse);
    } else {
        $(".schedule-course").text(todayCycle + " " + currentCourse);
    }
    $(".schedule-description").text(description);

    if (todaySchedule) {
        if (todaySchedule.length > 0) {
            $(".schedule-cycle").text(todayCycle);
        } else {
            $(".schedule-cycle").empty();
        }
        let todayCoursesEl = $(".schedule-today-courses").empty();
        for (let i = 0; i < todaySchedule.length; i++) {
            if (todaySchedule[i].description.course) {
                let courseDescription = `${todaySchedule[i].description.time} : ${todaySchedule[i].description.course}`;

                let courseEl = $("<span class='schedule-today-course'></span>").text(courseDescription);
                if (todaySchedule[i].description.course === currentCourse) courseEl.attr("data-active", true);
                todayCoursesEl.append(courseEl);
                if (i < todaySchedule.length) todayCoursesEl.append($("<br>"));
            }
        }
    }
}

$(document).ready(function () {
    setup();
    setInterval(update, 1000);
});
