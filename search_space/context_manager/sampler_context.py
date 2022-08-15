class SamplerInfo:
    def __init__(self, scope, domain, sampler_value, real_value) -> None:
        self.scope = scope
        self.domain = domain
        self.sampler_value = sampler_value
        self.real_value = real_value

    def __str__(self) -> str:
        return f'{self.scope.scope}[{self.domain}] ---> {self.sampler_value} ---> {self.real_value}'


class ConstraintInfo:
    def __init__(self, scope, constraint_name, initial_domain, result) -> None:
        self.scope = scope
        self.initial_domain = initial_domain
        self.result = result
        self.constraint_name = constraint_name

    def __str__(self) -> str:
        return f'{self.scope.scope}[{self.initial_domain}] ---> {self.constraint_name} ---> {self.result}'


class InitSamplerInfo:
    def __init__(self, scope, domain) -> None:
        self.scope = scope
        self.domain = domain

    def __str__(self) -> str:
        return f'Sampler in {self.scope.scope}[{self.domain}]:'


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
        result, index = [], 0
        while index < len(self.sampler_logs):
            r, index = self.__print_history(index=index)
            result += r

        print('\n'.join(result))

    def __print_history(self, index=0, tabs=''):
        result = [tabs + str(self.sampler_logs[index])]
        index += 1
        while index < len(self.sampler_logs):
            log = self.sampler_logs[index]
            if isinstance(log, InitSamplerInfo):
                r, index = self.__print_history(index, tabs + '\t')
                result += r
            else:
                result.append(tabs + '\t' + str(log))
                if isinstance(log, SamplerInfo):
                    return result, index + 1
                index += 1
        return result, index
