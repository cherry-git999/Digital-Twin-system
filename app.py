import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import serial

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Digital Twin SHM", layout="wide")

# -------------------------------
# SERIAL INIT (RUN ONCE)
# -------------------------------
if "ser" not in st.session_state:
    try:
        st.session_state.ser = serial.Serial('COM7', 115200, timeout=1)
        time.sleep(2)
    except:
        st.session_state.ser = None

# -------------------------------
# PREMIUM CSS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    text-align: center;
}
.big-title {
    font-size: 40px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🧠 Digital Twin - Structural Intelligence System</p>', unsafe_allow_html=True)

# -------------------------------
# SIDEBAR CONTROL PANEL
# -------------------------------
st.sidebar.header("🎮 Control Panel")

beam_type = st.sidebar.selectbox("Beam Type", 
    ["Simply Supported", "Cantilever", "Fixed", "Overhanging"])

length = st.sidebar.slider("Beam Length L (mm)", 400, 2000, 1000)

shape = st.sidebar.selectbox("Cross Section", ["Rectangular", "Circular"])

if shape == "Rectangular":
    b = st.sidebar.number_input("Breadth b (mm)", 10, 200, 40)
    d = st.sidebar.number_input("Depth d (mm)", 10, 200, 50)
else:
    D = st.sidebar.number_input("Diameter D (mm)", 10, 200, 40)

material = st.sidebar.selectbox("Material", ["Mild Steel", "Aluminum"])
load_type = st.sidebar.selectbox("Load Type", ["Point Load", "UDL"])

position = st.sidebar.slider("Load Position (mm)", 0, length, int(length/2))

apply_btn = st.sidebar.button("✅ Apply Input")

if "applied_position" not in st.session_state:
    st.session_state.applied_position = position

if apply_btn:
    st.session_state.applied_position = position
    st.sidebar.success("Input Applied ✅")

# -------------------------------
# MATERIAL
# -------------------------------
def get_material(mat):
    if mat == "Mild Steel":
        return 200e3, 250
    else:
        return 70e3, 150

E, allowable_stress = get_material(material)

# -------------------------------
# MOMENT OF INERTIA
# -------------------------------
if shape == "Rectangular":
    I = b * d**3 / 12
    y = d/2
else:
    I = (np.pi * D**4) / 64
    y = D/2

# -------------------------------
# READ DATA FROM ESP32
# -------------------------------
load = 0
deflection_actual = 0
strain = 0

if st.session_state.ser is not None:
    try:
        send_pos = st.session_state.applied_position
        st.session_state.ser.write(f"{send_pos}\n".encode())

        line = st.session_state.ser.readline().decode(errors='ignore').strip()

        if line:
            values = list(map(float, line.split(',')))
            if len(values) == 4:
                load, pos_from_esp, strain, deflection_actual = values

    except:
        pass

# -------------------------------
# DEFLECTION (THEORY)
# -------------------------------
if load_type == "Point Load":
    deflection_pred = (load * length**3) / (48 * E * I)
else:
    deflection_pred = (5 * load * length**4) / (384 * E * I)

# -------------------------------
# STRESS
# -------------------------------
M = load * length / 4
stress = (M * y) / I if I != 0 else 0

# -------------------------------
# HEALTH METRICS
# -------------------------------
fos = allowable_stress / stress if stress != 0 else 0
health = 100 - (stress / allowable_stress * 100) if allowable_stress != 0 else 0

# -------------------------------
# CPS LOGIC
# -------------------------------
if stress > allowable_stress or deflection_actual > deflection_pred * 1.5:
    status = "🔴 DANGER"
elif stress > allowable_stress * 0.7:
    status = "🟡 WARNING"
else:
    status = "🟢 SAFE"

# -------------------------------
# TOP PANEL
# -------------------------------
c1,c2,c3,c4,c5 = st.columns(5)

c1.markdown(f"<div class='card'><h4>Load</h4><h2>{round(load,2)} kg</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h4>Max Stress</h4><h2>{round(stress,2)}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h4>Deflection</h4><h2>{round(deflection_actual,2)} mm</h2></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'><h4>Health %</h4><h2>{round(health,1)}</h2></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='card'><h4>FoS</h4><h2>{round(fos,2)}</h2></div>", unsafe_allow_html=True)

st.markdown(f"### ⚙️ System Status: {status}")

# -------------------------------
# DIGITAL TWIN GRAPH
# -------------------------------
st.subheader("📊 Digital Twin")

x = np.linspace(0, length, 100)

y_pred = -deflection_pred * (x*(length-x)) / (length**2)

# ✅ FIX ADDED HERE (safe handling)
if deflection_pred != 0:
    y_real = y_pred * (deflection_actual / deflection_pred)
else:
    y_real = np.zeros_like(y_pred)

fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y_pred, name="Predicted", line=dict(width=4)))
fig.add_trace(go.Scatter(x=x, y=y_real, name="Actual", line=dict(width=4, dash='dash')))

fig.update_layout(template="plotly_dark", height=400)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# STRESS COLOR MAP
# -------------------------------
st.subheader("🌈 Stress Distribution")

colors = np.linspace(0, stress, len(x))

fig2 = go.Figure(go.Scatter(
    x=x, y=y_real,
    mode='markers',
    marker=dict(
        size=8,
        color=colors,
        colorscale='Jet',
        colorbar=dict(title="Stress")
    )
))

fig2.update_layout(template="plotly_dark", height=300)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# BOTTOM GRAPHS
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Load vs Deflection")
    st.line_chart(np.random.randn(20)+deflection_actual)

with col2:
    st.subheader("Load vs Strain")
    st.line_chart(np.random.randn(20)+strain)

# -------------------------------
# DEBUG
# -------------------------------
st.sidebar.write("Raw Data:", line if 'line' in locals() else "No Data")

# -------------------------------
# AUTO REFRESH
# -------------------------------
time.sleep(0.5)
st.rerun()