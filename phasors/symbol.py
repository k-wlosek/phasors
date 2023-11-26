"""
This module contains the Symbol class, which represents a symbol in a phasor diagram.
"""
import dataclasses
from typing import Union
import numpy as np


# noinspection PyMethodMayBeStatic
@dataclasses.dataclass
class Symbol:
    """
    Represents a symbol in a phasor diagram.
    ex. [(1, 0, 'V_1', 'red'), (1, 1.25, 'V_2', 'blue'), (1, 3.14, 'V_3', 'green')]
    All angles are in radians.

    One symbol is represented by a list of tuples, where each tuple represents a phasor.
    """
    def __init__(self, data_list: list[Union[tuple[float, float, str, str], str]]):
        phasors: list[tuple[float, float, str, str]] = []
        _data_list = data_list.copy()
        self.unit = self._prepare_annotation(_data_list.pop(-1))
        for phasor in _data_list:
            length, angle, annotation, color = phasor
            angle_rad = np.deg2rad(angle)
            phasors.append((length, angle_rad, self._prepare_annotation(annotation), color))
        self.phasors = phasors

    def _prepare_annotation(self, annotation: str) -> str:
        """
        Prepares annotation for LaTeX rendering.
        :param annotation: string for preparation
        :return: prepared string
        :rtype: str
        """
        underscore_location = annotation.find('_')
        return "$" + annotation[:underscore_location + 1] + "{" + annotation[underscore_location + 1:] + "}$"

    @staticmethod
    def from_list(data_list: list[list[Union[tuple[float, float, str, str], str]]]):
        """
        Returns a list of symbols from a list of lists of tuples representing data for each symbol.
        :type data_list: list[list[Union[tuple[float, float, str, str], str]]]
        :param data_list: list of lists of tuples representing data for each symbol
        :return: list of symbols
        :rtype: list[Symbol]
        """
        symbols = []
        symbol_list: list[Union[tuple[float, float, str, str], str]]
        for symbol_list in data_list:
            symbols.append(Symbol(symbol_list))
        return symbols

    def __iter__(self):
        return iter(self.phasors)

    def __getitem__(self, item):
        return self.phasors[item]

    def __len__(self):
        return len(self.phasors)

    def __repr__(self):
        return f'Symbol({repr(self.phasors)})'

    def __str__(self):
        str_rep = ""
        for value, angle, annotation, color in self.phasors:
            str_rep += f'Value: {value}, angle (rad): {angle}, annotation: {annotation}, color: {color}\n'
        return str_rep

    def __eq__(self, other):
        return self.phasors == other.phasors

    def __ne__(self, other):
        return self.phasors != other.phasors
