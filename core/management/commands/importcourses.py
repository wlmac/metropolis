import json

from django.core.management.base import BaseCommand, CommandError

from core import models


class InvalidCourseJSONFileError(Exception):
    pass


class Command(BaseCommand):
    help = "Imports courses as specified in the JSON file provided"

    def add_arguments(self, parser):
        parser.add_argument(
            "term_id", type=int, help="ID of the Term object to add courses to"
        )
        parser.add_argument(
            "json_file", type=str, help="JSON file to import courses from"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Just show what courses will be updated or skipped; don't actually write them.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        data = []

        try:
            term = models.Term.objects.get(pk=options["term_id"])
        except models.Term.DoesNotExist:
            raise CommandError(f'Term #{options["term_id"]} does not exist')

        try:
            with open(options["json_file"], "r") as f:
                dirty_data = json.load(f)

                if not isinstance(dirty_data, list):
                    raise InvalidCourseJSONFileError

                for course_json in dirty_data:
                    if not isinstance(course_json, dict):
                        raise InvalidCourseJSONFileError

                    if "code" not in course_json or "position" not in course_json:
                        raise InvalidCourseJSONFileError

                    if not isinstance(course_json["code"], str) or not isinstance(
                        course_json["position"], int
                    ):
                        raise InvalidCourseJSONFileError

                    data.append(
                        {
                            "code": course_json["code"],
                            "position": course_json["position"],
                        }
                    )
        except FileNotFoundError:
            raise CommandError("Specified file does not exist")
        except json.decoder.JSONDecodeError:
            raise CommandError("Specified file is not a valid JSON file")
        except InvalidCourseJSONFileError:
            raise CommandError("Invalid JSON format")

        num_courses_added = 0
        num_courses_updated = 0
        num_courses_unmodified = 0

        for course_json in data:
            course_code = course_json["code"]
            course_position = course_json["position"]

            try:
                course = models.Course.objects.get(term=term, code=course_code)

                if course.position == course_position:
                    num_courses_unmodified += 1

                    self.stdout.write(
                        self.style.NOTICE(f"Skipped course {course_code}")
                    )
                else:
                    course_previous_position = course.position

                    course.position = course_position
                    if not dry_run:
                        course.save()

                    num_courses_updated += 1

                    self.stdout.write(
                        self.style.NOTICE(
                            f"Updated course {course_code} from position {course_previous_position} to {course_position}"
                        )
                    )
            except models.Course.DoesNotExist:
                if not dry_run:
                    models.Course.objects.create(
                        term=term, code=course_code, position=course_position
                    )

                num_courses_added += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{num_courses_added} courses added, {num_courses_updated} updated, {num_courses_unmodified} unmodified."
            )
        )
