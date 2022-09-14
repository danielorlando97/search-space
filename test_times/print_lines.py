from time import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def plot_time_line(dsl_line, best_line, domain_line, iter=10000, tittle="Simple Test"):

    _, ax = plt.subplots(figsize=(3, 3))

    ax.set_title(tittle, color='C0')

    points = []
    results = []
    start = time()
    for i in range(iter):
        points.append(i)
        dsl_line()
        results.append(time() - start)

    ax.plot(points, results, 'C1', label=f'fast dsl last: time {results[-1]}')

    points = []
    results = []
    start = time()
    for i in range(iter):
        points.append(i)
        best_line()
        results.append(time() - start)

    ax.plot(points, results, 'C2', label=f'best form: last time {results[-1]}')

    points = []
    results = []
    start = time()
    for i in range(iter):
        points.append(i)
        domain_line()
        results.append(time() - start)

    ax.plot(points, results, 'C3',
            label=f'domain dsl: last time {results[-1]}')

    ax.legend()
    plt.show()
