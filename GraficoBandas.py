import Funciones_dispo as dispo
from constantes import Materiales
import graficar as vis

# Objeto Semiconductor
semi = dispo.Semiconductor(Materiales.SI, T=300, Na=0, Nd=0, V=-1, L=0.02)

# Grafico de mi semiconductor
vis.graficar_diagrama_bandas(semi)