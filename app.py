import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Digital Twin Pro", layout="wide")

# -------------------------------
# CSS
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
</style>
""", unsafe_allow_html=True)

st.title("🧠 Digital Twin - Structural Intelligence System")

# -------------------------------
# SESSION STATE (HISTORY)
# -------------------------------
if "load_hist" not in st.session_state:
    st.session_state.load_hist = []
    st.session_state.def_hist = []
    st.session_state.strain_hist = []

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("🎮 Control Panel")

beam_type = st.sidebar.selectbox("Beam Type", 
["Simply Supported", "Cantilever", "Fixed"])

length = st.sidebar.slider("Length (mm)", 500, 2000, 1000)

shape = st.sidebar.selectbox("Section", ["Rectangular","Circular"])

if shape == "Rectangular":
    b = st.sidebar.number_input("b",10,200,40)
    d = st.sidebar.number_input("d",10,200,50)
else:
    D = st.sidebar.number_input("D",10,200,40)

material = st.sidebar.selectbox("Material", ["Steel","Aluminum"])
load_type = st.sidebar.selectbox("Load Type", ["Point","UDL"])
position = st.sidebar.slider("Position",0,length,int(length/2))

# -------------------------------
# MATERIAL
# -------------------------------
if material=="Steel":
    E, allowable = 200e3, 250
else:
    E, allowable = 70e3, 150

# -------------------------------
# INERTIA
# -------------------------------
if shape=="Rectangular":
    I = b*d**3/12
    y = d/2
else:
    I = np.pi*D**4/64
    y = D/2

# -------------------------------
# SENSOR (DUMMY NOW)
# -------------------------------
load = np.random.uniform(2,8)
deflection_actual = np.random.uniform(1,6)
strain = deflection_actual/length

# -------------------------------
# ML MODEL
# -------------------------------
X = np.array([[2,200],[4,500],[6,800],[8,1000]])
y_ml = np.array([1,3,5,7])
model = LinearRegression().fit(X,y_ml)

pred_deflection_ml = model.predict([[load,position]])[0]

# -------------------------------
# PHYSICS DEFLECTION
# -------------------------------
deflection_pred = (load*length**3)/(48*E*I)

# -------------------------------
# STRESS
# -------------------------------
M = load*length/4
stress = (M*y)/I

# -------------------------------
# HEALTH
# -------------------------------
fos = allowable/stress if stress!=0 else 0
health = 100 - (stress/allowable*100)

# -------------------------------
# CPS
# -------------------------------
if stress>allowable or deflection_actual>deflection_pred*1.5:
    status="🔴 DANGER"
elif stress>0.7*allowable:
    status="🟡 WARNING"
else:
    status="🟢 SAFE"

# -------------------------------
# STORE HISTORY
# -------------------------------
st.session_state.load_hist.append(load)
st.session_state.def_hist.append(deflection_actual)
st.session_state.strain_hist.append(strain)

# -------------------------------
# TOP PANEL
# -------------------------------
c1,c2,c3,c4,c5 = st.columns(5)

c1.markdown(f"<div class='card'>Load<br>{round(load,2)}</div>",unsafe_allow_html=True)
c2.markdown(f"<div class='card'>Stress<br>{round(stress,2)}</div>",unsafe_allow_html=True)
c3.markdown(f"<div class='card'>Deflection<br>{round(deflection_actual,2)}</div>",unsafe_allow_html=True)
c4.markdown(f"<div class='card'>Health<br>{round(health,1)}%</div>",unsafe_allow_html=True)
c5.markdown(f"<div class='card'>FoS<br>{round(fos,2)}</div>",unsafe_allow_html=True)

st.subheader(f"System Status: {status}")

# -------------------------------
# DIGITAL TWIN (3D EFFECT)
# -------------------------------
x = np.linspace(0,length,100)

y_pred = -deflection_pred*(x*(length-x))/length**2
y_real = y_pred*(deflection_actual/deflection_pred)

fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=x,
    y=y_pred,
    z=np.sin(x/200)*5,
    mode='lines',
    name="Predicted"
))

fig.add_trace(go.Scatter3d(
    x=x,
    y=y_real,
    z=np.sin(x/200)*5,
    mode='lines',
    name="Actual"
))

fig.update_layout(
    template="plotly_dark",
    height=400
)

st.plotly_chart(fig,use_container_width=True)

# -------------------------------
# STRESS MAP
# -------------------------------
colors = np.linspace(0,stress,len(x))

fig2 = go.Figure(go.Scatter(
    x=x,y=y_real,
    mode='markers',
    marker=dict(
        color=colors,
        colorscale='Jet',
        size=8,
        colorbar=dict(title="Stress")
    )
))

fig2.update_layout(template="plotly_dark",height=300)

st.plotly_chart(fig2,use_container_width=True)

# -------------------------------
# BOTTOM GRAPHS
# -------------------------------
col1,col2 = st.columns(2)

with col1:
    st.subheader("Load vs Deflection")
    st.line_chart(st.session_state.def_hist)

with col2:
    st.subheader("Load vs Strain")
    st.line_chart(st.session_state.strain_hist)

# -------------------------------
# AUTO REFRESH
# -------------------------------
time.sleep(0.8)
st.experimental_rerun()