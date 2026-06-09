import streamlit as st
import numpy as np
import Funciones_dispo as dispo
from constantes import Materiales, PARAMETROS
import graficar as vis

st.set_page_config(page_title="Laboratorio Virtual de Semiconductores", layout="wide")

if "mis_parametros" not in st.session_state:
    st.session_state.mis_parametros = PARAMETROS.copy()

tab_simulador, tab_config, tab_autor = st.tabs(["📊 Simulador", "⚙️ Tabla de Constantes", "👨‍💻 Autor"])

# ----------------- TABLA DE CONSTANTES -----------------
with tab_config:
    st.header("📋 Tabla de Constantes del Material")
    st.write("Modificá los valores de los campos según los datos de tu cátedra y hacé clic en **Guardar Cambios**.")

    with st.form("form_constantes"):
        # --- ENCABEZADOS DE LA TABLA ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1])
        with c_prop: st.markdown("**Propiedad / Variable**")
        with c_si: st.markdown("**Silicio (Si)**")
        with c_ge: st.markdown("**Germanio (Ge)**")
        with c_asga: st.markdown("**Arseniuro de Galio (GaAs)**")
        st.markdown("---") 

        # --- FILA 1: Bandgap Inicial ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Bandgap Inicial ($E_{g0}$) [eV]")
        with c_si: gap_o_si = st.number_input("gap_o_si", value=st.session_state.mis_parametros["Si"]["gap_o"], format="%.3f", label_visibility="collapsed")
        with c_ge: gap_o_ge = st.number_input("gap_o_ge", value=st.session_state.mis_parametros["Ge"]["gap_o"], format="%.3f", label_visibility="collapsed")
        with c_asga: gap_o_asga = st.number_input("gap_o_asga", value=st.session_state.mis_parametros["AsGa"]["gap_o"], format="%.3f", label_visibility="collapsed")

        # --- FILA 2: Nc/T^1.5 ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("$N_c$")
        with c_si: nc_si = st.number_input("nc_si", value=float(st.session_state.mis_parametros["Si"]["nc"]), format="%.4e", label_visibility="collapsed")
        with c_ge: nc_ge = st.number_input("nc_ge", value=float(st.session_state.mis_parametros["Ge"]["nc"]), format="%.4e", label_visibility="collapsed")
        with c_asga: nc_asga = st.number_input("nc_asga", value=float(st.session_state.mis_parametros["AsGa"]["nc"]), format="%.4e", label_visibility="collapsed")
        
        # --- FILA 3: Nv/T^1.5 ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("$N_v$")
        with c_si: nv_si = st.number_input("nv_si", value=float(st.session_state.mis_parametros["Si"]["nv"]), format="%.4e", label_visibility="collapsed")
        with c_ge: nv_ge = st.number_input("nv_ge", value=float(st.session_state.mis_parametros["Ge"]["nv"]), format="%.4e", label_visibility="collapsed")
        with c_asga: nv_asga = st.number_input("nv_asga", value=float(st.session_state.mis_parametros["AsGa"]["nv"]), format="%.4e", label_visibility="collapsed")

        # --- FILA 4: Alpha ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Alpha ($\Alpha$) de Varshni")
        with c_si: alpha_si = st.number_input("alpha_si", value=float(st.session_state.mis_parametros["Si"]["alpha"]), format="%.3e", label_visibility="collapsed")
        with c_ge: alpha_ge = st.number_input("alpha_ge", value=float(st.session_state.mis_parametros["Ge"]["alpha"]), format="%.3e", label_visibility="collapsed")
        with c_asga: alpha_asga = st.number_input("alpha_asga", value=float(st.session_state.mis_parametros["AsGa"]["alpha"]), format="%.3e", label_visibility="collapsed")

        # --- FILA 5: Beta ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("Beta ($\Beta$) de Varshni")
        with c_si: betha_si = st.number_input("betha_si", value=float(st.session_state.mis_parametros["Si"]["betha"]), format="%.1f", label_visibility="collapsed")
        with c_ge: betha_ge = st.number_input("betha_ge", value=float(st.session_state.mis_parametros["Ge"]["betha"]), format="%.1f", label_visibility="collapsed")
        with c_asga: betha_asga = st.number_input("betha_asga", value=float(st.session_state.mis_parametros["AsGa"]["betha"]), format="%.1f", label_visibility="collapsed")

        # --- FILA 6: Movilidad Electrones ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("$\mu_n$")
        with c_si: mn_si = st.number_input("mn_si", value=float(st.session_state.mis_parametros["Si"]["movility_n"]), format="%.1f", label_visibility="collapsed")
        with c_ge: mn_ge = st.number_input("mn_ge", value=float(st.session_state.mis_parametros["Ge"]["movility_n"]), format="%.1f", label_visibility="collapsed")
        with c_asga: mn_asga = st.number_input("mn_asga", value=float(st.session_state.mis_parametros["AsGa"]["movility_n"]), format="%.1f", label_visibility="collapsed")

        # --- FILA 7: Movilidad Huecos ---
        c_prop, c_si, c_ge, c_asga = st.columns([2.5, 1, 1, 1], vertical_alignment="center")
        with c_prop: st.markdown("$\mu_p$")
        with c_si: mp_si = st.number_input("mp_si", value=float(st.session_state.mis_parametros["Si"]["movility_p"]), format="%.1f", label_visibility="collapsed")
        with c_ge: mp_ge = st.number_input("mp_ge", value=float(st.session_state.mis_parametros["Ge"]["movility_p"]), format="%.1f", label_visibility="collapsed")
        with c_asga: mp_asga = st.number_input("mp_asga", value=float(st.session_state.mis_parametros["AsGa"]["movility_p"]), format="%.1f", label_visibility="collapsed")

        st.markdown("---")
        
        boton_guardar = st.form_submit_button("💾 Guardar Cambios")
        
        if boton_guardar:

            
            st.session_state.mis_parametros = {
                "Si": {"name": "Silicio", "gap_o": gap_o_si, "nc": nc_si, "nv": nv_si, "alpha": alpha_si, "betha": betha_si, "movility_n": mn_si, "movility_p": mp_si},
                "Ge": {"name": "Germanio", "gap_o": gap_o_ge, "nc": nc_ge, "nv": nv_ge, "alpha": alpha_ge, "betha": betha_ge, "movility_n": mn_ge, "movility_p": mp_ge},
                "AsGa": {"name": "Arseniuro de Galio", "gap_o": gap_o_asga, "nc": nc_asga, "nv": nv_asga, "alpha": alpha_asga, "betha": betha_asga, "movility_n": mn_asga, "movility_p": mp_asga}
            }
            st.success("¡Constantes actualizadas con éxito! Volvé a la pestaña del Simulador.")

# ----------------- SIMULADOR PRINCIPAL -----------------

with tab_simulador:
    st.title("⚡ Simulador de Dispositivos Electrónicos")
    st.write("Modificá los parámetros en el panel izquierdo para actualizar el simulador en tiempo real.")

    # SIDEBAR DE PARAMETROS
    with st.sidebar:
        st.header("🎛️ Parámetros de Entrada")
        
        # Selección de materiales
        material_elegido = st.selectbox(
            "Seleccioná el Material:",
            options=[Materiales.SI, Materiales.GE, Materiales.ASGA],
            format_func=lambda x: "Silicio (Si)" if x == Materiales.SI else ("Germanio (Ge)" if x == Materiales.GE else "Arseniuro de Galio (GaAs)")
        )

        # Temperatura del material
        temperatura = st.slider("Temperatura [K]:", min_value=100, max_value=600, value=300, step=10)

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

    st.subheader("📊 Resultados Numéricos")
    
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
        st.subheader("📈 Diagrama de Niveles de Energía")
        vis.graficarApp(semi)
        st.plotly_chart(vis.figura_actual, use_container_width=True)

    with col_tablas:
        st.subheader("📌 Distancias y Brechas Energéticas")
        
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
    st.subheader("🚗 Corrientes de Drift")
    
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
    st.header("👨‍💻 Acerca del Desarrollador")
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
