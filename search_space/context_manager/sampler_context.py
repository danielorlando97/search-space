class SamplerInfo:
    def __init__(self, scope, domain, sampler_value, real_value) -> None:
        self.scope = scope
        self.domain = domain
        self.sampler_value = sampler_value
        self.real_value = real_value

    def __str__(self) -> str:
        pass


class ConstraintInfo:
    def __init__(self, scope, constraint_name, initial_domain, result) -> None:
        self.scope = scope
        self.initial_domain = initial_domain
        self.result = result
        self.constraint_name = constraint_name

    def __str__(self) -> str:
        pass


class SamplerContext:
    def __init__(self) -> None:
        self.sampler_logs = []
        self.context = {}
        self.result = None

    def push_log(self, log):
        self.sampler_logs.append(log)

    def registry_sampler(self, search_space, value):
        self.context[search_space] = value

    def get_sampler_value(self, search_space):
        try:
            return self.context[search_space]
        except KeyError:
            return None

    def print_history(self):
        pass
