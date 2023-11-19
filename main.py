from src.diagram import Diagram
from src.symbol import Symbol

phasors_list: list[list[tuple[float, float, str, str]]] = [
    [
        (3, 0, "U_R1", "green"),
        (2, 90, "U_L1", "blue"),
        (1, 90, "U_M", "black"),
        (3, 0, "U_R2", "green"),
        (2, 90, "U_L2", "blue"),
        (1, 90, "U_M", "black"),
        (8.5, 45, "U", "pink")
    ],
    [
        (2, 0, "I_R1", "blue"),
        (1, 90, "I_L1", "black"),
        (0.5, 90, "I_M", "green"),
        (1.5, 0, "I_R2", "blue"),
        (1, 90, "I_L2", "black"),
        (0.5, 90, "I_M", "green"),
        (4.25, 45, "I", "red")
    ]
]

symbols: list[Symbol] = Symbol.from_list(phasors_list)
d = Diagram(symbols, "Wykres fazorowy w połączeniu szeregowym cewek sprzężonych zgodnie")
d.create()
d.show()
byte = d.save_as_bytes()
print(byte)
