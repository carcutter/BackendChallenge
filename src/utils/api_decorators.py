from functools import wraps
from typing import Callable

from flask import current_app


from core.value_objects import CustomerId

class ApiDecorators:

    @staticmethod
    def require_customer_id(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'customer_id' not in kwargs:
                raise KeyError('customer_id value not provided in the URL')
            kwargs['customer_id'] = CustomerId(kwargs['customer_id'])

            return f(*args, **kwargs)

        return decorated_function
