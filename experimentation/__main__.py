from . import simple_experimentation as se
from .import unique_experimentation as ue
import sys

print(sys.argv[1:])
exp, i, n = tuple(sys.argv[1:])
n = int(n)

if exp == 'set':
    ue.set_randint(n, f'_{i}')
    ue.dsl_set(n, f'_{i}')
    exit(0)

if exp == 'set2':
    ue.set_2_randint(n, f'_{i}')
    ue.dsl_2_set(n, f'_{i}')
    exit(0)

if exp == 'matrix':
    ue.matrix_randint(n, f'_{i}')
    ue.dsl_matrix(n, f'_{i}')

if exp == 'even':
    ue.even_find_trap_plus(n)
    ue.even_find_trap(n)
    ue.even_find_randint(n)
    ue.even_find_dsl(n)

if exp == 'even_fixed':
    ue.even_find_randint_fixed(n, 2)
    ue.even_find_dsl_fixed(n, 2)
    ue.even_find_fixed_limits(n, 2)

if exp == 'basic':
    se.dsl_vs_randint_int()
    se.dsl_vs_randint_list_int()
    se.dsl_vs_randint_class()
    se.dsl_choice()

if exp == 'center':
    se.center_point(n)
