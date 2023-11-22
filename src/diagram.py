"""
This module contains the Diagram class, which represents a phasor diagram.
"""
from typing import Union
import io
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
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
        self._counter: int = 1
        self._calculate_scale()
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

    def _draw_angle(self, angle: float, last_angle: float, center: tuple[float, float], size: float) -> None:
        """
        Draws angle between last phasor and the current one.
        :param angle:
        :param last_angle:
        :return:
        """
        wedge = Wedge(center, size, np.rad2deg(angle), np.rad2deg(last_angle), color='black', alpha=0.2)
        x_center, y_center = center
        if len(self.symbols) < 3:
            self.ax.annotate(
                f'$\\phi = {np.rad2deg(last_angle-angle)}$',
                xy=(x_center + size, x_center + size),
                xytext=(x_center + size, x_center + size),
                fontsize=10,
                color='red'
            )
        else:
            self.ax.annotate(
                f'$\\phi_{self._counter} = {np.rad2deg(last_angle-angle)}$',
                xy=(x_center + 0.25 * size, x_center + 0.25 * size),
                xytext=(x_center + 0.25 * size + 0.2, x_center + 0.25 * size + 0.1),
                fontsize=10,
                color='red'
            )
            self._counter += 1
        self.ax.add_patch(wedge)

    def _calculate_scale(self):
        """
        Calculates the scale of the phasor diagram.
        :return: None
        """
        # TODO: Fix this method, it currently expects only two symbols!!!
        # Extract lengths from phasors_list
        lengths_U = [phasor[0] for phasor in self.symbols[0]]
        lengths_I = [phasor[0] for phasor in self.symbols[1]]

        # Find the maximum length in both U and I phasors
        max_length_U = np.max(lengths_U)
        max_length_I = np.max(lengths_I)

        # Define scales for U and I phasors
        scale_U = 1 / max_length_U
        scale_I = 1 / max_length_I

        # Scales for all phasors in a list
        self.scales = [scale_U, scale_I]

    def create(self) -> None:
        """
        Creates the phasor diagram.
        :return: None
        """
        # self.fig, self.ax = plt.subplots()
        self.fig, (self.ax, ax_side) = plt.subplots(1, 2, width_ratios=[12, 1])
        self.ax.set_aspect('equal', adjustable='box')

        x_range: list[float] = []
        y_range: list[float] = []

        x_start: float = 0
        y_start: float = 0

        for j, symbol in enumerate(self.symbols):
            if j != 0:
                should_draw_angle: bool = True
                last_angle = angle
                last_length = length
            else:
                should_draw_angle: bool = False
            length: float
            angle: float
            annotation: str
            color: str
            for i, (length, angle, annotation, color) in enumerate(symbol):
                # Skip the last phasor
                if i == len(symbol) - 1:
                    continue

                length *= self.scales[j]

                x_end: float = x_start + length * np.cos(angle)
                y_end: float = y_start + length * np.sin(angle)

                if i == 0 and should_draw_angle:
                    self._draw_angle(angle, last_angle, (x_start, y_start), (last_length-length)/8)
                    should_draw_angle = False

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
                x_start = x_end
                y_start = y_end

            # Add the last phasor
            length, angle, annotation, color = symbol[-1]
            if should_draw_angle:
                print((last_length-length)/8, last_length, length, last_length-length)
                self._draw_angle(angle, last_angle, (x_start, y_start), (last_length-length)/4)
                should_draw_angle = False
            length *= self.scales[j]
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
            # Calculate the middle point of the phasor
            middle_x: float = (x_start + x_end) / 2
            middle_y: float = (y_start + y_end) / 2
            if 45 < angle % 180 < 135:
                self.ax.annotate(
                    annotation,
                    xy=(middle_x, middle_y),
                    xytext=(middle_x + middle_x * 0.4, middle_y + middle_y * 0.2),
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
                    xytext=(middle_x + middle_x * 0.1, middle_y + middle_y * 0.2),
                    fontsize=10,
                    color=color
                )

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

        ax_side.set_aspect('equal', adjustable='box')
        # ax_side.set_xlim(
        #     0.01,
        #     0.01
        # )
        ax_side.set_ylim(
            min(y_range) * 1.1,
            max(y_range) * 1.1
        )
        # ax_side.axhline(0, color='black', linewidth=0.5)
        # ax_side.axvline(0, color='black', linewidth=0.5)
        # ax_side.grid(color='gray', linestyle='--', linewidth=0.5)
        ax_side.set_xticks([])  # This will remove the x-axis ticks
        ax_side.set_xticklabels([])  # This will remove the x-axis labels
        ax_side.set_yticks([])  # This will remove the y-axis ticks
        ax_side.set_yticklabels([])  # This will remove the y-axis labels
        ax_side.spines['top'].set_visible(False)
        ax_side.spines['right'].set_visible(False)
        ax_side.spines['bottom'].set_visible(False)
        ax_side.spines['left'].set_visible(False)

        # Plot a vertical line of length 1
        ax_side.plot([0, 0], [1, 0], color='black', linewidth=2)

        # Annotate the line on the right
        ax_side.annotate(
            f'{1/self.scales[0]} V\n{1/self.scales[1]} A',
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

    def save(self, filename: str, format: str = "png") -> None:
        """
        Saves the phasor diagram.
        :param filename: name of the file
        :return: None
        """
        self.fig.savefig(filename, format=format, dpi=200, bbox_inches='tight')

    def save_as_bytes(self, format: str = "png") -> io.BytesIO:
        """
        Saves the phasor diagram as bytes.
        :return: figure as bytes
        :rtype: io.BytesIO
        """
        buf = io.BytesIO()
        self.fig.savefig(buf, format=format, dpi=200, bbox_inches='tight')
        buf.seek(0)
        return buf
