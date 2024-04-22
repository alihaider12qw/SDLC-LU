import os


def is_postgres():
    return os.getenv("TOOSIMPLEQ_TEST_DB", "postgres") == "postgres"


class FakeException(Exception):
    """An artification exception to simulate an unexpected error"""
