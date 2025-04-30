import pytest
import crlite_python


def test_sum_as_string():
    assert crlite_python.sum_as_string(1, 1) == "2"
