import uuid


class CustomerId(uuid.UUID):
    def __init__(self, *args, **kwargs):
        kwargs["version"] = 4
        super(CustomerId, self).__init__(*args, **kwargs)

    def getCustomer(self):
        import core.customer

        return core.customer.Customer(self)
