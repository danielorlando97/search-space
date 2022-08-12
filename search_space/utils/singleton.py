class Singleton(type):
    _instances = None

    def __call__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances
