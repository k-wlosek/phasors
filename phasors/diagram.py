"""
This module contains the Diagram class, which represents a phasor diagram.
"""
from typing import Union
import io
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
from phasors.symbol import Symbol


# noinspection PyUnusedLocal,PyMethodMayBeStatic
class Diagram:
    """
    Represents a phasor diagram.
    """
    def __init__(self, symbols: list[Symbol], title: str, angles_to_draw: list[tuple[int, int, str]]):
        """
        :type symbols: list[Symbol]
        :param symbols: list of symbols
        :type title: str
        :param title: title of the diagram
        :type angles_to_draw: list[tuple[int, int, str]]
        :param angles_to_draw: list of tuples of indices of symbols to draw angles between and color
        """
        self.symbols = symbols
        self.title = title
        self._angles_to_draw = angles_to_draw
        self._counter: int = 1
        self._calculate_scale()

        # Matplotlib objects
        self.ax: Union[None, plt.Axes] = None
        self.fig: Union[None, plt.Figure] = None
        params = {'mathtext.default': 'regular'}
        plt.rcParams.update(params)

        # Variables for drawing phasors
        self.__x_range: Union[list[float], None] = None
        self.__y_range: Union[list[float], None] = None
        self.__x_start: Union[float, None] = None
        self.__y_start: Union[float, None] = None
        self.__x_end: Union[float, None] = None
        self.__y_end: Union[float, None] = None

    def __repr__(self):
        return f'Diagram({repr(self.symbols)}, {repr(self.title)})'

    def __str__(self):
        return f'Diagram({str(self.symbols)}, {str(self.title)})'

    def __eq__(self, other):
        return self.symbols == other.symbols and self.title == other.title

    def __ne__(self, other):
        return self.symbols != other.symbols or self.title != other.title

    def _draw_phasor(self, length: float, angle: float, annotation: str, color: str, j: int) -> None:
        """
        Draws a phasor.
        :type length: float
        :param length: length of the phasor
        :type angle: float
        :param angle: angle of the phasor
        :type annotation: str
        :param annotation: annotation of the phasor
        :type color: str
        :param color: color of the phasor and the annotation
        :type j: int
        :param j: index of the symbol in the symbols list
        """
        length *= self.scales[j]

        self.__x_end: float = self.__x_start + length * np.cos(angle)
        self.__y_end: float = self.__y_start + length * np.sin(angle)

        # Add x and y values for scaling
        self.__x_range.append(self.__x_end)
        self.__x_range.append(self.__x_start)
        self.__y_range.append(self.__y_end)
        self.__y_range.append(self.__y_start)

        self.ax.quiver(
            self.__x_start,
            self.__y_start,
            self.__x_end - self.__x_start,
            self.__y_end - self.__y_start,
            angles='xy',
            scale_units='xy',
            scale=1,
            color=color,
            headlength=3.5,
            headaxislength=3.5
        )

        # Calculate the middle point of the phasor
        middle_x: float = (self.__x_start + self.__x_end) / 2
        middle_y: float = (self.__y_start + self.__y_end) / 2

        # Adjust text position for sideways phasors
        if 45 < np.rad2deg(angle) % 180 < 135:
            self.ax.annotate(
                annotation,
                xy=(middle_x, middle_y),
                xytext=(middle_x + middle_x * 0.1, middle_y - middle_y * 0.1),
                fontsize=10,
                color=color
            )
        elif middle_y == 0:
            self.ax.annotate(
                annotation,
                xy=(middle_x, middle_y),
                xytext=(middle_x + middle_x * 0.1, middle_y + 0.01 * max(self.scales[j], 1)),
                fontsize=10,
                color=color
            )
        else:
            self.ax.annotate(
                annotation,
                xy=(middle_x, middle_y),
                xytext=(middle_x + middle_x * 0.1, middle_y + middle_y * 0.1),
                fontsize=10,
                color=color
            )

        # Set the start of the next phasor
        self.__x_start = self.__x_end
        self.__y_start = self.__y_end

    def _draw_angle(self, angle: float, last_angle: float,
                    center: tuple[float, float], size: float, color: str) -> None:
        """
        Draws angle between last phasor and the current one.
        :type angle: float
        :param angle: angle of the current phasor
        :type last_angle: float
        :param last_angle: angle of the last phasor
        :type center: tuple[float, float]
        :param center: center of the angle shape
        :type size: float
        :param size: radius of the angle shape
        :type color: str
        :param color: color of the angle shape and the text
        :return:
        """
        wedge = Wedge(center, size, np.rad2deg(angle), np.rad2deg(last_angle), color=color, alpha=0.2)
        x_center, y_center = center
        if len(self.symbols) < 3:
            self.ax.annotate(
                f'$φ = {np.rad2deg(last_angle-angle)}°$',
                xy=(x_center + size, y_center + size),
                xytext=(x_center + size, y_center + size),
                fontsize=10,
                color=color
            )
        else:
            self.ax.annotate(
                f'$φ_{self._counter} = {np.rad2deg(last_angle-angle)}°$',
                xy=(x_center + 0.25 * size, y_center + 0.25 * size),
                xytext=(x_center + 0.25 * size + 0.2, y_center + 0.25 * size + 0.1),
                fontsize=10,
                color=color
            )
            self._counter += 1
        self.ax.add_patch(wedge)

    def _calculate_scale(self):
        """
        Calculates the scale of the phasors for each symbol.
        :return: None
        """
        self.scales: list[float] = []
        for symbol in self.symbols:
            # Extract lengths from phasors_list
            lengths: list[float] = [phasor[0] for phasor in symbol]

            # Find the maximum length in both U and I phasors
            max_length: float = np.max(lengths)

            # Define scales for U and I phasors
            scale: float = 1 / max_length

            # Scales for all phasors in a list
            self.scales.append(scale)

    def _draw_angle_between(self) -> None:
        """
        Draws angle between specified symbols,
        specifically, last phasors of those symbols.
        :return: None
        """
        symbol_pairs: tuple[int, int, str]
        symbol1_index: int
        symbol2_index: int
        color: str
        for symbol_pairs in self._angles_to_draw:
            symbol1_index, symbol2_index, color = symbol_pairs
            symbol1 = self.symbols[symbol1_index]
            symbol2 = self.symbols[symbol2_index]

            # Extract lengths of the last phasors for each symbol
            length1: float = symbol1[-1][0] * self.scales[symbol1_index]
            length2: float = symbol2[-1][0]

            # Extract angles of the last phasors for each symbol
            angle1: float = symbol1[-1][1]
            angle2: float = symbol2[-1][1]

            self._draw_angle(angle2, angle1, (0, 0), (length1-length2)/8, color)

    def create(self) -> None:
        """
        Creates the phasor diagram.
        :return: None
        """
        self.fig, (self.ax, ax_side) = plt.subplots(1, 2, width_ratios=[12, 1])
        self.ax.set_aspect('equal', adjustable='box')

        self.__x_range: list[float] = []
        self.__y_range: list[float] = []

        self.__x_start: float = 0
        self.__y_start: float = 0

        for j, symbol in enumerate(self.symbols):
            length: float
            angle: float
            annotation: str
            color: str
            for i, (length, angle, annotation, color) in enumerate(symbol):
                # Skip the last phasor
                if i == len(symbol) - 1:
                    continue

                self._draw_phasor(length, angle, annotation, color, j)

            # Add the last phasor
            length, angle, annotation, color = symbol[-1]
            self.__x_start, self.__y_start = 0, 0
            self._draw_phasor(length, angle, annotation, color, j)

        # Set xlim and ylim based on min and max values
        self.ax.set_xlim(
            min(self.__x_range) * 1.1,
            max(self.__x_range) * 1.1
        )
        self.ax.set_ylim(
            min(self.__y_range) * 1.1,
            max(self.__y_range) * 1.1
        )

        self.ax.set_aspect('auto', adjustable='box')
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
        self.ax.set_title(self.title)

        # Draw angles between specified symbols
        self._draw_angle_between()

        # Set the side diagram, for scale
        ax_side.set_aspect('equal', adjustable='box')

        ax_side.set_ylim(
            min(self.__y_range) * 1.1,
            max(self.__y_range) * 1.1
        )

        # Remove ticks and spines from the side diagram
        ax_side.set_xticks([])
        ax_side.set_xticklabels([])
        ax_side.set_yticks([])
        ax_side.set_yticklabels([])
        ax_side.spines['top'].set_visible(False)
        ax_side.spines['right'].set_visible(False)
        ax_side.spines['bottom'].set_visible(False)
        ax_side.spines['left'].set_visible(False)

        # Plot a vertical line of length 1
        ax_side.plot([0, 0], [1, 0], color='black', linewidth=2)

        # Annotate the line on the right
        annotation: str = ''
        for i, scale in enumerate(self.scales):
            annotation += f'{1/scale} {self.symbols[i].unit}\n'
        ax_side.annotate(
            annotation,
            xy=(0, 1),
            xytext=(0.03, 0.6),
            fontsize=10,
            color='black'
        )

    def show(self) -> None:
        """
        Shows the phasor diagram.
        :return: None
        """
        plt.show()

    def save(self, filename: str, filetype: str = "png") -> None:
        """
        Saves the phasor diagram.
        :type filetype: str
        :param filetype: file type to save the diagram as, default is png
        :type filename: str
        :param filename: name of the file
        :return: None
        """
        self.fig.savefig(filename, format=filetype, dpi=200, bbox_inches='tight')

    def save_as_bytes(self, filetype: str = "png") -> io.BytesIO:
        """
        Saves the phasor diagram as bytes.
        :type filetype: str
        :param filetype: file type to save the diagram as, default is png
        :return: figure as bytes
        :rtype: io.BytesIO
        """
        buf = io.BytesIO()
        self.fig.savefig(buf, format=filetype, dpi=200, bbox_inches='tight')
        buf.seek(0)
        return buf
