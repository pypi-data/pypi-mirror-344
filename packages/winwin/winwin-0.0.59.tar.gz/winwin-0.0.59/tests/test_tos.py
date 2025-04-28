# ruff: noqa: T201
from os import environ

import pytest

from winwin.tos import TosFs


@pytest.fixture
def fs():
    return create_fs()


def create_fs():
    return TosFs(
        access_key=environ["TOS_ACCESS_KEY"],
        secret_key=environ["TOS_SECRET_KEY"],
        endpoint=environ["TOS_ENDPOINT"],
        region=environ["TOS_REGION"],
        bucket=environ["TOS_BUCKET"],
    )


def test_tos(fs):
    fs.write("test/test.txt", b"hello world")
    assert fs.exists("test/test.txt")
    assert fs.open("test/test.txt").read() == b"hello world"
