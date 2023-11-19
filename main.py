import matplotlib.pyplot as plt
import numpy as np


def prepare_annotations(phasors: list[tuple[float, float, str, str]]) -> list[tuple[float, float, str, str]]:
    prepared = []
    for length, angle, annotation, color in phasors:
        # Prepare annotation for LaTeX rendering
        underscore_location: int = annotation.find('_')
        annotation: str = "$" + annotation[:underscore_location + 1] + "{" + annotation[underscore_location + 1:] + "}$"
        prepared.append((length, angle, annotation, color))
    return prepared


def create_phasor_diagram(phasors: list[tuple[float, float, str, str]], title: str) -> None:
    ax: plt.Axes
    fig: plt.Figure
    fig, ax = plt.subplots()
    params: dict[str, str] = {'mathtext.default': 'regular'}
    plt.rcParams.update(params)
    ax.set_aspect('equal', adjustable='box')

    x_start: float
    y_start: float
    x_start, y_start = 0, 0

    last_phasor: tuple[float, float, str, str] = phasors.pop(len(phasors) - 1)

    length: float
    angle: float
    annotation: str
    color: str
    for i, (length, angle, annotation, color) in enumerate(phasors):
        angle_rad: np.ufunc = np.deg2rad(angle)

        x_end: float = x_start + length * np.cos(angle_rad)
        y_end: float = y_start + length * np.sin(angle_rad)

        ax.quiver(
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
            ax.annotate(
                annotation,
                xy=(middle_x, middle_y),
                xytext=(middle_x + 0.2, middle_y + 0.1),
                fontsize=8,
                color=color
            )
        else:
            ax.annotate(
                annotation,
                xy=(middle_x, middle_y),
                xytext=(middle_x + 0.2, middle_y + 0.2),
                fontsize=8,
                color=color
            )

        x_start, y_start = x_end, y_end

    # Draw the last phasor, which is always starting from the (0, 0) point
    length, angle, annotation, color = last_phasor
    angle_rad = np.deg2rad(angle)
    x_start, y_start = 0, 0
    x_end = x_start + length * np.cos(angle_rad)
    y_end = y_start + length * np.sin(angle_rad)
    ax.quiver(
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
    ax.annotate(annotation, xy=(middle_x, middle_y), xytext=(middle_x + 0.2, middle_y + 0.7), fontsize=8, color=color)

    # Calculate sum x and y values
    max_x: float = sum([abs(p[0]) * np.cos(np.deg2rad(p[1])) for p in phasors])
    max_y: float = sum([abs(p[0]) * np.sin(np.deg2rad(p[1])) for p in phasors])
    print(max_y)

    # Set xlim and ylim based on maximum values
    ax.set_xlim(-1, max_x * 1.2)
    ax.set_ylim(-1, max_y * 1.2)
    ax.set_aspect('auto', adjustable='box')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.set_title(title)

    plt.show()


phasors_list: list[tuple[float, float, str, str]] = [
        (3, 0, "U_R1", "green"),
        (2, 90, "U_L1", "blue"),
        (1, 90, "U_M", "black"),
        (3, 0, "U_R2", "green"),
        (2, 90, "U_L2", "blue"),
        (1, 90, "U_M", "black"),
        (8.5, 45, "U", "pink")
]
prepared_phasors: list[tuple[float, float, str, str]] = prepare_annotations(phasors_list)
print(prepared_phasors)
create_phasor_diagram(prepared_phasors, "Wykres fazorowy napięć w połączeniu szeregowym cewek sprzężonych zgodnie")
