from enum import Enum

PARAMETROS = {
    "Si":{
        "name": "Silicio",
        "gap_o": 1.17,
        "nc": 3.22e19, 
        "nv": 1.82e19, 
        "alpha": 4.73e-4,
        "betha": 636,
        "movility_n": 1350,
        "movility_p": 480
    },
    "Ge":{
        "name": "Germanio",
        "gap_o": 0.742,
        "nc": 1.03e19,
        "nv": 5.35e18,
        "alpha": 4.8e-4,
        "betha": 235,
        "movility_n": 3900,
        "movility_p": 1900
    },
    "AsGa":{
        "name": "Arseniuro de Galio",
        "gap_o": 1.519,
        "nc": 4.21e17,
        "nv": 9.52e18,   
        "alpha": 5.405e-4,
        "betha": 204,
        "movility_n": 8800,
        "movility_p": 400
    }
}

class Materiales(Enum):
    SI = "Si"
    ASGA = "AsGa"
    GE = "Ge"

K_B = 8.6333e-5 # [eV/K]
V_TH = 0.0259 #[eV]
Q_E = 1.602176621e-19 #[C]

class Dopaje(Enum):
    TIPO_N = 1
    TIPO_P = 2
    NO_DOPADO = 3