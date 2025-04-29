import numpy as np
from abc import ABC, abstractmethod


class Calculate(ABC):
    @staticmethod
    @abstractmethod
    def calculate(values):
        pass


class Average(Calculate):
    """ Класс для вычисления среднего значения в массиве"""

    @staticmethod
    def calculate(values):
        """
        Возвращает среднее значение в массиве.

        Parameters
        ----------
        values: np.ndarray
            Массив значений.

        Returns
        -------
        float
            Среднее значение в массиве.
        """

        return np.mean(values)


class Min(Calculate):
    """ Класс для вычисления минимального значения в массиве"""

    @staticmethod
    def calculate(values):
        """
        Возвращает минимальное значение в массиве.

        Parameters
        ----------
        values: np.ndarray
            Массив значений.

        Returns
        -------
        float
            Минимальное значение в массиве.
        """

        return np.min(values)


class Max(Calculate):
    """ Класс для вычисления максимального значения в массиве"""

    @staticmethod
    def calculate(values):
        """
        Возвращает максимальное значение в массиве.

        Parameters
        ----------
        values: np.ndarray
            Массив значений.

        Returns
        -------
        float
            Максимальное значение в массиве.
        """

        return np.max(values)


class Median(Calculate):
    """ Класс для вычисления медианного значения в массиве"""

    @staticmethod
    def calculate(values):
        """
        Возвращает медианное значение в массиве.

        Parameters
        ----------
        values: np.ndarray
            1D массив значений.

        Returns
        -------
        float
            Медианное значение в массиве.
        """
        assert values.ndim == 1, "values: Ожидался 1D массив"

        sorted_values = sorted(values)
        idx = int(len(sorted_values) // 2)
        return sorted_values[idx]


class Top(Calculate):
    """ Класс для вычисления первого значения в массиве"""

    @staticmethod
    def calculate(values):
        """
        Возвращает первое значение в массиве.

        Parameters
        ----------
        values: np.ndarray
            1D массив значений.

        Returns
        -------
        float
            Первое значение в массиве.
        """
        assert values.ndim == 1, "values: Ожидался 1D массив"

        return values[0]


class MostFrequent(Calculate):
    """ Класс для вычисления наиболее часто встречаемого значения в массиве"""

    @staticmethod
    def calculate(values):
        """
        Возвращает наиболее часто встречаемое значение в массиве.

        Parameters
        ----------
        values: np.ndarray
            Массив значений.

        Returns
        -------
        float
            Наиболее часто встречаемое значение в массиве.
        """

        uniq_values, counts = np.unique(values, return_counts=True)
        return uniq_values[np.argmax(counts)]


class LessFrequent(Calculate):
    """ Класс для вычисления наименее часто встречаемого значения в массиве"""

    @staticmethod
    def calculate(values):
        """
        Возвращает наименее часто встречаемое значение в массиве.

        Parameters
        ----------
        values: np.ndarray
            Массив значений.

        Returns
        -------
        float
            Наименее часто встречаемое значение в массиве.
        """
        uniq_values, counts = np.unique(values, return_counts=True)
        return uniq_values[np.argmin(counts)]
