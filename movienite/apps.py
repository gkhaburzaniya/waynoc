from django.apps import AppConfig


class MovieniteConfig(AppConfig):
    name = 'movienite'

    def ready(self):
        import movienite.signals
