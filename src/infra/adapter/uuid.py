from uuid import uuid4
from domain.ports import UuidInterface

class Uuid(UuidInterface):

    def generate_uuid(self):
        return str(uuid4())
