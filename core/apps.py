from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        """
        Clears any useless comments.
        """
        from core.models import Comment

        Comment.scrub()
