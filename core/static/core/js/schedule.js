const DateTime = luxon.DateTime;
let scheduleData = [];

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
                            if (todayDate in data && data[todayDate].length > 0) scheduleData = data;
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
                description = `Starting ${DateTime.fromISO(courseData.time.start).toRelative({base: now})}`;
                } else {
                    description = `Ending ${DateTime.fromISO(courseData.time.end).toRelative({base: now})}`;
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
                let todayCoursesEl = $(".schedule-today-courses").empty()
                for (let i = 0; i < todayData.length; i++) {
                    if (todayData[i].course) {
                        let courseEl = $("<span class='schedule-today-course'></span>").text(`${todayData[i].description.course} - ${todayData[i].course}`)
                        if (todayData[i].course === currentCourse) courseEl.attr("data-active", true)
                        todayCoursesEl.append(courseEl)
                        if (i < todayData.length) todayCoursesEl.append($("<br>"))
                    }
                }
            }
        }

        $(document).ready(function () {
            setup();
            var time = 60 - parseInt((new Date().getTime() / 1000) % 60);
            setInterval(update, 1000);
        });
