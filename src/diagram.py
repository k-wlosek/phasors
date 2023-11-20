"""
This module contains the Diagram class, which represents a phasor diagram.
"""
from typing import Union
import io
import matplotlib.pyplot as plt
import numpy as np
from src.symbol import Symbol


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class Diagram:
    """
    Represents a phasor diagram.
    """
    def __init__(self, symbols: list[Symbol], title: str):
        """
        :type symbols: list[Symbol]
        :param symbols: list of symbols
        :type title: str
        :param title: title of the diagram
        """
        self.symbols = symbols
        self.title = title
        self.ax: Union[None, plt.Axes] = None
        self.fig: Union[None, plt.Figure] = None
        params = {'mathtext.default': 'regular'}
        plt.rcParams.update(params)

    def __repr__(self):
        return f'Diagram({repr(self.symbols)}, {repr(self.title)})'

    def __str__(self):
        return f'Diagram({str(self.symbols)}, {str(self.title)})'

    def __eq__(self, other):
        return self.symbols == other.symbols and self.title == other.title

    def __ne__(self, other):
        return self.symbols != other.symbols or self.title != other.title

    def create(self) -> None:
        """
        Creates the phasor diagram.
        :return: None
        """
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', adjustable='box')

        x_range: list[float] = []
        y_range: list[float] = []

        x_start: float = 0
        y_start: float = 0

        for symbol in self.symbols:
            length: float
            angle: float
            annotation: str
            color: str
            for i, (length, angle, annotation, color) in enumerate(symbol):
                # Skip the last phasor
                if i == len(symbol) - 1:
                    continue
                x_end: float = x_start + length * np.cos(angle)
                y_end: float = y_start + length * np.sin(angle)

                # Add x and y values for scaling
                x_range.append(x_end)
                x_range.append(x_start)
                y_range.append(y_end)
                y_range.append(y_start)

                self.ax.quiver(
                    x_start,
                    y_start,
                    x_end - x_start,
                    y_end - y_start,
                    angles='xy',
                    scale_units='xy',
                    scale=1,
                    color=color,
                    headlength=3.5,
                    headaxislength=3.5
                )

                # Calculate the middle point of the phasor
                middle_x: float = (x_start + x_end) / 2
                middle_y: float = (y_start + y_end) / 2

                # Adjust text position for sideways phasors
                if 45 < angle % 180 < 135:
                    self.ax.annotate(
                        annotation,
                        xy=(middle_x, middle_y),
                        xytext=(middle_x + 0.2, middle_y + 0.1),
                        fontsize=8,
                        color=color
                    )
                else:
                    self.ax.annotate(
                        annotation,
                        xy=(middle_x, middle_y),
                        xytext=(middle_x + 0.2, middle_y + 0.2),
                        fontsize=8,
                        color=color
                    )

                # Set the start of the next phasor
                x_start = x_end
                y_start = y_end

            # Add the last phasor
            length, angle, annotation, color = symbol[-1]
            x_start, y_start = 0, 0
            x_end = x_start + length * np.cos(angle)
            y_end = y_start + length * np.sin(angle)

            # Add x and y values for scaling
            x_range.append(x_end)
            x_range.append(x_start)
            y_range.append(y_end)
            y_range.append(y_start)

            self.ax.quiver(
                x_start,
                y_start,
                x_end - x_start,
                y_end - y_start,
                angles='xy',
                scale_units='xy',
                scale=1,
                color=color,
                headlength=3.5,
                headaxislength=3.5
            )

        # Add -3 to both ranges if min value is 0, so the phasors are not on the edge of the diagram
        if 0 in x_range:
            x_range.append(-3)
        if 0 in y_range:
            y_range.append(-3)
        # Set xlim and ylim based on min and max values
        self.ax.set_xlim(
            min(x_range) * 1.1,
            max(x_range) * 1.1
        )
        self.ax.set_ylim(
            min(y_range) * 1.1,
            max(y_range) * 1.1
        )

        self.ax.set_aspect('auto', adjustable='box')
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        self.ax.set_title(self.title)

    def show(self) -> None:
        """
        Shows the phasor diagram.
        :return: None
        """
        plt.show()

    def save(self, filename: str) -> None:
        """
        Saves the phasor diagram.
        :param filename: name of the file
        :return: None
        """
        self.fig.savefig(filename)

    def save_as_bytes(self) -> io.BytesIO:
        """
        Saves the phasor diagram as bytes.
        :return: figure as bytes
        :rtype: io.BytesIO
        """
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png', dpi=200, bbox_inches='tight')
        buf.seek(0)
        return buf
