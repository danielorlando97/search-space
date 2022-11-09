from unittest import result
from search_space.context_manager.runtime_manager import SearchSpacePrinter
from search_space.errors import UnSupportOpError
from search_space.utils.singleton import Singleton
from search_space.utils import visitor
from search_space.spaces.asts import constraints
from typing import Iterable
from search_space.utils.itertools import is_iterable


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
        self.ast_space = '|||'

    def init_search(self, id_space, name_space):
        tabs = self.tabs * '\t'

        print(f"""{tabs} _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
{tabs}| Init Sample By {Color.f_green(name_space)} Space Id: {Color.f_red(id_space)}""")

    def context_name(self, context):
        tabs = self.tabs * '\t'

        names = []
        while not context.father is None:
            names.append(context.name)
            context = context.father

        names.append(context.name)
        names.reverse()

        print(
            f"""{tabs}| {Color.b_yellow('Context')}: {' -> '.join(names)}""")

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

    def sample_value(self, value, caching_value=False):
        tabs = self.tabs * '\t'

        if type(value) in [list, tuple]:
            result = "[\n"
            for i, item in enumerate(value):
                result += f'{tabs}| {i} -> {item},\n'
            result += f'{tabs}| ]'
        else:
            result = value

        print(f"""{tabs}| Sample Result [Is Caching: {Color.f_blue(caching_value)}]
{tabs}| {Color.b_green('Value')}: {result}
{tabs}|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _""")

    def sample_error(self, sample, error, sample_num, domain):

        tabs = self.tabs * '\t'

        if is_iterable(sample):
            result = "[\n"
            for i, item in enumerate(sample):
                result += f'{tabs}| {i} -> {item},\n'
            result += f'{tabs}| ]'
        else:
            result = sample

        if isinstance(domain, type):
            name = domain.__name__
        else:
            name = domain.__class__.__name__

        try:
            limits = domain.limits
        except:
            limits = None

        print(f"""{tabs}{Color.b_red('_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')}
{tabs}| Invalid Sampler [Sampler: {result}] [Sample Numbs: {sample_num}] [Domain Type: {name}] [Domain Limits: {Color.f_red(limits)}]
{tabs}| Error: {error}
{tabs}{Color.b_red('|_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _')}""")

    def ast_transformation(self, domain, ast, visitor_name=''):
        tabs = self.tabs * '\t'

        if isinstance(domain, type):
            name = domain.__name__
        else:
            name = domain.__class__.__name__

        try:
            limits = domain.limits
        except:
            limits = None

        print(f"""{tabs}_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
{tabs}{Color.b_green(f'| AST Transform: {visitor_name}]')} [Domain Type: {name}][Domain Limits: {Color.f_red(limits)}]""")
        self.pivot_tab = self.tabs
        self.visit(ast)
        print(f"""{tabs}{Color.b_blue('| ')}_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _""")

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(constraints.AstRoot)
    def visit(self, node: constraints.AstRoot):
        self.tabs += 1

        for n in node.asts:
            self.visit(n)

        self.tabs -= 1

    @visitor.when(constraints.UniversalVariableBinaryOperation)
    def visit(self, node):
        init_tab = self.pivot_tab * '\t'
        tabs = (self.tabs - self.pivot_tab) * self.ast_space

        print(
            f"""{init_tab}{Color.b_blue(f'| ')}{tabs} {node.__class__.__name__}:""")
        self.tabs += 1
        self.visit(node.target)
        self.visit(node.other)
        self.tabs -= 1

    @visitor.when(constraints.GetItem)
    def visit(self, node):
        init_tab = self.pivot_tab * '\t'
        tabs = (self.tabs - self.pivot_tab) * self.ast_space

        print(
            f"""{init_tab}{Color.b_blue(f'| ')}{tabs} {node.__class__.__name__}:""")
        self.tabs += 1
        self.visit(node.target)
        self.visit(node.other)
        self.tabs -= 1

    @visitor.when(constraints.GetAttr)
    def visit(self, node):
        init_tab = self.pivot_tab * '\t'
        tabs = (self.tabs - self.pivot_tab) * self.ast_space

        print(
            f"""{init_tab}{Color.b_blue(f'| ')}{tabs} {node.__class__.__name__}:""")
        self.tabs += 1
        self.visit(node.target)
        self.visit(node.other)
        self.tabs -= 1

    @visitor.when(constraints.SelfNode)
    def visit(self, node):
        init_tab = self.pivot_tab * '\t'
        tabs = (self.tabs - self.pivot_tab) * self.ast_space

        print(
            f"""{init_tab}{Color.b_blue(f'| ')}{tabs} {Color.f_blue(node.__class__.__name__)}""")

    @visitor.when(constraints.NaturalValue)
    def visit(self, node):
        init_tab = self.pivot_tab * '\t'
        tabs = (self.tabs - self.pivot_tab) * self.ast_space

        value = node.target

        try:
            value = (value.space_name, hash(value.a))
        except UnSupportOpError:
            value = type(value)
        except AttributeError:
            pass

        print(
            f"""{init_tab}{Color.b_blue(f'| ')}{tabs} {Color.f_yellow(node.__class__.__name__)}({value})""")

    # @visitor.when(FunctionNode)
    # def visit(self, node: FunctionNode, current_index):
    #     new_args = []
    #     for arg in node.args:
    #         new_args.append(self.visit(arg, current_index))

    #     new_kw = {}
    #     for name, arg in node.kwargs:
    #         new_kw[name] = self.visit(arg, current_index)

    #     return FunctionNode(node.func, new_args, new_kw)
