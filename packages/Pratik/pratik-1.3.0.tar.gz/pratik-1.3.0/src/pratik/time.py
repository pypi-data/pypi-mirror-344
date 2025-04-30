import datetime

from pratik.functions import progress_bar


class TimeRemaining:
    def __init__(self, numbers):
        """ Calculate the average remaining time

        :param numbers: Number of objects
        :type numbers: int
        """
        self.iterations = 0
        self.numbers = numbers
        self._start = datetime.datetime.now()

    def add(self, number: int = 1):
        self.iterations += number

    def remove(self, number: int = 1):
        self.iterations -= number

    def progress_bar(self, *, width: int = 100):
        passed = datetime.datetime.now() - self._start
        restant = str(((passed * self.numbers) / self.iterations) - passed).split('.')[0]
        progress_bar(self.iterations, self.numbers, width=width)
        print(f" {restant}", end='')
