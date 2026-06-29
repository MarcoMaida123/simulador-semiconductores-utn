import numpy as np
from constantes import *

# Clase Semiconductor
class Semiconductor():
    
    # Parametros del semiconductor
    props: dict
    L: float
    A: float
    tau_p: float
    Nd: float
    Na: float

    # Resolucion de simulacion
    x: np.ndarray
    t: np.ndarray
    dx: float
    dt: float 

    # Parametros Térmicos Simulados
    Egap: float
    Nc: float
    Nv: float
    ni: float
    po_eq: float
    no_eq: float
    mu_n: float
    mu_p: float
    Dn: float
    Dp: float
    
    # Parametros Energéticos Simulados
    no: np.ndarray
    po: np.ndarray
    Ecv: np.ndarray
    Efn_i: np.ndarray
    Efp_i: np.ndarray
    Eiv: np.ndarray
    Ev: np.ndarray

    S_n: float
    S_p: float

    def __init__(self, material, tau_p=1e-6, Na=0, Nd=0, L=1, A=1):
        # ------------------- PARAMETROS PROPIOS DEL SEMICONDUCTOR -------------------
        self.props = PARAMETROS[material.value]
        self.L = L
        self.A = A
        self.tau_p = tau_p
        self.Na = Na
        self.Nd = Nd
        pass
    
    def actualizarValores(self, T, V, Gl, dpn0, transitorio, puntos_x):
        self.T = T
        # ------------------- CALCULOS TERMICOS ------------------- 
        # GAP
        self.calcEgap(T=T)     
        # Nc y Nv
        self.calcNcNv(T=T)
        # ni  
        self.calcNi(T=T)
        # no_eq y po_eq
        self.calcNoPoEQ() 
        # Movilidades
        self.calcMovilidades(T=T)
        # Dp y Dn
        self.calcDpDn(T=T)

        # ------------------- RESOLUCION ESPACIAL Y TEMPORAL ------------------- 
        self.x, self.dx, self.t, self.dt = self.calcResolucionXT(N=puntos_x, E=V/self.L)

        # ------------------- CALCULOS ENERGÉTICOS ------------------- 
        # no y po
        self.calcConcentraciones(gl=Gl, dpn0=dpn0, transitorio=transitorio, E=V/self.L)
        # Bandas de Energia
        self.calcBandas(T=T, E=V/self.L)
        # Sigmas
        self.calcSigma()
        # Corrientes
        self.calcCorrientes(V=V)

        return self.x, self.dx, self.t, self.dt

    def calcEgap(self, T):
        # Término de corrección exacto basado en la referencia de 300K
        factor_300 = (300**2) / (300 + self.props["beta"])
        factor_t = (T**2) / (T + self.props["beta"])
        
        self.Egap = self.props["gap"] + self.props["alpha"] * (factor_300 - factor_t)

    def calcNcNv(self, T):
        self.Nc = self.props["nc"]*(T/300)**(3/2)
        self.Nv = self.props["nv"]*(T/300)**(3/2)

    def calcNi(self, T):
        self.ni = np.sqrt(self.Nc * self.Nv) * np.exp(- self.Egap / (2*K_B*T))

    def calcNoPoEQ(self):
        # Determinamos el exceso de dopaje neto
        dopaje_neto = self.Nd - self.Na

        if dopaje_neto > 0: # Predomina Tipo N
            # Mayoritario por resolvente (numéricamente estable porque sumamos)
            self.no_eq = (dopaje_neto + np.sqrt(dopaje_neto**2 + 4 * self.ni**2)) / 2
            self.po_eq = self.ni**2 / self.no_eq
        elif dopaje_neto < 0: # Predomina Tipo P
            # Mayoritario por resolvente
            self.po_eq = (-dopaje_neto + np.sqrt(dopaje_neto**2 + 4 * self.ni**2)) / 2
            self.no_eq = self.ni**2 / self.po_eq
        else: # Intrínseco
            self.no_eq = self.ni
            self.po_eq = self.ni

    def calcBandas(self, T, E):

        # 1. Expandimos el campo eléctrico a una matriz de (Nx, Nt)
        E_xt = np.full((len(self.x), len(self.t)), E)
        
        # 2. Convertimos self.x en columna (Nx, 1) y la repetimos horizontalmente Nt veces
        # np.tile toma el vector columna y lo replica (1 vez vertical, len(self.t) veces horizontal)
        X_grid = np.tile(self.x[:, None], (1, len(self.t)))

        self.Ecv = self.Egap - E_xt * X_grid
        self.Eiv = self.Egap/2 - (K_B*T/2)*np.log(self.Nc/self.Nv) - E_xt * X_grid
        self.Efn_i = K_B*T*np.log(self.no/self.ni) + self.Eiv
        self.Efp_i = - K_B*T*np.log(self.po/self.ni) + self.Eiv
        self.Ev = - E_xt * X_grid

    def calcSigma(self):

        self.S_n = Q_E * self.no * self.mu_n
        self.S_p = Q_E * self.po * self.mu_p
   
    def calcCorrientes(self, V):
        self.In = self.S_n * V * self.A / self.L
        self.Ip = self.S_p * V * self.A / self.L
        self.It = self.In + self.Ip

    def calcMovilidades(self, T):
        self.mu_n = self.props["mu_n"]*(T/300)**(-self.props["mu_n-exp"])
        self.mu_p = self.props["mu_p"]*(T/300)**(-self.props["mu_p-exp"])
    
    def calcDpDn(self, T):
        self.Dp = K_B*T*self.mu_p
        self.Dn = K_B*T*self.mu_n

    def calcResolucionXT(self, N, E):
        dx = self.L / N
        dt = 0.5 * 1/((2*self.Dp)/((dx)**2))

        # En lugar de max puro sobre la difusión de toda la barra, nos acotamos
        # Si la barra es larga, lo que limita la física es la recombinación (5 * tau_p)
        tmax = 5 * self.tau_p
        
        # Solo si hay campo eléctrico, el tiempo de tránsito puede ser más rápido
        if E != 0:
            t_drift = self.L / (self.mu_p * abs(E))
            # Si el viaje por drift es más rápido que la recombinación, simulamos ese viaje
            if t_drift < tmax:
                tmax = t_drift * 1.5  # Le damos un changüí de 50% más de tiempo
    
        # Vectores de tiempo y espacio
        x = np.arange(0, self.L + dx, dx) 
        t = np.arange(0, tmax + dt, dt)

        return x, dx, t, dt

    def calcConcentraciones(self, transitorio, dpn0, gl, E):
        # Vector de concentraciones (armo grilla de espacio-tiempo)
        dp = np.zeros((len(self.x), len(self.t)))


        # =====================================================================
        # Establecer condiciones de contorno automáticas según la física
        # =====================================================================
        # 1. Condición Inicial Pura (t=0)
        if transitorio == Transitorios.ENCENDIDO_LUZ:
            dp[:, 0] = 0        # Toda la barra arranca a oscuras
        elif transitorio == Transitorios.APAGADO_LUZ:
            Lp = np.sqrt(self.Dp * self.tau_p)
            dp[:, 0] = dpn0 * np.exp(-self.x / Lp)
    

        # 2. Bucle temporal (avanza en el tiempo)
        for n in range(1, len(self.t)):
            
            # --- CONDICIONES DE CONTORNO EN EL TIEMPO n ---
            if transitorio == Transitorios.ENCENDIDO_LUZ:
                if gl > 0 :
                    # ESCENARIO 1.13 (Luz uniforme): Fronteras Libres (Neumann)
                    # La punta izquierda vale lo mismo que el primer punto interno
                    dp[0, n-1] = dp[1, n-1]
                    # La punta derecha vale lo mismo que el último punto interno
                    dp[-1, n-1] = dp[-2, n-1]
                else:
                    # ESCENARIO 1.14: Fronteras Fijas (Dirichlet)
                    dp[0, n-1] = dpn0
                    dp[-1, n-1] = 0
            elif transitorio == Transitorios.APAGADO_LUZ:
                # Transitorio de apagado (sin luz en ningún lado): Ambos extremos mueren
                dp[0, n-1] = 0
                dp[-1, n-1] = 0 

            # 3. Bucle espacial (calcula el interior de la barra)
            dp[1:-1, n] = dp[1:-1, n-1] + self.dt * (
                self.Dp * (dp[2:, n-1] - 2*dp[1:-1, n-1] + dp[:-2, n-1]) / self.dx**2 
                - self.mu_p * E * (dp[2:, n-1] - dp[:-2, n-1]) / (2*self.dx) 
                + gl 
                - dp[1:-1, n-1] / self.tau_p
            )

        # Calculo de concentraciones de acuerdo a dp(x, t)
        self.no = self.no_eq + dp
        self.po = self.po_eq + dp

class Laboratorio():
    # Seteo mis variables de trabajo
    T: float
    V: float
    GL: float
    dpn0 : float
    transitorio: Transitorios
    semi : Semiconductor

    # Resolucion temporal y espacial
    dx: float
    dt: float
    t: np.ndarray
    x: np.ndarray

    def __init__(self):
        pass

    # Funcion de simulacion
    def simular(self, puntos_x):
        # Mis parametros de simulación
        self.x, self.dx, self.t, self.dt = self.semi.actualizarValores(
            T=self.T,
            V=self.V,
            Gl=self.GL,
            dpn0=self.dpn0, 
            transitorio=self.transitorio,
            puntos_x=puntos_x
        )
    
    # Cambio en mi semiconductor
    def cargarSemi(self, tau_p, material, Nd, Na, L, A):
        self.semi = Semiconductor(material=material, tau_p=tau_p, Nd=Nd, Na=Na, L=L, A=A)
