# 🧠 Digital Twin - Structural Intelligence System

A real-time Structural Health Monitoring (SHM) system that combines theoretical analysis with actual sensor data to monitor and assess the health of structural beams. This application uses a digital twin approach to compare predicted vs. actual beam behavior.

## 📋 Features

- **Real-time Monitoring**: Live data streaming from ESP32 sensors via serial communication (COM7, 115200 baud rate)
- **Multiple Beam Types**: Support for Simply Supported, Cantilever, Fixed, and Overhanging beams
- **Flexible Cross-Sections**: Rectangular and Circular cross-section support
- **Material Selection**: Support for Mild Steel and Aluminum materials
- **Load Analysis**: Point Load and Uniform Distributed Load (UDL) calculations
- **Digital Twin Visualization**: Compare predicted deflection with actual measured deflection
- **Health Metrics Dashboard**: 
  - Real-time load measurement
  - Maximum stress calculation
  - Deflection monitoring
  - Structural health percentage
  - Factor of Safety (FoS)
- **Stress Distribution**: Color-mapped visualization of stress across the beam
- **System Status Indicator**: 
  - 🟢 SAFE: Normal operating condition
  - 🟡 WARNING: Stress exceeds 70% of allowable threshold
  - 🔴 DANGER: Stress exceeds allowable limit or deflection is 1.5x higher than predicted
- **Interactive Control Panel**: Adjust beam parameters in real-time and see results instantly

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Virtual environment (`.venv`)
- ESP32 microcontroller with sensor data (optional for demo mode)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/cherry-git999/Digital-Twin-system.git
   cd "Digital Twin system"
   ```

2. **Create and activate virtual environment** (if not already created):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or manually install:
   ```bash
   pip install streamlit numpy plotly pyserial
   ```

### Running the Application

```bash
.venv\Scripts\activate; streamlit run app.py
```

The application will start and be accessible at `http://localhost:8501` in your default web browser.

## 🎮 Usage Guide

### Control Panel (Left Sidebar)

1. **Beam Type**: Select from Simply Supported, Cantilever, Fixed, or Overhanging configurations
2. **Beam Length**: Set the beam length in millimeters (400-2000 mm)
3. **Cross Section**: Choose Rectangular or Circular cross-section
   - For Rectangular: Specify breadth (b) and depth (d)
   - For Circular: Specify diameter (D)
4. **Material**: Select Mild Steel or Aluminum
5. **Load Type**: Choose between Point Load or UDL (Uniform Distributed Load)
6. **Load Position**: Specify where the load is applied along the beam
7. **Apply Input**: Click to confirm settings and update calculations

### Dashboard Metrics

- **Load**: Current load in kilograms from the sensor
- **Max Stress**: Maximum stress experienced by the beam
- **Deflection**: Current vertical deflection of the beam in millimeters
- **Health %**: Structural health percentage (100% = optimal condition)
- **FoS**: Factor of Safety (higher is safer)

### Visualizations

- **Digital Twin Graph**: Compares predicted vs. actual deflection profiles
- **Stress Distribution**: Heat map showing stress concentration along the beam
- **Load vs Deflection**: Real-time trend of load-deflection relationship
- **Load vs Strain**: Real-time strain measurements

## 🔧 Configuration

### Serial Connection (ESP32)
- **Port**: COM7 (configurable in code)
- **Baud Rate**: 115200
- **Timeout**: 1 second
- **Data Format**: Expected CSV format from ESP32: `load, position, strain, deflection_actual`

### Material Properties

| Material | Young's Modulus (E) | Allowable Stress |
|----------|-------------------|-----------------|
| Mild Steel | 200,000 MPa | 250 MPa |
| Aluminum | 70,000 MPa | 150 MPa |

### Beam Type Formulas

**Deflection Calculation:**
- Point Load: δ = (P × L³) / (48 × E × I)
- UDL: δ = (5 × w × L⁴) / (384 × E × I)

**Maximum Moment:**
- M = P × L / 4

**Stress:**
- σ = (M × y) / I

Where:
- P = Point load
- w = Distributed load
- L = Beam length
- E = Young's Modulus
- I = Moment of inertia
- y = Distance from neutral axis

## 📁 Project Structure

```
Digital Twin system/
├── app.py                 # Main Streamlit application
├── .venv/                 # Virtual environment
├── .git/                  # Git repository
├── .vscode/               # VS Code settings
└── README.md              # This file
```

## 🔌 Hardware Requirements

- **Microcontroller**: ESP32 with analog sensors
- **Sensors Required**:
  - Load cell / Force sensor
  - Displacement/deflection sensor
  - Strain gauge
- **Connection**: USB-to-Serial cable to COM7

## 📊 Calculation Details

### Moment of Inertia
- **Rectangular**: I = (b × d³) / 12
- **Circular**: I = (π × D⁴) / 64

### Health Calculation
```
Health % = 100 - (Current Stress / Allowable Stress × 100)
```

### Factor of Safety
```
FoS = Allowable Stress / Current Stress
```

## ⚠️ Status Indicators

| Status | Condition |
|--------|-----------|
| 🟢 SAFE | Stress < 70% of allowable & Deflection normal |
| 🟡 WARNING | 70% ≤ Stress < 100% of allowable |
| 🔴 DANGER | Stress ≥ allowable OR Deflection > 1.5× predicted |

## 🌐 User Interface

The application features a modern, dark-themed interface with:
- Glassmorphism design cards
- Real-time metric updates
- Interactive Plotly graphs
- Responsive layout (wide mode)
- Color-coded visualizations

## 📝 Notes

- Application auto-refreshes every 0.5 seconds for real-time updates
- If ESP32 is not connected, the application will run in demo mode with zero values
- Debug data from serial connection is displayed in the sidebar
- All calculations follow standard structural mechanics formulas

## 🐛 Troubleshooting

**No data from ESP32?**
- Check COM port and baud rate settings
- Verify USB cable connection
- Ensure ESP32 firmware is properly programmed
- Check data format: `load, position, strain, deflection_actual`

**Application crashes?**
- Ensure all dependencies are installed
- Check Python version compatibility
- Verify serial port is not in use by another application

## 📚 Requirements

See dependencies in the code:
- `streamlit` - Web app framework
- `numpy` - Numerical computations
- `plotly` - Interactive graphing
- `pyserial` - Serial communication

## 👥 Developer

Cherry Git999

## 📄 License

[Add your license here]

## 🔄 Future Enhancements

- [ ] Database logging for historical analysis
- [ ] Predictive maintenance alerts
- [ ] Multi-beam monitoring
- [ ] Advanced fatigue analysis
- [ ] Cloud data synchronization
- [ ] Mobile app integration

---

**Last Updated**: May 2026
**Version**: 1.0
