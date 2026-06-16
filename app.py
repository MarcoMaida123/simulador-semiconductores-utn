import streamlit as st
import numpy as np
import Funciones_dispo as dispo
from constantes import Materiales, PARAMETROS
import graficar as vis

st.set_page_config(page_title="Laboratorio Virtual de Semiconductores", layout="wide")

if "mis_parametros" not in st.session_state:
    st.session_state.mis_parametros = PARAMETROS.copy()

tab_simulador, tab_config, tab_autor = st.tabs(["Simulador", "Tabla de Constantes", "Autor"])

# ----------------- TABLA DE CONSTANTES -----------------
# ----------------- TABLA DE CONSTANTES -----------------
with tab_config:
    st.header("Tabla de Constantes del Material")
    st.write("Modificá los valores de los campos según los datos de tu cátedra y hacé clic en **Guardar Cambios**.")

    with st.form("form_constantes"):
        
        # =========================================================================
        # PARTE 1: PARÁMETROS TÍPICOS / COMUNES (A 300K)
        # =========================================================================
        st.subheader("Parámetros Típicos / Comunes (a 300K)")
        st.caption("Valores estándar tabulados para condiciones normales de laboratorio.")
        
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1])
        with c_prop: st.markdown("**Propiedad / Variable**")
        with c_si: st.markdown("**Silicio (Si)**")
        with c_ge: st.markdown("**Germanio (Ge)**")
        with c_asga: st.markdown("**Arseniuro de Galio (GaAs)**")
        st.markdown("---") 

        # --- FILA: Bandgap Inicial ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Bandgap a 300K ($E_g$) [eV]")
        with c_si: gap_si = st.number_input("gap_si", value=float(st.session_state.mis_parametros["Si"]["gap"]), format="%.3f", label_visibility="collapsed")
        with c_ge: gap_ge = st.number_input("gap_ge", value=float(st.session_state.mis_parametros["Ge"]["gap"]), format="%.3f", label_visibility="collapsed")
        with c_asga: gap_asga = st.number_input("gap_asga", value=float(st.session_state.mis_parametros["AsGa"]["gap"]), format="%.3f", label_visibility="collapsed")

        # --- FILA: Nc ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Efectiva en Conducción ($N_c$) [cm⁻³]")
        with c_si: nc_si = st.number_input("nc_si", value=float(st.session_state.mis_parametros["Si"]["nc"]), format="%.4e", label_visibility="collapsed")
        with c_ge: nc_ge = st.number_input("nc_ge", value=float(st.session_state.mis_parametros["Ge"]["nc"]), format="%.4e", label_visibility="collapsed")
        with c_asga: nc_asga = st.number_input("nc_asga", value=float(st.session_state.mis_parametros["AsGa"]["nc"]), format="%.4e", label_visibility="collapsed")
        
        # --- FILA: Nv ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Efectiva en Valencia ($N_v$) [cm⁻³]")
        with c_si: nv_si = st.number_input("nv_si", value=float(st.session_state.mis_parametros["Si"]["nv"]), format="%.4e", label_visibility="collapsed")
        with c_ge: nv_ge = st.number_input("nv_ge", value=float(st.session_state.mis_parametros["Ge"]["nv"]), format="%.4e", label_visibility="collapsed")
        with c_asga: nv_asga = st.number_input("nv_asga", value=float(st.session_state.mis_parametros["AsGa"]["nv"]), format="%.4e", label_visibility="collapsed")

        # --- FILA: Movilidad Electrones ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Movilidad de electrones ($\mu_n$) [cm²/V·s]")
        with c_si: mn_si = st.number_input("mn_si", value=float(st.session_state.mis_parametros["Si"]["mu_n"]), format="%.1f", label_visibility="collapsed")
        with c_ge: mn_ge = st.number_input("mn_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_n"]), format="%.1f", label_visibility="collapsed")
        with c_asga: mn_asga = st.number_input("mn_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_n"]), format="%.1f", label_visibility="collapsed")

        # --- FILA: Movilidad Huecos ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Movilidad de huecos ($\mu_p$) [cm²/V·s]")
        with c_si: mp_si = st.number_input("mp_si", value=float(st.session_state.mis_parametros["Si"]["mu_p"]), format="%.1f", label_visibility="collapsed")
        with c_ge: mp_ge = st.number_input("mp_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_p"]), format="%.1f", label_visibility="collapsed")
        with c_asga: mp_asga = st.number_input("mp_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_p"]), format="%.1f", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True) # Espaciador visual

        # =========================================================================
        # PARTE 2: CONSTANTES ESPECÍFICAS (DEPENDENCIA TÉRMICA)
        # =========================================================================
        st.subheader("Coeficientes de Dependencia Térmica")
        st.caption("Parámetros empíricos avanzados que modelan la variación respecto a la temperatura.")
        
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1])
        with c_prop: st.markdown("**Propiedad / Variable**")
        with c_si: st.markdown("**Silicio (Si)**")
        with c_ge: st.markdown("**Germanio (Ge)**")
        with c_asga: st.markdown("**Arseniuro de Galio (GaAs)**")
        st.markdown("---") 

        # --- FILA: Alpha ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Alpha ($\alpha$) de Varshni [eV/K]")
        with c_si: alpha_si = st.number_input("alpha_si", value=float(st.session_state.mis_parametros["Si"]["alpha"]), format="%.3e", label_visibility="collapsed")
        with c_ge: alpha_ge = st.number_input("alpha_ge", value=float(st.session_state.mis_parametros["Ge"]["alpha"]), format="%.3e", label_visibility="collapsed")
        with c_asga: alpha_asga = st.number_input("alpha_asga", value=float(st.session_state.mis_parametros["AsGa"]["alpha"]), format="%.3e", label_visibility="collapsed")

        # --- FILA: Beta ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Beta ($\beta$) de Varshni [K]")
        with c_si: beta_si = st.number_input("beta_si", value=float(st.session_state.mis_parametros["Si"]["beta"]), format="%.1f", label_visibility="collapsed")
        with c_ge: beta_ge = st.number_input("beta_ge", value=float(st.session_state.mis_parametros["Ge"]["beta"]), format="%.1f", label_visibility="collapsed")
        with c_asga: beta_asga = st.number_input("beta_asga", value=float(st.session_state.mis_parametros["AsGa"]["beta"]), format="%.1f", label_visibility="collapsed")

        # --- FILA: Exponente Movilidad n ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Exponente Temp. de $\mu_n$")
        with c_si: exp_n_si = st.number_input("exp_n_si", value=float(st.session_state.mis_parametros["Si"]["mu_n-exp"]), format="%.2f", label_visibility="collapsed")
        with c_ge: exp_n_ge = st.number_input("exp_n_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_n-exp"]), format="%.2f", label_visibility="collapsed")
        with c_asga: exp_n_asga = st.number_input("exp_n_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_n-exp"]), format="%.2f", label_visibility="collapsed")

        # --- FILA: Exponente Movilidad p ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Exponente Temp. de $\mu_p$")
        with c_si: exp_p_si = st.number_input("exp_p_si", value=float(st.session_state.mis_parametros["Si"]["mu_p-exp"]), format="%.2f", label_visibility="collapsed")
        with c_ge: exp_p_ge = st.number_input("exp_p_ge", value=float(st.session_state.mis_parametros["Ge"]["mu_p-exp"]), format="%.2f", label_visibility="collapsed")
        with c_asga: exp_p_asga = st.number_input("exp_p_asga", value=float(st.session_state.mis_parametros["AsGa"]["mu_p-exp"]), format="%.2f", label_visibility="collapsed")

        st.markdown("---")
        
        boton_guardar = st.form_submit_button("💾 Guardar Cambios")
        
        if boton_guardar:
            st.session_state.mis_parametros = {
                "Si": {"name": "Silicio", "gap": gap_si, "nc": nc_si, "nv": nv_si, "alpha": alpha_si, "beta": beta_si, "mu_n": mn_si, "mu_n-exp": exp_n_si, "mu_p": mp_si, "mu_p-exp": exp_p_si},
                "Ge": {"name": "Germanio", "gap": gap_ge, "nc": nc_ge, "nv": nv_ge, "alpha": alpha_ge, "beta": beta_ge, "mu_n": mn_ge, "mu_n-exp": exp_n_ge, "mu_p": mp_ge, "mu_p-exp": exp_p_ge},
                "AsGa": {"name": "Arseniuro de Galio", "gap": gap_asga, "nc": nc_asga, "nv": nv_asga, "alpha": alpha_asga, "beta": beta_asga, "mu_n": mn_asga, "mu_n-exp": exp_n_asga, "mu_p": mp_asga, "mu_p-exp": exp_p_asga}
            }
            st.success("¡Constantes actualizadas con éxito! Volvé a la pestaña del Simulador.")
# ----------------- SIMULADOR PRINCIPAL -----------------

with tab_simulador:
    st.title("Laboratorio Virtual de Semiconductores")
    st.write("Modificá los parámetros en el panel izquierdo para actualizar el simulador en tiempo real.")

    # SIDEBAR DE PARAMETROS
    with st.sidebar:
        st.header("Parámetros de Entrada")
        
        # Selección de materiales
        material_elegido = st.selectbox(
            "Seleccioná el Material:",
            options=[Materiales.SI, Materiales.GE, Materiales.ASGA],
            format_func=lambda x: "Silicio (Si)" if x == Materiales.SI else ("Germanio (Ge)" if x == Materiales.GE else "Arseniuro de Galio (GaAs)")
        )

        # Temperatura del material
        temperatura = st.slider("Temperatura [K]:", min_value=100, max_value=600, value=300, step=5)

        # Dopaje del material
        st.subheader("🧪 Dopaje [cm^-3]")
        Na = st.number_input("Aceptores ($N_a$):", min_value=0.0, value=0.0, format="%.2e")
        Nd = st.number_input("Donores ($N_d$):", min_value=0.0, value=0.0, format="%.2e")

        # Agente Externo
        st.subheader("🔌 Agentes Externos")
        longitud = st.number_input("Longitud ($cm$):", min_value=0.0000001, value=1.0, format="%.2e")
        area = st.number_input("Área ($cm^2$):", min_value=0.0000001, value=1.0, format="%.2e")
        tension = st.slider("Tensión Aplicada [V] (V(0) = Vapp):", min_value=-5.0, max_value=5.0, value=0.0, step=0.1)

    # Guardamos parametros actuales en la sesion
    dispo.PARAMETROS = st.session_state.mis_parametros

    # Instanciamos el semiconductor a trabajar
    semi = dispo.Semiconductor(material_elegido, T=temperatura, Na=Na, Nd=Nd, V=tension, L=longitud, A=area)

    st.subheader("Resultados Numéricos")
    
    # Métricas base: GAP, concentraciones y conductividades
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(
            vis.mostrarCajaHTML("Bandgap (E<sub>g</sub>)", f"{semi.Egap:.4f}", "eV") +
            vis.mostrarCajaHTML("Concentración Intrínseca (n<sub>i</sub>)", f"{semi.ni:.4e}", "cm⁻³"),
            unsafe_allow_html=True
        )

    with m_col2:
        st.markdown(
            vis.mostrarCajaHTML("Electrones en Conducción (n<sub>0</sub>)", f"{semi.no:.4e}", "cm⁻³") +
            vis.mostrarCajaHTML("Huecos en Valencia (p<sub>0</sub>)", f"{semi.po:.4e}", "cm⁻³"),
            unsafe_allow_html=True
        )
    
    with m_col3:
        st.markdown(
            vis.mostrarCajaHTML("Conductividad Electrones (&sigma;<sub>n</sub>)", f"{semi.S_n:.4e}", "S/cm") +
            vis.mostrarCajaHTML("Conductividad Huecos (&sigma;<sub>p</sub>)", f"{semi.S_h:.4e}", "S/cm"),
            unsafe_allow_html=True
        )

    st.markdown("---")
    
    # Tabla de diagramas de Banda y distancias calculadas entre niveles
    col_grafico, col_tablas = st.columns([1.5, 1])

    with col_grafico:
        st.subheader("Diagrama de Niveles de Energía")
        vis.graficarApp(semi)
        st.plotly_chart(vis.figura_actual, use_container_width=True)

    with col_tablas:
        st.subheader("Distancias y Brechas Energéticas")
        
        Ecv, Efv, Eiv, Ev, x = semi.calcBandas()

        dist_Ec_Ev = semi.Egap
        dist_Ec_Ef = Ecv[0] - Efv[0]
        dist_Ec_Ei = np.abs(Ecv[0] - Eiv[0])
        dist_Ei_Ref = np.abs(Eiv[0] - Efv[0])
        dist_Ev_Ef = Efv[0]
        dist_Ev_Ei = Eiv[0]

        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.markdown(vis.mostrarCajaHTML("Brecha Principal (E<sub>c</sub> - E<sub>v</sub>)", f"{dist_Ec_Ev:.4f}", "eV"), unsafe_allow_html=True)
            st.markdown(vis.mostrarCajaHTML("Distancia (E<sub>c</sub> - E<sub>f</sub>)", f"{dist_Ec_Ef:.4f}", "eV"), unsafe_allow_html=True)
            st.markdown(vis.mostrarCajaHTML("Distancia (E<sub>c</sub> - E<sub>i</sub>)", f"{dist_Ec_Ei:.4f}", "eV"), unsafe_allow_html=True)

        with b_col2:
            st.markdown(vis.mostrarCajaHTML("Distancia (E<sub>i</sub> - E<sub>f</sub>)", f"{dist_Ei_Ref:.4f}", "eV"), unsafe_allow_html=True)
            st.markdown(vis.mostrarCajaHTML("Distancia (E<sub>v</sub> - E<sub>f</sub>)", f"{dist_Ev_Ef:.4f}", "eV"), unsafe_allow_html=True)
            st.markdown(vis.mostrarCajaHTML("Distancia (E<sub>v</sub> - E<sub>i</sub>)", f"{dist_Ev_Ei:.4f}", "eV"), unsafe_allow_html=True)
    st.markdown("---")
    
    # Corrientes de DRIFT calculadas
    st.subheader("Corrientes de Drift")
    
    It, In, Ip = semi.calcCorrientes()

    i_col1, i_col2, i_col3 = st.columns(3)
    with i_col1:
        st.markdown(vis.mostrarCajaHTML("Corriente Total (I<sub>t</sub>)", f"{It:.4e}", "A"), unsafe_allow_html=True)
    with i_col2:
        st.markdown(vis.mostrarCajaHTML("Corriente de h<sup>+</sup> (I<sub>p</sub>)", f"{Ip:.4e}", "A"), unsafe_allow_html=True)
    with i_col3:
        st.markdown(vis.mostrarCajaHTML("Corriente de e<sup>-</sup> (I<sub>n</sub>)", f"{In:.4e}", "A"), unsafe_allow_html=True)

# ----------------- DATOS MIOS -----------------
with tab_autor:
    st.header("Acerca del Desarrollador")
    st.write("Este simulador fue desarrollado con fines pedagógicos para la comunidad de ingeniería.")
    
    st.markdown(
            """
            <div style='background-color: #1e2430; padding: 20px; border-radius: 10px; border-left: 5px solid #388e3c;'>
                <h3 style='margin-top: 0; color: #ffffff;'>Mis Datos</h3>
                <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Nombre y Apellido:</strong> Marco Maida</p>
                <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Carrera:</strong> Ingeniería Electrónica</p>
                <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Año de Cursada:</strong> 4to Año / 2026</p>
                <p style='margin: 6px 0; font-size: 16px;'><strong style='color: #a3b8cc;'>Contacto:</strong> <a href='mmaidacapalbo@frba.utn.edu.ar' style='color: #388e3c;'>mmaidacapalbo@frba.utn.edu.ar</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )
