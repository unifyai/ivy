# global
import os
from pathlib import Path

import redis
from hypothesis import HealthCheck, settings
from hypothesis.database import (
    DirectoryBasedExampleDatabase,
    MultiplexedDatabase,
    ReadOnlyDatabase,
)
from hypothesis.extra.redis import RedisExampleDatabase
from pytest import mark

hypothesis_cache = os.getcwd() + "/.hypothesis/examples/"
redis_connect = None
try:
    os.makedirs(hypothesis_cache)
except FileExistsError:
    pass


def is_db_available():
    global redis_connect
    redis_connect = redis.Redis.from_url(
        url="redis://redis-17011.c259.us-central1-2.gce.cloud.redislabs.com:17011",
        username="general_use",
        password="Hypothesiscache@123",
        max_connections=2,
    )
    try:
        redis_connect.get("b")
    except redis.exceptions.ConnectionError:
        print("Fallback to DirectoryBasedExamples")
        return False
    return True


def pytest_addoption(parser):
    parser.addoption(
        "--num-examples",
        action="store",
        default=5,
        type=int,
        help="set max examples generated by Hypothesis",
    )
    parser.addoption(
        "--deadline",
        action="store",
        default=500000,
        type=int,
        help="set deadline for testing one example",
    )


def pytest_configure(config):
    profile_settings = {}
    getopt = config.getoption
    max_examples = getopt("--num-examples")
    deadline = getopt("--deadline")
    if os.getenv("REDIS_URL", default=False) and os.environ["REDIS_URL"]:
        print("Update Database with examples !")
        db = redis.Redis.from_url(
            os.environ["REDIS_URL"], password=os.environ["REDIS_PASSWD"]
        )
        profile_settings["database"] = RedisExampleDatabase(
            db, key_prefix=b"hypothesis-example:"
        )

    elif is_db_available():
        print("Use Database in ReadOnly Mode with local caching !")
        shared = RedisExampleDatabase(redis_connect, key_prefix=b"hypothesis-example:")
        profile_settings["database"] = MultiplexedDatabase(
            DirectoryBasedExampleDatabase(path=hypothesis_cache),
            ReadOnlyDatabase(shared),
        )

    else:
        print("Database unavailable, local caching only !")
        profile_settings["database"] = DirectoryBasedExampleDatabase(
            path=hypothesis_cache
        )

    if max_examples:
        profile_settings["max_examples"] = max_examples
    if deadline:
        profile_settings["deadline"] = deadline

    settings.register_profile(
        "ivy_profile",
        **profile_settings,
        suppress_health_check=(HealthCheck(3), HealthCheck(2)),
        print_blob=True,
    )
    settings.load_profile("ivy_profile")


skip_ids = []
skips_path = Path(__file__).parent / "skips.txt"
if skips_path.exists():
    with open(skips_path) as f:
        for line in f:
            if line.startswith("ivy_tests"):
                id_ = line.strip("\n")
                skip_ids.append(id_)


def pytest_collection_modifyitems(items):
    skip_ivy = mark.skip(reason="ivy skip - see ivy_tests/skips.txt for details")
    for item in items:
        # skip if specified in skips.txt
        for id_ in skip_ids:
            if item.nodeid.startswith(id_):
                item.add_marker(skip_ivy)
                break
