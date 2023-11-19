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

            # Calculate the middle point of the last phasor
            middle_x = (x_start + x_end) / 2
            middle_y = (y_start + y_end) / 2

            # Adjust text position for the last phasor (always above)
            self.ax.annotate(
                annotation,
                xy=(middle_x, middle_y),
                xytext=(middle_x + 0.2, middle_y + 0.7),
                fontsize=8,
                color=color
            )

        # Calculate sum x and y values
        p: tuple[float, float, str, str]
        max_x: list[float] = []
        for symbol in self.symbols:
            max_x.append(max([p[0] * np.cos(p[1]) for p in symbol]))
        max_y: list[float] = []
        for symbol in self.symbols:
            max_y.append(max([p[0] * np.sin(p[1]) for p in symbol]))

        # Set xlim and ylim based on maximum values
        self.ax.set_xlim(-1, max(max_x) * 1.2)
        self.ax.set_ylim(-1, max(max_y) * 1.2)
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
        plt.savefig(filename)

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
