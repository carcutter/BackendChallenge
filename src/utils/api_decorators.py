from functools import wraps
from uuid import uuid4


class ApiDecorators:

    MOCK_CUSTOMER_ID = str(uuid4())

    @staticmethod
    def require_customer_id(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(ApiDecorators.MOCK_CUSTOMER_ID, *args, **kwargs)

        return decorated_function
