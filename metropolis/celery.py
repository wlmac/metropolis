import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metropolis.settings")

app = Celery("Metropolis")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    import core.tasks as tasks
    from celery.schedules import crontab

    sender.add_periodic_task(crontab(hour=0, minute=0), tasks.delete_expired_users)
    sender.add_periodic_task(crontab(hour=18, minute=0), tasks.notif_events_singleday)
    sender.add_periodic_task(crontab(day_of_month=1), tasks.run_group_migrations)
    sender.add_periodic_task(
        crontab(hour=1, minute=0), tasks.oauth2_clear_expired
    )  # Delete expired oauth2 tokens from db everyday at 1am

    # sender.add_periodic_task(
    #     crontab(hour=8, minute=0, day_of_week="mon-fri"), tasks.fetch_announcements
    # )

    sender.add_periodic_task(crontab(hour=4, minute=0), tasks.fetch_calendar_events)
