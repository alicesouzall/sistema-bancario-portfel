import re
import pytest

from src.infra.adapter.uuid import Uuid

def test_should_generate_a_not_empty_uuid():
    uuid = Uuid().generate_uuid()

    assert uuid != ""

def test_should_correctly_generate_a_uuid():
    uuid = Uuid().generate_uuid()
    uuid_regex = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

    assert re.match(uuid_regex, uuid)
