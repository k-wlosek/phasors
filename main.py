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
        (66.48, 0, "U_R1", "green"),
        (169.67, 90, "U_L1", "blue"),
        (-88.2, 90, "U_M", "black"),
        (58.94, 0, "U_R2", "green"),
        (162.51, 90, "U_L2", "blue"),
        (-88.2, 90, "U_M", "black"),
        (200, 51.16, "U", "pink")
    ],
    [
        (0.53, 0, "I", "red")
    ]
]
# phasors_list2 = [
#     [
#         (25.38, 0, "U_R1", "green"),
#         (64.78, 90, "U_L1", "blue"),
#         (33.68, 90, "U_M", "black"),
#         (22.51, 0, "U_R2", "green"),
#         (62.05, 90, "U_L2", "blue"),
#         (33.68, 90, "U_M", "black"),
#         (200, 76.15, "U", "pink")
#     ],
#     [
#         (0.2, 0, "I", "red")
#     ]
# ]

symbols: list[Symbol] = Symbol.from_list(phasors_list)
d = Diagram(symbols, "Wykres fazorowy dla pomiaru 1 w sprzężeniu przeciwnym")
d.create()
d.show()
# d.save("zad2_1_wrong.png")
byte = d.save_as_bytes("svg")
print(byte)
