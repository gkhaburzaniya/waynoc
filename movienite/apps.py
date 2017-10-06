from django.apps import AppConfig


class MovieniteConfig(AppConfig):

    def ready(self):
        import movienite.signals
