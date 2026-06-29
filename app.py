import streamlit as st
import numpy as np
import Funciones_dispo as dispo
from constantes import Materiales, PARAMETROS, Transitorios
import plotly.graph_objects as go

st.set_page_config(page_title="Laboratorio Virtual de Semiconductores", layout="wide")
 
# Inicializamos parámetros en session_state si no existen
if "mis_parametros" not in st.session_state:
    st.session_state.mis_parametros = PARAMETROS.copy()

# Sincronizamos las constantes globales con las del estado de sesión
dispo.PARAMETROS = st.session_state.mis_parametros

tab_simulador, tab_config, tab_autor = st.tabs(["Simulador Principal", "Tabla de Constantes", "Autor"])

# =============================================================================
# FUNCIONES DE RENDERIZADO POR SECCIÓN (MÓDULOS DE LA INTERFAZ)
# =============================================================================
def renderizar_pestaña_configuracion():

    st.header("Tabla de Constantes del Material")
    st.write("Modificá los valores de los campos según los datos de tu cátedra y hacé clic en **Guardar Cambios**.")

    with st.form("form_constantes"):
        st.subheader("Parámetros Típicos / Comunes (a 300K)")
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1])
        with c_prop: st.markdown("**Propiedad / Variable**")
        with c_si: st.markdown("**Silicio (Si)**")
        with c_ge: st.markdown("**Germanio (Ge)**")
        with c_asga: st.markdown("**Arseniuro de Galio (GaAs)**")
        st.markdown("---") 

        # Gap
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Bandgap a 300K ($E_g$) [eV]")
        with c_si: gap_si = st.number_input("gap_si", value=float(st.session_state.mis_parametros["Si"]["gap"]), format="%.3f", label_visibility="collapsed")
        with c_ge: gap_ge = st.number_input("gap_ge", value=float(st.session_state.mis_parametros["Ge"]["gap"]), format="%.3f", label_visibility="collapsed")
        with c_asga: gap_asga = st.number_input("gap_asga", value=float(st.session_state.mis_parametros["AsGa"]["gap"]), format="%.3f", label_visibility="collapsed")

        # Nc
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Efectiva en Conducción ($N_c$) [cm⁻³]")
        with c_si: nc_si = st.number_input("nc_si", value=float(st.session_state.mis_parametros["Si"]["nc"]), format="%.4e", label_visibility="collapsed")
        with c_ge: nc_ge = st.number_input("nc_ge", value=float(st.session_state.mis_parametros["Ge"]["nc"]), format="%.4e", label_visibility="collapsed")
        with c_asga: nc_asga = st.number_input("nc_asga", value=float(st.session_state.mis_parametros["AsGa"]["nc"]), format="%.4e", label_visibility="collapsed")
        
        # Nv
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Efectiva en Valencia ($N_v$) [cm⁻³]")
        with c_si: nv_si = st.number_input("nv_si", value=float(st.session_state.mis_parametros["Si"]["nv"]), format="%.4e", label_visibility="collapsed")
        with c_ge: nv_ge = st.number_input("nv_ge", value=float(st.session_state.mis_parametros["Ge"]["nv"]), format="%.4e", label_visibility="collapsed")
        with c_asga: nv_asga = st.number_input("nv_asga", value=float(st.session_state.mis_parametros["AsGa"]["nv"]), format="%.4e", label_visibility="collapsed")

        # mu_n
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Movilidad de electrones ($\mu_n$) [cm²/V·s]")
        with c_si: mn_si = st.number_input("mn_si", value=float(st.session_state.mis_parametros["Si"]["mu_n"]), format="%.1f", label_visibility="collapsed")
        with c_ge: mn_ge = st.number_input("mn_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_n"]), format="%.1f", label_visibility="collapsed")
        with c_asga: mn_asga = st.number_input("mn_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_n"]), format="%.1f", label_visibility="collapsed")

        # mu_p
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Movilidad de huecos ($\mu_p$) [cm²/V·s]")
        with c_si: mp_si = st.number_input("mp_si", value=float(st.session_state.mis_parametros["Si"]["mu_p"]), format="%.1f", label_visibility="collapsed")
        with c_ge: mp_ge = st.number_input("mp_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_p"]), format="%.1f", label_visibility="collapsed")
        with c_asga: mp_asga = st.number_input("mp_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_p"]), format="%.1f", label_visibility="collapsed")

        st.subheader("Coeficientes de Dependencia Térmica (Varshni / Exponentes)")
        # Alphas
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Alpha ($\alpha$) [eV/K]")
        with c_si: alpha_si = st.number_input("alpha_si", value=float(st.session_state.mis_parametros["Si"]["alpha"]), format="%.3e", label_visibility="collapsed")
        with c_ge: alpha_ge = st.number_input("alpha_ge", value=float(st.session_state.mis_parametros["Ge"]["alpha"]), format="%.3e", label_visibility="collapsed")
        with c_asga: alpha_asga = st.number_input("alpha_asga", value=float(st.session_state.mis_parametros["AsGa"]["alpha"]), format="%.3e", label_visibility="collapsed")

        # Betas
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Beta ($\beta$) [K]")
        with c_si: beta_si = st.number_input("beta_si", value=float(st.session_state.mis_parametros["Si"]["beta"]), format="%.1f", label_visibility="collapsed")
        with c_ge: beta_ge = st.number_input("beta_ge", value=float(st.session_state.mis_parametros["Ge"]["beta"]), format="%.1f", label_visibility="collapsed")
        with c_asga: beta_asga = st.number_input("beta_asga", value=float(st.session_state.mis_parametros["AsGa"]["beta"]), format="%.1f", label_visibility="collapsed")

        # Exponentes mu_n y mu_p
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Exponente Temp. de $\mu_n$")
        with c_si: exp_n_si = st.number_input("exp_n_si", value=float(st.session_state.mis_parametros["Si"]["mu_n-exp"]), format="%.2f", label_visibility="collapsed")
        with c_ge: exp_n_ge = st.number_input("exp_n_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_n-exp"]), format="%.2f", label_visibility="collapsed")
        with c_asga: exp_n_asga = st.number_input("exp_n_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_n-exp"]), format="%.2f", label_visibility="collapsed")

        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Exponente Temp. de $\mu_p$")
        with c_si: exp_p_si = st.number_input("exp_p_si", value=float(st.session_state.mis_parametros["Si"]["mu_p-exp"]), format="%.2f", label_visibility="collapsed")
        with c_ge: exp_p_ge = st.number_input("exp_p_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_p-exp"]), format="%.2f", label_visibility="collapsed")
        with c_asga: exp_p_asga = st.number_input("exp_p_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_p-exp"]), format="%.2f", label_visibility="collapsed")

        boton_guardar = st.form_submit_button("💾 Guardar Cambios")
        if boton_guardar:
            st.session_state.mis_parametros = {
                "Si": {"name": "Silicio", "gap": gap_si, "nc": nc_si, "nv": nv_si, "alpha": alpha_si, "beta": beta_si, "mu_n": mn_si, "mu_n-exp": exp_n_si, "mu_p": mp_si, "mu_p-exp": exp_p_si},
                "Ge": {"name": "Germanio", "gap": gap_ge, "nc": nc_ge, "nv": nv_ge, "alpha": alpha_ge, "beta": beta_ge, "mu_n": mn_ge, "mu_n-exp": exp_n_ge, "mu_p": mp_ge, "mu_p-exp": exp_p_ge},
                "AsGa": {"name": "Arseniuro de Galio", "gap": gap_asga, "nc": nc_asga, "nv": nv_asga, "alpha": alpha_asga, "beta": beta_asga, "mu_n": mn_asga, "mu_n-exp": exp_n_asga, "mu_p": mp_asga, "mu_p-exp": exp_p_asga}
            }
            st.rerun()

def renderizar_sidebar_controles():
    """Dibuja de forma agrupada los controles de entrada y devuelve las variables seleccionadas."""
    st.header("Panel de Control")
    
    # --- GRUPO 1: PARÁMETROS INDEPENDIENTES DEL DISPOSITIVO ---
    with st.expander("Parámetros del Dispositivo", expanded=True):
        material = st.selectbox(
            "Material Base:", options=[Materiales.SI, Materiales.GE, Materiales.ASGA],
            format_func=lambda x: "Silicio (Si)" if x == Materiales.SI else ("Germanio (Ge)" if x == Materiales.GE else "Arseniuro de Galio (GaAs)")
        )
        L = st.number_input("Longitud L [cm]:", min_value=1e-5, value=0.05, format="%.4f")
        A = st.number_input("Área Sección A [cm²]:", min_value=1e-7, value=0.05, format="%.4e")
        tau_p = st.number_input("Vida media τ_p [seg]:", min_value=1e-10, value=1e-6, format="%.2e")

    # --- GRUPO 2: PARÁMETROS TÉRMICOS Y DOPAJE ---
    with st.expander("Temperatura y Dopajes", expanded=True):
        T = st.slider("Temperatura T [K]:", min_value=100, max_value=600, value=300, step=5)
        Na = st.number_input("Aceptores Na [cm⁻³]:", min_value=0.0, value=0.0, format="%.2e")
        Nd = st.number_input("Donores Nd [cm⁻³]:", min_value=0.0, value=0.0, format="%.2e")

    # --- GRUPO 3: AGENTES EXTERNOS Y TRANSITORIOS ---
    with st.expander("Excitaciones y Luz", expanded=True):
        Vapp = st.slider("Tensión Aplicada Vapp [V]:", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)
        transitorio = st.selectbox(
            "Tipo de Régimen / Transitorio:",
            options=[Transitorios.SIN_LUZ, Transitorios.ENCENDIDO_LUZ, Transitorios.APAGADO_LUZ],
            format_func=lambda x: "Oscuridad total / Equilibrio" if x == Transitorios.SIN_LUZ else ("Encendido de Luz" if x == Transitorios.ENCENDIDO_LUZ else "Apagado de Luz")
        )
        gl = st.number_input("Generación en volumen g_L [cm⁻³s⁻¹]:", min_value=0.0, value=0.0, format="%.2e")
        dpn0 = st.number_input("Inyección en frontera δp_n0 [cm⁻³]:", min_value=0.0, value=0.0, format="%.2e")
        puntos_x = st.slider("Puntos de la grilla espacial (N):", min_value=50, max_value=300, value=200, step=10)

    return material, L, A, tau_p, T, Na, Nd, Vapp, transitorio, gl, dpn0, puntos_x

def mostrar_tab_portadores(labo):

    st.subheader("Distribución Espacial de Portadores")
    Nt = len(labo.t)

    # Slider de tiempo
    opciones_tiempo = [(i, f"t = {labo.t[i]*1e6:.3f} µs") for i in range(Nt)]
    val_slider = st.select_slider(
            "Evolución temporal (Portadores):",
            options=[opt[0] for opt in opciones_tiempo],
            format_func=lambda x: opciones_tiempo[x][1],
            value=0,
            key=f"p_time_{Nt}"
    )
    idx_t = val_slider if val_slider < Nt else (Nt - 1)

    # Estructurar vista de grafico y métricas
    grafico, metricas = st.columns([3, 1])

    with metricas:
        # Fila de métricas tecnológicas clave
        st.metric("$n_o$ (Equilibrio)", f"{labo.semi.no_eq:.2e} cm⁻³")
        st.metric("$p_o$ (Equilibrio)", f"{labo.semi.po_eq:.2e} cm⁻³")
        st.metric("$n_i$ (Intrínseco)", f"{labo.semi.ni:.2e} cm⁻³")

    with grafico:
        # Gráfico interactivo logarítmico (n, p vs x)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.no[:, idx_t], name="Electrones (n)", line=dict(color='#b91c1c', width=3.5)))
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.po[:, idx_t], name="Huecos (p)", line=dict(color='#1d4ed8', width=3.5)))
        fig.update_layout(
            template="plotly_white", xaxis_title="Posición x [cm]", yaxis_title="Concentración [cm⁻³]",
            yaxis_type="log", margin=dict(l=10, r=10, t=10, b=10), height=400, hovermode="x unified"
        )
        fig.update_yaxes(
            exponentformat="power",  # Options: "none", "e", "E", "power", "SI", "B"
            showexponent="all"       # Options: "all", "first", "last", "none"
        )
        st.plotly_chart(fig, use_container_width=True)

def mostrar_tab_bandas(labo):
    """Renderiza el diagrama espacial de bandas de energía y cuasi-niveles de Fermi."""
    st.subheader("Evolución Espacial del Diagrama de Bandas")
    Nt = len(labo.t)

    if Nt > 1:
        opciones_tiempo = [(i, f"t = {labo.t[i]*1e6:.3f} µs") for i in range(Nt)]
        val_slider = st.select_slider(
            "Evolución temporal (Bandas):",
            options=[opt[0] for opt in opciones_tiempo],
            format_func=lambda x: opciones_tiempo[x][1],
            value=0,
            key=f"b_time_{Nt}"
        )
        idx_t = val_slider if val_slider < Nt else (Nt - 1)
    else:
        idx_t = 0

    # Estructurar vista de grafico y métricas
    grafico, metricas = st.columns([3, 1])

    with metricas:
        # Métricas de energía
        st.metric("Bandgap Efectivo (Egap)", f"{labo.semi.Egap:.4f} eV")
        ei_centro = labo.semi.Eiv[0, idx_t]
        st.metric("Nivel Intrínseco en $x=0$ (Ei)", f"{ei_centro:.4f} eV")
        st.metric("Tensión de Deformación (Vapp)", f"{labo.V:.2f} V")

    with grafico:
        # Gráfico estructural cuántico (Ec, Ev, Ei, Efn, Efp)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.Ecv[:, idx_t], name="Banda Conducción (Ec)", line=dict(color='#d32f2f', width=3)))
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.Eiv[:, idx_t], name="Nivel Intrínseco (Ei)", line=dict(color='#d97706', width=1.5, dash='dash')))
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.Efn_i[:, idx_t], name="Cuasi-Fermi e⁻ (Efn)", line=dict(color='#15803d', width=2.5, dash='dashdot')))
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.Efp_i[:, idx_t], name="Cuasi-Fermi h⁺ (Efp)", line=dict(color='purple', width=2.5, dash='dashdot')))
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.Ev[:, idx_t], name="Banda Valencia (Ev)", line=dict(color='#1d4ed8', width=3)))
        
        fig.update_layout(
            template="plotly_white", xaxis_title="Posición x [cm]", yaxis_title="Energía [eV]",
            margin=dict(l=10, r=10, t=10, b=10), height=420, hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

def mostrar_tab_corrientes(labo):
    """Renderiza el perfil de corrientes de transporte a lo largo del elemento."""
    st.subheader("Distribución Espacial de Corrientes de Drift")
    Nt = len(labo.t)

    if Nt > 1:
        opciones_tiempo = [(i, f"t = {labo.t[i]*1e6:.3f} µs") for i in range(Nt)]
        val_slider = st.select_slider(
            "Evolución temporal (Corrientes):",
            options=[opt[0] for opt in opciones_tiempo],
            format_func=lambda x: opciones_tiempo[x][1],
            value=0,
            key=f"c_time_{Nt}"
        )
        idx_t = val_slider if val_slider < Nt else (Nt - 1)
    else:
        idx_t = 0

    # Estructurar vista de grafico y métricas
    grafico, metricas = st.columns([3, 1])

    with metricas:
        # Métricas de energía
        ubicacion_central = len(labo.semi.S_n)//2
        st.metric("Conductividad $e^-$ centro", f"{labo.semi.S_n[ubicacion_central, idx_t]:.4f} S/cm")
        st.metric("Conductividad $h^+$ centro", f"{labo.semi.S_p[ubicacion_central, idx_t]:.4f} S/cm")
        st.metric("Tensión aplicada (Vapp)", f"{labo.V:.2f} V")

    with grafico: 
        # Gráfico de vectores de corrientes (It, In, Ip) convertido a mA
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.It[:, idx_t]*1000, name="Corriente Total (It)", line=dict(color='black', width=3.5)))
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.In[:, idx_t]*1000, name="Drift Electrones (In)", line=dict(color='#b91c1c', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=labo.x, y=labo.semi.Ip[:, idx_t]*1000, name="Drift Huecos (Ip)", line=dict(color='#1d4ed8', width=2, dash='dot')))
        
        fig.update_layout(
            template="plotly_white", xaxis_title="Posición x [cm]", yaxis_title="Intensidad de Corriente [mA]",
            margin=dict(l=10, r=10, t=10, b=10), height=400, hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

def renderizar_pestaña_autor():
    """Imprime el bloque institucional fijo de firma del alumno desarrollador."""
    st.header("Acerca del Desarrollador")
    st.write("Este simulador fue desarrollado con fines pedagógicos para la comunidad de ingeniería.")
    st.markdown(
        """
        <div style='background-color: #1e2430; padding: 20px; border-radius: 10px; border-left: 5px solid #388e3c;'>
            <h3 style='margin-top: 0; color: #ffffff;'>Mis Datos</h3>
            <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Nombre y Apellido:</strong> Marco Maida</p>
            <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Carrera:</strong> Ingeniería Electrónica</p>
            <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Año de Cursada:</strong> 4to Año / 2026</p>
            <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Contacto:</strong> <a href='mailto:mmaidacapalbo@frba.utn.edu.ar' style='color: #388e3c;'>mmaidacapalbo@frba.utn.edu.ar</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# FLUJO PRINCIPAL DE EJECUCIÓN (ORQUESTADOR)
# =============================================================================

# 1. Ejecución de la Tab 2: Configuración de Parámetros del cristal
with tab_config:
    renderizar_pestaña_configuracion()

# 2. Ejecución de la Tab 3: Firma del Desarrollador
with tab_autor:
    renderizar_pestaña_autor()

# 3. Ejecución de la Tab 1: Consola Central del Laboratorio
with tab_simulador:
    st.title("Consola de Ensayos del Laboratorio Virtual")
    st.write("Configurá los grupos de parámetros en el Sidebar izquierdo. La barra se simulará dinámicamente.")

    # Dibujamos el Sidebar y capturamos el estado actual de los sliders
    with st.sidebar:
        mat, L, A, tau_p, T, Na, Nd, Vapp, trans, gl, dpn0, puntos_x = renderizar_sidebar_controles()

    # Instanciamos el laboratorio y cargamos el dispositivo
    labo = dispo.Laboratorio()
    labo.T = T
    labo.V = Vapp
    labo.GL = gl
    labo.dpn0 = dpn0
    labo.transitorio = trans
    labo.cargarSemi(material=mat, Nd=Nd, Na=Na, tau_p=tau_p, L=L, A=A)
    
    # Ejecutamos la simulación espacio-temporal completa (NumPy Vectorial)
    labo.simular(puntos_x=puntos_x)

    # Creamos las sub-pestañas internas para separar el tipo de dato gráfico
    subtab_portadores, subtab_bandas, subtab_corrientes = st.tabs([
        "Perfil de Portadores", 
        "Diagrama de Bandas", 
        "Corrientes de Drift"
    ])



    with subtab_portadores:
        mostrar_tab_portadores(labo)

    with subtab_bandas:
        mostrar_tab_bandas(labo)

    with subtab_corrientes:
        mostrar_tab_corrientes(labo)

