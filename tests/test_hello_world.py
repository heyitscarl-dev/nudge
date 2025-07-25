import pytest

from nudge import hello_world

def test_hello_world():
    assert hello_world.hello_world() == ":)"

def test_hello_world_broken():
    with pytest.raises(Exception):
        hello_world.hello_world_broken()
