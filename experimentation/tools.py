import csv
import matplotlib.pyplot as plt
import pandas as pd
import random


def save_csv(header, data, name):
    try:
        f = open(f'experimentation/csv/{name}.csv',
                 'x', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(header)
    except Exception:
        f = open(f'experimentation/csv/{name}.csv',
                 'a', encoding='UTF8', newline='')
        writer = csv.writer(f)

    writer.writerows(data)
    f.close()


class Plotting:
    def __init__(self) -> None:
        self.data = []

    def append(self, X, Y, name):
        self.data.append((X, Y, name))

    def append_data_set(self, data, name, xlabel, ylabel):
        self.data.append((data, name, ylabel, xlabel))

    def multiplot(self):
        _, ax = plt.subplots(len(self.data), 1, figsize=(10, 10))

        for i, data in enumerate(self.data):
            X, Y, name = data

            ax[i].plot(X, Y, f'C{i+1}', label=name)
            ax[i].grid(True)
            ax[i].legend()

        _ = plt.plot()

    def hmultiplot(self, save=False):
        _, ax = plt.subplots(1, len(self.data), figsize=(20, 6))

        for i, data in enumerate(self.data):
            data, title, left_name, bottom_name = data
            for j, _data in enumerate(data):
                X, Y, name = _data

                ax[i].plot(X, Y, f'C{j+1}', label=name)
                ax[i].grid(True)
                ax[i].set_xlabel(left_name)
                ax[i].set_ylabel(bottom_name)
                ax[i].set_title(title)
                ax[i].legend()

        if save:
            plt.savefig(f'{save}.png')
        else:
            _ = plt.plot()

    def plot(self):
        _, ax = plt.subplots(figsize=(10, 10))

        for i, data in enumerate(self.data):
            X, Y, name = data

            ax.plot(X, Y, f'C{i+1}', label=name)

        ax.grid(True)
        ax.legend()
        _ = plt.plot()

    def save(self, _name):
        _, ax = plt.subplots(figsize=(10, 10))

        for i, data in enumerate(self.data):
            X, Y, name = data

            ax.plot(X, Y, f'C{i+1}', label=name)

        ax.grid(True)
        ax.legend()
        plt.savefig(f'{_name}.png')


def run_test(f, _iter, name):
    result = []

    print(name)
    for i in range(_iter):
        print(f"!!!!! {i} !!!!!!!!", end='\r')
        result.append(f(i))
    print('!!!!! END !!!!!!!!')
    return result


def mean(data):
    result = [0] * len(data)

    for items in data:
        for i, item in enumerate(items):
            result[i] += item

    return [s/len(data) for s in result]


def statics_test(f, _iter, name):
    result = []

    print(name)
    for i in range(_iter):
        temp = []
        ff = f(i)
        for j in range(30):
            print(f"!!!!! {i} - {j} !!!!!!!!", end='\r')
            temp.append(ff())

        temp = mean(temp)
        result.append([i] + temp[1:])

    print('!!!!! END !!!!!!!!')
    return result


def computing_time(times):
    Y = [0]

    for v in times:
        Y.append(v + Y[-1])

    Y.pop(0)
    return Y


def randint(a, b):
    value = random.uniform(a, b)
    decimal = value - int(value)
    return int(value) if decimal <= 0.5 else int(value) + 1


def choice(domain):
    index = randint(0, len(domain) - 1)
    return domain[index]
