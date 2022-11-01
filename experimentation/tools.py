import csv
import matplotlib.pyplot as plt


def save_csv(header, data, name):
    with open(f'experimentation/csv/{name}.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write multiple rows
        writer.writerows(data)


class Plotting:
    def __init__(self) -> None:
        self.data = []

    def append(self, X, Y, name):
        self.data.append((X, Y, name))

    def plot(self):
        _, ax = plt.subplots(figsize=(10, 10))

        for i, data in enumerate(self.data):
            X, Y, name = data

            ax.plot(X, Y, f'C{i+1}', label=name)

        ax.legend()
        _ = plt.plot()

    def save(self, _name):
        _, ax = plt.subplots(figsize=(10, 10))

        for i, data in enumerate(self.data):
            X, Y, name = data

            ax.plot(X, Y, f'C{i+1}', label=name)

        ax.legend()
        plt.savefig(f'{_name}.png')


def run_test(f, _iter, name):
    result = []

    print(name)
    for i in range(_iter):
        print(f"!!!!! {i} !!!!!!!!", end='\r')
        result.append(f(i))

    return result


def computing_time(times):
    Y = [0]

    for v in times:
        Y.append(v + Y[-1])

    Y.pop(0)
    return Y
