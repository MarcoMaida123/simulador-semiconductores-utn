import Funciones_dispo as dispo
from constantes import *
import numpy as np
import matplotlib.pyplot as plt

# 1. Instanciamos el Panel de Control (Laboratorio)
labo = dispo.Laboratorio()

# 2. Configuración de parámetros externos (T = 300K, barra libre de campo)
labo.T = 300                 
labo.V = 0.0                 # Sin campo eléctrico (E = 0)
labo.GL = 0.0                # La luz NO penetra en el cuerpo (gL = 0)
labo.dpn0 = 1e10             # Exceso inyectado de huecos en x=0
labo.transitorio = Transitorios.ENCENDIDO_LUZ # Usamos encendido para que evolucione

# 3. Parámetros del cristal de Silicio tipo N (Datos del enunciado)
A = 1.0                      
L = 0.03                     # Longitud de la barra [cm] (Suficiente para ver caer Lp)
material = Materiales.SI     
Na = 0.0                     
Nd = 1e15                    # Dopaje donor
tau_p = 1e-6                 

# Forzamos en el diccionario la movilidad exacta del enunciado para calibrar
PARAMETROS["Si"]["mu_p"] = 438.0

# 4. Cargamos el dispositivo en el laboratorio
labo.cargarSemi(material=material, Nd=Nd, Na=Na, tau_p=tau_p, L=L, A=A)

# 5. Corremos la simulación espacio-temporal (200 puntos espaciales)
labo.simular(puntos_x=200)

# =============================================================================
# EXTRACCIÓN DE DATOS EN RÉGIMEN PERMANENTE (ÚLTIMA COLUMNA DE TIEMPO)
# =============================================================================
x = labo.x
n_final = labo.semi.no[:, -1]
p_final = labo.semi.po[:, -1]

# Extraemos las bandas de energía estacionarias finales
Ecv_final = labo.semi.Ecv[:, -1]
Eiv_final = labo.semi.Eiv[:, -1]
Efn_final = labo.semi.Efn_i[:, -1] # Cuasi-Fermi de electrones
Efp_final = labo.semi.Efp_i[:, -1] # Cuasi-Fermi de huecos
Ev_final  = labo.semi.Ev[:, -1]

# =============================================================================
# GRÁFICO 1: PERFIL ESPACIAL DE CONCENTRACIONES TOTALES (n, p vs x)
# =============================================================================
plt.figure(1, figsize=(8, 5.5))

plt.plot(x, n_final, label=f"Electrones ($n$)", color="#b91c1c", lw=2.5)
plt.plot(x, p_final, label=f"Huecos ($p$)", color="#1d4ed8", lw=2.5)

# Línea indicando el piso de equilibrio p0 para ver cómo se desinfla el exceso
plt.axhline(y=labo.semi.po_eq, color="gray", linestyle=":", label=f"$p_0$ equilibrio ({labo.semi.po_eq:.1e})", alpha=0.7)


plt.title("Perfil Espacial de Concentración de Portadores (Inyección Superficial)\nRégimen Permanente Estacionario a T = 300K", fontsize=11, pad=12)
plt.ylabel("Densidad de Portadores [$cm^{-3}$] (Escala Log)", fontsize=10)
plt.xlabel("Posición a lo largo de la barra $x$ [cm]", fontsize=10)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(loc="center right", frameon=True, shadow=True, fontsize=9)
plt.tight_layout()

# =============================================================================
# GRÁFICO 2: DIAGRAMA DE BANDAS ESPACIAL (DEFORMACIÓN POR INYECCIÓN SUPERFICIAL)
# =============================================================================
plt.figure(2, figsize=(8, 5.5))

plt.plot(x, Ecv_final, label=r"Banda de Conducción ($E_c$)", color="#d32f2f", lw=2.5)
plt.plot(x, Eiv_final, label=r"Nivel Intrínseco ($E_i$)", color="#f57c00", linestyle="--", lw=1.5)
plt.plot(x, Ev_final, label=r"Banda de Valencia ($E_v$)", color="#1976d2", lw=2.5)

# Graficamos los cuasi-niveles de Fermi que cambian en el espacio
plt.plot(x, Efn_final, label=r"Cuasi-Fermi de Electrones ($E_{fn}$)", color="darkgreen", linestyle="-.", lw=2.5)
plt.plot(x, Efp_final, label=r"Cuasi-Fermi de Huecos ($E_{fp}$)", color="purple", linestyle="-.", lw=2.5)

plt.title("Diagrama de Bandas Espacial en Fuera de Equilibrio\nEfecto de la Difusión de Portadores desde la Frontera Izquierda", fontsize=11, pad=12)
plt.ylabel("Energía [eV]", fontsize=10)
plt.xlabel("Posición a lo largo de la barra $x$ [cm]", fontsize=10)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(loc="center right", frameon=True, shadow=True, fontsize=9)
plt.tight_layout()

plt.show()