from core.value_objects import CustomerId
from core.storage import DiskStorage as Storage


class Customer(object):
    customer_id = None

    def __init__(self, id: CustomerId):
        self.customer_id = id

    def getStorage(self) -> Storage:
        return Storage(self.customer_id)
