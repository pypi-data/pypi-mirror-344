import logging
import os

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.utils import OperationalError
from django.http import HttpResponse
from django_redis import get_redis_connection

from .azure_helper import get_db_password, get_redis_credentials

logger = logging.getLogger("pulumi_django_azure.health_check")


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _self_heal(self):
        # Send HUP signal to gunicorn main thread,
        # which will trigger new workers to start.
        os.kill(os.getppid(), 1)

    def __call__(self, request):
        if request.path == settings.HEALTH_CHECK_PATH:
            # Update the database credentials if needed
            if settings.AZURE_DB_PASSWORD:
                try:
                    current_db_password = settings.DATABASES["default"]["PASSWORD"]
                    new_db_password = get_db_password()

                    if new_db_password != current_db_password:
                        logger.debug("Database password has changed, updating credentials")
                        settings.DATABASES["default"]["PASSWORD"] = new_db_password

                        # Close existing connections to force reconnect with new password
                        connection.close()
                    else:
                        logger.debug("Database password unchanged, keeping existing credentials")
                except Exception as e:
                    logger.error("Failed to update database credentials: %s", str(e))
                    self._self_heal()
                    return HttpResponse(status=503)

            # Update the Redis credentials if needed
            if settings.AZURE_REDIS_CREDENTIALS:
                try:
                    current_redis_password = settings.CACHES["default"]["OPTIONS"]["PASSWORD"]
                    redis_credentials = get_redis_credentials()

                    if redis_credentials.password != current_redis_password:
                        logger.debug("Redis password has changed, updating credentials")

                        # Re-authenticate the Redis connection
                        redis_connection = get_redis_connection("default")
                        redis_connection.execute_command("AUTH", redis_credentials.username, redis_credentials.password)

                        settings.CACHES["default"]["OPTIONS"]["PASSWORD"] = redis_credentials.password
                    else:
                        logger.debug("Redis password unchanged, keeping existing credentials")
                except Exception as e:
                    logger.error("Failed to update Redis credentials: %s", str(e))
                    self._self_heal()
                    return HttpResponse(status=503)

            try:
                # Test the database connection
                connection.ensure_connection()
                logger.debug("Database connection check passed")

                # Test the Redis connection
                cache.set("health_check", "test")
                logger.debug("Redis connection check passed")

                return HttpResponse("OK")

            except Exception as e:
                logger.error("Health check failed with unexpected error: %s", str(e))
                logger.warning("Self-healing by gracefully restarting workers.")
                self._self_heal()
                return HttpResponse(status=503)

        return self.get_response(request)
