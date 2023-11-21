"""
    Main file of the project.
"""
from src.diagram import Diagram
from src.symbol import Symbol

phasors_list: list[list[tuple[float, float, str, str]]] = [
    [
        (66.27, 0, "U_R1", "green"),
        (169.13, 90, "U_L1", "blue"),
        (-87.92, 90, "U_M", "black"),
        (58.76, 0, "U_R2", "green"),
        (162, 90, "U_L2", "blue"),
        (-87.92, 90, "U_M", "black"),
        (200, 57.25, "U", "pink")
    ],
    [
        (0.53, 0, "I", "red")
    ]
]

phasors_list2 = [
    [
        (181.56, 68.60, "U_LR1", "green"),
        (172.32, 70.06, "U_LR2", "green"),
        (-87.91, 90, "U_M", "black"),
        (-87.91, 90, "U_M", "black"),
        (199.70, 57.2, "U", "pink")
    ]
]

symbols: list[Symbol] = Symbol.from_list(phasors_list)
d = Diagram(symbols, "Wykres fazorowy dla pomiaru 1 w sprzężeniu przeciwnym")
d.create()
d.show()
# d.save("fazor4.png")
byte = d.save_as_bytes()
print(byte)
