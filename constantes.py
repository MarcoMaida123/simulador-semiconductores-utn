from enum import Enum

PARAMETROS = {
    "Si":{
        "name": "Silicio",
        "gap": 1.12,
        "nc": 3.22e19, 
        "nv": 1.82e19, 
        "alpha": 4.73e-4,
        "beta": 636,
        "mu_n": 1350,
        "mu_n-exp": 2.42,
        "mu_p": 480,
        "mu_p-exp": 2.2
    },
    "Ge":{
        "name": "Germanio",
        "gap": 0.66,
        "nc": 1.03e19,
        "nv": 5.35e18,
        "alpha": 4.8e-4,
        "beta": 235,
        "mu_n": 3900,
        "mu_n-exp": 1.66,
        "mu_p": 1900,
        "mu_p-exp": 2.33
    },
    "AsGa":{
        "name": "Arseniuro de Galio",
        "gap": 1.42,
        "nc": 4.21e17,
        "nv": 9.52e18,   
        "alpha": 5.405e-4,
        "beta": 204,
        "mu_n": 8800,
        "mu_n-exp": 1,
        "mu_p": 400,
        "mu_p-exp": 2.1
    }
}

class Materiales(Enum):
    SI = "Si"
    ASGA = "AsGa"
    GE = "Ge"

K_B = 8.6333e-5 # [eV/K]
V_TH = 0.0259 #[eV]
Q_E = 1.602176621e-19 #[C]

class Transitorios(Enum):
    SIN_LUZ = 0
    ENCENDIDO_LUZ = 1
    APAGADO_LUZ = 2

class Dopaje(Enum):
    TIPO_N = 1
    TIPO_P = 2
    NO_DOPADO = 3