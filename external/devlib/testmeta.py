#! /usr/bin/env python3

from functools import wraps
import inspect

class InitCheckpointMeta(type):
    """
    Metaclass providing an ``initialized`` boolean attributes on instances.

    ``initialized`` is set to ``True`` once the ``__init__`` constructor has
    returned. It will deal cleanly with nested calls to ``super().__init__``.
    """
    def __new__(metacls, name, bases, dct, **kwargs):
        cls = super().__new__(metacls, name, bases, dct, **kwargs)
        init_f = cls.__init__

        @wraps(init_f)
        def init_wrapper(self, *args, **kwargs):
            self.initialized = False

            # Track the nesting of super()__init__ to set initialized=True only
            # when the outer level is finished
            try:
                stack = self._init_stack
            except AttributeError:
                stack = []
                self._init_stack = stack

            stack.append(init_f)
            try:
                x = init_f(self, *args, **kwargs)
            finally:
                stack.pop()

            if not stack:
                self.initialized = True
                del self._init_stack

            return x

        cls.__init__ = init_wrapper

        return cls


class InitCheckpoint(metaclass=InitCheckpointMeta):
    """
    Inherit from this class to set the :class:`InitCheckpointMeta` metaclass.
    """
    pass

class C(InitCheckpoint):
    def __init__(self):
        print('__init__ C')
        assert not self.initialized

class D(C):
    def __init__(self):
        assert not self.initialized
        super().__init__()
        assert not self.initialized
        print('__init__ D')

class D2(C):
    def __init__(self):
        assert not self.initialized
        super().__init__()
        assert not self.initialized
        print('__init__ D2')

class E(D, D2):
    def __init__(self):
        assert not self.initialized
        super().__init__()
        assert not self.initialized
        print('__init__ E')

o = E()
assert o.initialized
