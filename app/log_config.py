from logging.config import dictConfig


client = google.cloud.logging.Client()
client.setup_logging()

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(lineno)d %(funcName)s %(message)s"
            }
        },
        "handlers": {
            "google_cloud": {
                "level": "DEBUG",
                "class": "google.cloud.logging.handlers.CloudLoggingHandler",
                "formatter": "verbose",
                "client": client,
            },
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            },
        },
        "loggers": {
            "main_logger": {
                "handlers": ["google_cloud"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
)
