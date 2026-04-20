import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Digital Twin SHM", layout="wide")

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
    border: 1px solid rgba(255,255,255,0.1);
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
# SIDEBAR (CONTROL PANEL)
# -------------------------------
st.sidebar.header("🎮 Control Panel")

beam_type = st.sidebar.selectbox("Beam Type", 
    ["Simply Supported", "Cantilever", "Fixed", "Overhanging"])

length = st.sidebar.slider("Beam Length L (mm)", 500, 2000, 1000)

shape = st.sidebar.selectbox("Cross Section", ["Rectangular", "Circular"])

if shape == "Rectangular":
    b = st.sidebar.number_input("Breadth b (mm)", 10, 200, 40)
    d = st.sidebar.number_input("Depth d (mm)", 10, 200, 50)
else:
    D = st.sidebar.number_input("Diameter D (mm)", 10, 200, 40)

material = st.sidebar.selectbox("Material", ["Mild Steel", "Aluminum"])

load_type = st.sidebar.selectbox("Load Type", ["Point Load", "UDL"])

position = st.sidebar.slider("Load Position (mm)", 0, length, int(length/2))

# -------------------------------
# MATERIAL PROPERTIES
# -------------------------------
def get_material(material):
    if material == "Mild Steel":
        return 200e3, 250  # MPa units
    else:
        return 70e3, 150

E, allowable_stress = get_material(material)

# -------------------------------
# MOMENT OF INERTIA
# -------------------------------
def calc_I():
    if shape == "Rectangular":
        return b * d**3 / 12
    else:
        return (np.pi * D**4) / 64

I = calc_I()

# -------------------------------
# SENSOR INPUT (DUMMY NOW)
# -------------------------------
load = np.random.uniform(2, 8)
deflection_actual = np.random.uniform(1, 6)
strain = deflection_actual / length

# -------------------------------
# DEFLECTION FORMULAS
# -------------------------------
def calc_deflection():
    if load_type == "Point Load":
        return (load * length**3) / (48 * E * I)
    else:
        return (5 * load * length**4) / (384 * E * I)

deflection_pred = calc_deflection()

# -------------------------------
# STRESS CALCULATION
# -------------------------------
M = load * length / 4
y = (d/2) if shape=="Rectangular" else (D/2)
stress = (M * y) / I

# -------------------------------
# HEALTH METRICS
# -------------------------------
fos = allowable_stress / stress if stress != 0 else 0
health = 100 - (stress / allowable_stress * 100)

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

st.markdown(f"### System Status: {status}")

# -------------------------------
# DIGITAL TWIN GRAPH
# -------------------------------
st.subheader("📊 Digital Twin")

x = np.linspace(0, length, 100)

y_pred = -deflection_pred * (x*(length-x)) / (length**2)
y_real = y_pred * (deflection_actual / deflection_pred)

fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=y_pred, name="Predicted", line=dict(width=4)))
fig.add_trace(go.Scatter(x=x, y=y_real, name="Actual", line=dict(width=4, dash='dash')))

fig.update_layout(template="plotly_dark", height=400)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# STRESS COLOR MAP (SIMULATED)
# -------------------------------
st.subheader("🌈 Stress Distribution")

colors = np.linspace(0, stress, len(x))

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
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
# AUTO REFRESH
# -------------------------------
time.sleep(0.8)
st.rerun()