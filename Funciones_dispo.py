import numpy as np
from constantes import *

class Sigmas(Enum):
    ELECTRONES = 1
    HUECOS = 2
    TOTAL = 3


class Semiconductor():
    Egap: float
    props: dict
    Nc: float
    Nv: float
    ni: float
    po: float
    no: float
    T: float
    V: float
    E: float
    L: float
    A: float
    S_n: float
    S_h: float

    def __init__(self, material, T=300, Na=0, Nd=0, V=0, L=1, A=1):
        # Cargo parametros de acuerdo al material
        self.props = PARAMETROS[material.value]
        self.T = T
        self.L = L
        self.V = V
        self.A = A

        # Calculo Egap en funcion de T
        self.calcEgap()
        # Calculo Nc y Nv
        self.calcNcNv()
        # Calculo ni
        self.calcNi()
        # Calculo no y pc
        self.no, self.po = self.calcNoPo(Na, Nd)
        # Calculo S_n y S_h
        self.S_n = self.calcSigma(Sigmas.ELECTRONES)
        self.S_h = self.calcSigma(Sigmas.HUECOS)
        # Calculo la pendiente de las bandas de energia (campo eléctrico)
        self.E = V / L

        pass
    
    def calcEgap(self):
        # Término de corrección exacto basado en la referencia de 300K
        factor_300 = (300**2) / (300 + self.props["beta"])
        factor_t = (self.T**2) / (self.T + self.props["beta"])
        
        return self.props["gap"] + self.props["alpha"] * (factor_300 - factor_t)

    def calcNcNv(self):
        self.Nc = self.props["nc"]*(self.T/300)**(3/2)
        self.Nv = self.props["nv"]*(self.T/300)**(3/2)

    def calcNi(self):
        self.ni = np.sqrt(self.Nc * self.Nv) * np.exp(- self.Egap / (2*K_B*self.T))

    def calcNoPo(self, Na, Nd):
        # Determinamos el exceso de dopaje neto
        dopaje_neto = Nd - Na

        if dopaje_neto > 0: # Predomina Tipo N
            # Mayoritario por resolvente (numéricamente estable porque sumamos)
            no = (dopaje_neto + np.sqrt(dopaje_neto**2 + 4 * self.ni**2)) / 2
            po = self.ni**2 / no
        elif dopaje_neto < 0: # Predomina Tipo P
            # Mayoritario por resolvente
            po = (-dopaje_neto + np.sqrt(dopaje_neto**2 + 4 * self.ni**2)) / 2
            no = self.ni**2 / po
        else: # Intrínseco
            no = self.ni
            po = self.ni

        return [no, po]

    def calcBandas(self):
        n = np.arange(0, self.L, self.L*0.1)

        # Obtengo expresiones de
        Ecv = self.Egap - self.E * n
        Efv = K_B*self.T*np.log(self.Nv/self.po) - self.E * n
        Eiv = self.Egap/2 - (K_B*self.T/2)*np.log(self.Nc/self.Nv) - self.E * n
        Ev = 0 - self.E * n

        return [Ecv, Efv, Eiv, Ev, n]

    def calcSigma(self, tipo:Sigmas):

        if tipo == Sigmas.ELECTRONES:
            return Q_E*self.no*self.props["movility_n"]
        elif tipo == Sigmas.HUECOS:
            return Q_E*self.po*self.props["movility_p"]
        else:
            return Q_E*(self.no*self.props["movility_n"] + self.po*self.props["movility_p"])
   
    def calcCorrientes(self):
        It = self.V * self.A * self.calcSigma(Sigmas.TOTAL) / self.L
        In = self.calcSigma(Sigmas.ELECTRONES)*self.V*self.A/self.L
        Ip = self.calcSigma(Sigmas.HUECOS)*self.V*self.A/self.L

        return [It, In, Ip]