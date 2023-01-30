from core.config import settings

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
    "logstash",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
        "logstash": {
            "()": "logstash_async.formatter.LogstashFormatter",
            "message_type": "python-logstash",
            "fqdn": False,
            "extra_prefix": "dev",
            "extra": {
                "environment": "production",
            },
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "logstash": {
            "level": "INFO",
            "class": "logstash_async.handler.AsynchronousLogstashHandler",
            "formatter": "logstash",
            "transport": "logstash_async.transport.UdpTransport",
            "host": settings.logstash.port,
            "port": settings.logstash.host,
            "ssl_enable": False,
            "ssl_verify": False,
            "database_path": "./logstash.db",
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["logstash"],
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}
