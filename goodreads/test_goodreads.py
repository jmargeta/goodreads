import os

from nose.tools import assert_equals

from goodreads import GoodreadsClient


def test_authentication():
    """Can authenticate with given credentials."""

    c = GoodreadsClient()
    assert_equals(c.user['name'], 'Jan Skus')
