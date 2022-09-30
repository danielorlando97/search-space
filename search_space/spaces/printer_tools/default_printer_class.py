from search_space.context_manager.runtime_manager import SearchSpacePrinter
from search_space.utils.singleton import Singleton


class Color:
    @staticmethod
    def formatter(text, color): return f'\x1b[{color}m{text}\x1b[0m'

    @staticmethod
    def f_red(text):
        return Color.formatter(text, 31)

    @staticmethod
    def f_green(text):
        return Color.formatter(text, 32)

    @staticmethod
    def f_blue(text):
        return Color.formatter(text, 96)

    @staticmethod
    def f_yellow(text):
        return Color.formatter(text, 33)

    @staticmethod
    def b_red(text):
        return Color.formatter(f'\x1b[30m{text}', 41)

    @staticmethod
    def b_green(text):
        return Color.formatter(f'\x1b[30m{text}', 42)

    @staticmethod
    def b_blue(text):
        return Color.formatter(f'\x1b[30m{text}', 44)

    @staticmethod
    def b_yellow(text):
        return Color.formatter(f'\x1b[30m{text}', 43)


class DefaultPrinter(SearchSpacePrinter, metaclass=Singleton):

    def __init__(self) -> None:
        self.tabs = 0

    def init_search(self, id_space, name_space):
        tabs = self.tabs * '\t'

        print(f"""{tabs} _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
{tabs}| Init Sample By {Color.f_green(name_space)} Space Id: {Color.f_red(id_space)}""")

#         print(f"""{tabs} _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
# {tabs}| Init Sample By
# {tabs}| Space Name: {name_space}
# {tabs}| Space Id: {id_space}
# {tabs}|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _""")

    def sample_value(self, value, caching_value=False):
        tabs = self.tabs * '\t'

        result = "[\n"
        try:
            for i, item in enumerate(value):
                result += f'{tabs}| {i} -> {item},\n'

            result += f'{tabs}| ]'
        except TypeError:
            result = value

        print(f"""{tabs}| Sample Result [Is Caching: {Color.f_blue(caching_value)}]
{tabs}| {Color.b_green('Value')}: {result}
{tabs}|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _""")

    def domain_init(self, domain):

        tabs = self.tabs * '\t'

        if isinstance(domain, type):
            name = domain.__name__
        else:
            name = domain.__class__.__name__

        try:
            limits = domain.limits
        except:
            limits = None

        print(
            f"""{tabs}| Sampler Domain Init [Domain Type: {name}] [Domain Limits: {Color.f_red(limits)}]""")

    def sample_error(self, sample, error, sample_num):

        tabs = self.tabs * '\t'

        result = "[\n"
        try:
            for i, item in enumerate(sample):
                result += f'{tabs}| {i} -> {item},\n'

            result += f'{tabs}| ]'
        except TypeError:
            result = sample

        print(f"""{tabs}{Color.b_red('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')}
{tabs}| Invalid Sampler [Sampler: {result}] [Sample Numbs: {sample_num}]
{tabs}| Error: {error}
{tabs}{Color.b_red('|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')}""")
