from ast import arg


def decorated_all_methods(decorator):
    def f(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return f


def check_ast_precedence(fun):
    def f(*args, **kws):
        if len(args) == 2:

            _self = args[0]
            other = args[1]

            try:
                p = other.precedence
            except AttributeError:
                p = -1

            if p > _self.precedence:

                f = getattr(other, fun.__name__)
                return f(_self).reverse()
        return fun(*args, **kws)
    f.__name__ = fun.__name__
    return f


def check_params_type(typ_fun, class_fun):
    def ff(func):

        def f(*args, **kws):
            new_args = []
            for arg in args:
                if isinstance(arg, typ_fun()):
                    new_args.append(arg)
                else:
                    new_args.append(class_fun(arg))
            return func(*new_args, **kws)
        f.__name__ = func.__name__
        return f
    return ff


def index_list(shape):
    dp = [[i] for i in range(shape[0])]

    for dim in range(1, len(shape)):
        dp = [current_index + [i] for current_index in dp for i in range(dim)]

    return dp
