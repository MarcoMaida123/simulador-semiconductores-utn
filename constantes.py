from enum import Enum

PARAMETROS = {
    "Si":{
        "name": "Silicio",
        "gap_o": 1.17,
        "nc_t": 6.1968e15, # NC/(T^(3/2))
        "nv_t": 3.5218e15, # NV/(T^(3/2)) 
        "alpha": 4.73e-4,
        "betha": 636,
        "movility_n": 1350,
        "movility_p": 480
    },
    "Ge":{
        "name": "Germanio",
        "gap_o": 0.742,
        "nc_t": 1.9822e15, # NC/(T^(3/2))
        "nv_t": 1.0296e15, # NV/(T^(3/2)) 
        "alpha": 4.8e-4,
        "betha": 235,
        "movility_n": 3900,
        "movility_p": 1900
    },
    "AsGa":{
        "name": "Arseniuro de Galio",
        "gap_o": 1.519,
        "nc_t": 8.1021e13, # NC/(T^(3/2))
        "nv_t": 1.8321e15, # NV/(T^(3/2))   
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