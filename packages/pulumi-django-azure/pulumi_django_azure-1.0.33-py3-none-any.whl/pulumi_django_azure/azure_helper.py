import base64
import json
import logging
import os
from dataclasses import dataclass
from subprocess import check_output

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.resource.subscriptions.models import Subscription

logger = logging.getLogger("pulumi_django_azure.azure_helper")


# Azure credentials
AZURE_CREDENTIAL = DefaultAzureCredential()

# Get the local IP addresses of the machine (only when runnig on Azure)
if os.environ.get("IS_AZURE_ENVIRONMENT"):
    LOCAL_IP_ADDRESSES = check_output(["hostname", "--all-ip-addresses"]).decode("utf-8").strip().split(" ")
else:
    LOCAL_IP_ADDRESSES = []


def get_db_password() -> str:
    """
    Get a valid password for the database.
    """
    token = AZURE_CREDENTIAL.get_token("https://ossrdbms-aad.database.windows.net/.default")

    logger.debug("New database token: %s", token)

    return token.token


@dataclass
class RedisCredentials:
    username: str
    password: str


def get_redis_credentials() -> RedisCredentials:
    """
    Get valid credentials for the Redis cache.
    """
    token = AZURE_CREDENTIAL.get_token("https://redis.azure.com/.default")

    logger.debug("New Redis token: %s", token)

    return RedisCredentials(_extract_username_from_token(token), token)


def get_subscription() -> Subscription:
    """
    Get the subscription for the current user.
    """
    subscription_client = SubscriptionClient(AZURE_CREDENTIAL)
    subscriptions = list(subscription_client.subscriptions.list())
    return subscriptions[0]


def _extract_username_from_token(token: str) -> str:
    """
    Extract the username from the JSON Web Token (JWT) token.
    """
    parts = token.split(".")
    base64_str = parts[1]

    if len(base64_str) % 4 == 2:
        base64_str += "=="
    elif len(base64_str) % 4 == 3:
        base64_str += "="

    json_bytes = base64.b64decode(base64_str)
    json_str = json_bytes.decode("utf-8")
    jwt = json.loads(json_str)

    return jwt["oid"]
