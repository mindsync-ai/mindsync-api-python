from mindsync.api import AsyncApi
from mindsync.exc import MindsyncCliError

# import json
import inspect


class CliHandler:
    def __init__(self):
        # make method stubs
        def create_method(name):
            def method(**kwargs):
                api = self.__api
                if not api:
                    raise MindsyncCliError('Api object is not binded')

                func = getattr(api, name)
                return func(**kwargs)
            return method

        methods = inspect.getmembers(AsyncApi, predicate=inspect.isfunction)
        print(methods)
        for m in methods:
            name, _ = m
            if '__' not in name:
                setattr(self, name, create_method(name))


    def bind(self, api):
        if api is None:
            raise ValueError('Invalid argument')

        self.__api = api
