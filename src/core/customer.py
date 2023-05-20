from uuid import uuid4


class Customer(object):

    @staticmethod
    def get_id() -> str:
        return str(uuid4())
