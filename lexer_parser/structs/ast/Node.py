from abc import ABC, abstractmethod
from ..parhl_exceptions import ParhlException

class Node(ABC):    

    def handle_exception(method):
        def handle(self, ctx):
            try:
                return method(self, ctx)
            except ParhlException as pe:
                if not pe.line:
                    raise pe.with_line(self.lineno)
                raise pe
            except Exception as e:
                # print("Unhandled exception")
                # TODO: In production we must handle this exception somehow
                # for dev we just raise the exception since we want to debug
                raise e
        return handle

    @abstractmethod
    def gen_impl(self, context):
        pass

    @handle_exception
    def gen(self, context):
        return self.gen_impl(context)

    def __init__(self, lineno):
        self.lineno = lineno