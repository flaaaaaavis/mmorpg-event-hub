from django.apps import AppConfig


class AwardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.awards'

    def ready(self) -> None:
        # import signal handlers
        try:
            import apps.awards.signals  # noqa: F401
        except Exception:
            # avoid import errors during migrations or test discovery
            pass
