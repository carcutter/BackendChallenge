from typing import Any, Dict, List, Tuple, Union


class Singleton(type):
    """
    A metaclass for a class that should behave as singleton.
    """

    def __init__(cls, class_name: str, class_bases: Union[List, Tuple], class_attrs: Dict) -> None:
        """
        Initializes an instance of the singleton class.

        :param class_name:      A string containing the name of the class
        :type:                  str
        :param class_bases:     A tuple of classes from which the current class derives
        :type:                  tuple
        :param class_attrs:     A dictionary of all methods and fields defined in the class
        :type:                  dict
        """
        super(Singleton, cls).__init__(class_name, class_bases, class_attrs)
        cls.__instance = None

    def __call__(cls, *args: Union[List, Tuple], **kwargs: Dict) -> Any:
        """
        "Magic" method, that is called when singleton-based class is called.
        Creates an instance of the singleton-based class.

        :param args:            Any necessary positional arguments
        :type:                  list or tuple
        :param args:            Any necessary keyword arguments
        :type:                  dict

        :return:                Created instance of the singleton-based class
        :rtype:                 Any
        """
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instance
