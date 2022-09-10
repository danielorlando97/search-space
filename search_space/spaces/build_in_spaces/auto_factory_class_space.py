import inspect
from search_space.spaces import SearchSpace
import types

__all__ = ['custom_space', 'parameters_space_description']


def custom_space(cls):
    dispatchers = {}
    for attr in cls.__dict__:
        if '$$$' in attr:
            method = getattr(cls, attr)
            dispatchers[attr.split('$$$')[0]] = method

    for attr in cls.__dict__:  # there's propably a better way to do this
        method = getattr(cls, attr)
        if callable(method) and not isinstance(method, DispatchedSpace):
            try:
                dispatcher = dispatchers[attr]
            except KeyError:
                dispatcher = DispatchedSpace(attr)
                dispatchers[attr] = dispatcher

            dispatcher.cls = cls
            setattr(cls, attr, calls(dispatcher)(method))

    return ClassSpace(cls, dispatchers)


def parameters_space_description(fn):
    frame = inspect.currentframe().f_back
    func_name = fn.func_name if 'func_name' in dir(fn) else fn.__name__

    try:
        dispatcher = frame.f_locals[f'{func_name}$$$domain']
    except KeyError:
        dispatcher = DispatchedSpace(func_name)
        frame.f_locals[f'{func_name}$$$domain'] = dispatcher

    try:
        function = frame.f_locals[func_name]
        dispatcher.calls_fn = function
    except KeyError:
        function = fn

    dispatcher.given_fn = fn
    return function


def calls(dispatcher):
    def f(fn):

        dispatcher.calls_fn = fn

        def ff(*args, **kw):
            return dispatcher(*args, **kw)
        ff.dispatcher = dispatcher
        return ff
    return f


class ClassSpace(SearchSpace, type):
    def __init__(self, cls, dispatchers) -> None:
        super().__init__(None, None, [])
        self.cls = cls
        self.dispatchers = dispatchers

    def __call__(self, *args, **kwds):
        return self.cls(*args, **kwds)

    def __ast_optimization__(self, ast_list):

        for item in self.dispatchers.values():
            for func in ast_list:
                item.ast_constraint.add_constraint(
                    self.__build_constraint__(func))

        return self


# class ClassMemberSpace:
#     pass


class DispatchedSpace(SearchSpace):
    def __init__(self, fn_name) -> None:
        super().__init__(None, None, [])
        self.given_fn = None
        self.calls_fn = None
        self.cls = None
        self.fn_name = fn_name

    def __call__(self, instance, *args, **kwds):
        if len(args) != 0:
            return self.__call(self, *args, **kwds)

        return self.get_sample(local_domain=(instance, kwds))

    def __sampler__(self, domain, context):
        instance, kwds = domain

        if self.calls_fn is None:
            getattr(super(self.cls, instance), self.fn_name)(**kwds)

    def __call(self, *args, **kwds):
        if self.calls_fn is None:
            return super(self.cls, self)[self.fn_name](*args, **kwds)

        return self.calls_fn(*args, **kwds)
