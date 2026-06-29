import numpy as np
import matplotlib.pyplot as plt
from constantes import Dopaje
import plotly.graph_objects as go

def graficar_diagrama_bandas(semi):
  """
  Recibe ÚNICAMENTE una instancia de la clase Semiconductor y grafica 
  su diagrama de bandas extrayendo de ella toda la información necesaria.
  """
  # 1. Obtener niveles de energía calculados internamente
  Ecv, Efv, Eiv, Ev, x = semi.calcBandas()

  # 2. Inicializar la figura
  plt.figure(figsize=(9, 6))
  
  # Dibujar las líneas de las bandas
  plt.plot(x, Ecv, label=r"Banda de Conducción ($E_c$)", color="#d32f2f", lw=2)
  plt.plot(x, Eiv, label=r"Nivel Intrínseco ($E_i$)", color="#f57c00", linestyle="--", lw=1.5)
  plt.plot(x, Efv, label=r"Nivel de Ferm i ($E_f$)", color="#388e3c", linestyle="-.", lw=2)
  plt.plot(x, Ev, label=r"Banda de Valencia ($E_v$)", color="#1976d2", lw=2)

  # 4. Acotaciones y Flechas Dinámicas
  # Flecha para el Egap (siempre a la izquierda, x=0.15)
  plt.annotate("", xy=(x[2], Ecv[2]), xytext=(x[2], Ev[2]),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.2))
  plt.text(x[2]*1.1, Ecv[2] / 2, f'$E_g$ = {semi.Egap:.4f} eV', va='center', weight='bold', )

  # Flechas para distancias al nivel de Fermi (x=0.6)
  x_fermi_arrows = x[6]
  
  # --- Flecha Ef - Ev ---
  plt.annotate("", xy=(x[6], Efv[6]), xytext=(x[6], Ev[6]),
                arrowprops=dict(arrowstyle='<->', color='#303f9f', lw=1.2))
  # CORRECCIÓN: Promedio exacto de altura en el punto x[6]
  plt.text(x[6] + x[2]*.1, (Efv[6] + Ev[6]) / 2, f'$E_f - E_v$ = {Efv[0]:.4f} eV', va='center')

  # --- Flecha Ec - Ef ---
  plt.annotate("", xy=(x[6], Ecv[6]), xytext=(x[6], Efv[6]),
                arrowprops=dict(arrowstyle='<->', color='#7b1fa2', lw=1.2))
  # CORRECCIÓN: Promedio exacto de altura en el punto x[6]
  plt.text(x[6] + x[2]*.1, (Ecv[6] + Efv[6]) / 2, f'$E_c - E_f$ = {Ecv[0] - Efv[0]:.4f} eV', va='center')
  # 5. Estética general del gráfico
  # Si guardaste tipo_dopaje en el objeto lo usás acá, si no, por defecto "upper left"
  tipo = getattr(semi, 'tipo_dopaje', Dopaje.NO_DOPADO)
  loc_leyenda = "upper left" if tipo == Dopaje.TIPO_P else "lower left"
  #plt.legend(loc=loc_leyenda, frameon=True, shadow=True)
  plt.legend(
      loc="upper center", 
      bbox_to_anchor=(0.5, -0.15), # (X, Y) relativo a los ejes. -0.15 la tira hacia abajo
      ncol=2,                      # Organiza las referencias en 2 columnas para que no ocupe tanto espacio vertical
      frameon=True, 
      shadow=True
  ) 

  # Título dinámico leyendo los atributos del objeto
  titulo = f"Diagrama de Bandas - {semi.props['name']}\n"
  titulo += f"T = {semi.T} K | $n_0$ = {semi.no:.2e} $cm^{{-3}}$ | $p_0$ = {semi.po:.2e} $cm^{{-3}}$ | $Vapp$ = {semi.V:0.2f} $V$"
  plt.title(titulo, fontsize=12, pad=15)
  
  plt.ylabel("Energía [eV]", fontsize=11)
  plt.xlabel("Largo del semiconductor", fontsize=11)
  
  #plt.xticks([]) 
  plt.grid(True)
  plt.tight_layout()
  #plt.show()

def mostrarCajaHTML(titulo, valor, unidad):
  return f"""<div style='background-color: #1e2430; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                    <span style='font-size: 14px; color: #a3b8cc; display: block; margin-bottom: 4px;'>{titulo}</span>
                    <span style='font-size: 19px; font-weight: bold; color: #ffffff;'>{valor} {unidad}</span>
                </div>"""

# ==============================================================================
# FUNCION 2: NUEVA FUNCIÓN EXCLUSIVA PARA LA APP WEB (PLOTLY INTERACTIVO)
# ==============================================================================
def graficarApp(semi):
    """
    Genera el diagrama de bandas interactivo en Plotly optimizado para Streamlit.
    Versión de ALTA VISIBILIDAD (Fondo claro para proyección) y diseño limpio sin flechas redundantes.
    """
    # 1. Obtener los vectores de niveles de energía
    Ecv, Efv, Eiv, Ev, x = semi.calcBandas()

    fig = go.Figure()

    # 2. Trazamos las curvas con colores de fuerte contraste aptos para fondo blanco
    fig.add_trace(go.Scatter(x=x, y=Ecv, name="Banda de Conducción (E<sub>c</sub>)", line=dict(color='#b91c1c', width=3), hovertemplate='%{y:.4f} eV'))
    fig.add_trace(go.Scatter(x=x, y=Eiv, name="Nivel Intrínseco (E<sub>i</sub>)", line=dict(color='#d97706', width=1.5, dash='dash'), hovertemplate='%{y:.4f} eV'))
    fig.add_trace(go.Scatter(x=x, y=Efv, name="Nivel de Fermi (E<sub>f</sub>)", line=dict(color='#15803d', width=2.5, dash='dashdot'), hovertemplate='%{y:.4f} eV'))
    fig.add_trace(go.Scatter(x=x, y=Ev, name="Banda de Valencia (E<sub>v</sub>)", line=dict(color='#1d4ed8', width=3), hovertemplate='%{y:.4f} eV'))

    # 3. Dejamos SOLO la cota del Egap bien limpia en el centro del semiconductor
    x_medio = x[len(x)//2]
    idx_medio = len(x)//2

    # 4. Ajustes estéticos para PROYECCIÓN EN PIZARRÓN (Fondo blanco de alto contraste)
   # 5. Configuración de la estética general del Layout (ALTA VISIBILIDAD)
    fig.update_layout(
        template="plotly_white",       # Fondo blanco nativo
        paper_bgcolor="#ffffff",       # Fondo exterior blanco puro
        plot_bgcolor="#ffffff",        # Fondo interior blanco puro
        font=dict(color="black", size=12), # Forzamos color base negro para todo el gráfico
        margin=dict(l=20, r=20, t=20, b=20),
        height=450,
        xaxis=dict(
            title=dict(text="Largo del semiconductor [cm]", font=dict(color="black", size=13, weight="bold")),
            tickfont=dict(color="black", size=11), # CORRECCIÓN: Números de la escala en negro
            showgrid=True, 
            gridcolor="#e2e8f0",       
            linecolor="black",         # Línea del eje en negro sólido
            linewidth=1.5
        ),
        yaxis=dict(
            title=dict(text="Energía [eV]", font=dict(color="black", size=13, weight="bold")),
            tickfont=dict(color="black", size=11), # CORRECCIÓN: Números de la escala en negro
            showgrid=True, 
            gridcolor="#e2e8f0", 
            linecolor="black",         # Línea del eje en negro sólido
            linewidth=1.5,
            showticklabels=False,
            zeroline=False
        ),
        legend=dict(
            orientation="h", 
            yanchor="bottom", y=-0.3, 
            xanchor="center", x=0.5,
            font=dict(color="black", size=11) # Texto de la leyenda en negro sólido
        ),
        hovermode="x unified"          
    )

    # Guardamos la figura en la variable global para app.py
    global figura_actual
    figura_actual = fig