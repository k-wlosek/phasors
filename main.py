"""
    Main file of the project.
"""
from typing import Union
import base64
from src.diagram import Diagram
from src.symbol import Symbol

phasors_list: list[list[Union[tuple[float, float, str, str]], str]] = [
    [
        (66.48, 0, "U_R1", "green"),
        (169.67, 90, "U_L1", "blue"),
        (-88.2, 90, "U_M", "black"),
        (58.94, 0, "U_R2", "green"),
        (162.51, 90, "U_L2", "blue"),
        (-88.2, 90, "U_M", "black"),
        (200, 51.16, "U", "pink"),
        "V"
    ],
    [
        (0.53, 0, "I", "red"),
        "A"
    ]
]

symbols: list[Symbol] = Symbol.from_list(phasors_list)
d = Diagram(symbols, "Wykres fazorowy dla pomiaru 1 w sprzężeniu przeciwnym", [(0, 1, "red")])
d.create()
d.show()
d.save("zad2_1.png", "png")
d.save("zad2_1.svg", "svg")
byte = d.save_as_bytes("svg")
byte.seek(0)
print(base64.b64encode(byte.read()).decode('UTF-8'))
