![](https://raw.githubusercontent.com/RipunjayS109/firevizz/main/bannerFV1.png)

# 🔥 FireVizz


A Python library for **visualizing** and **analyzing fire detection data** from sensor networks.  

---

## ✨ Features

- 🗺️ **Interactive map** visualization of fire sensor data  
- 🤖 **Real-time fire prediction** using machine learning models  
- 🌡️ **Heatmap** visualization for various sensor parameters  
- 📤 Export of fire prediction coordinates and sensor data  
- 🔌 Support for multiple sensor types (CO, air quality, temperature, etc.)  

---

## 📦 Installation

```bash
pip install firevizz
```

---

## 🚀 Usage

```python
from firevizz import FireVizz

# Initialize the visualizer
visualizer = FireVizz(
    data_path="sensor_data.csv",
    model_path="fire_detection_model.pkl"  # Optional
)

# Create an interactive map
visualizer.create_map("fire_map.html")

# Export fire predictions to CSV
visualizer.export_fire_predictions("fire_locations.csv")
```

---

## 🤖 Sample ML Model

A sample pretrained SVM model can be downloaded from [here](https://github.com/RipunjayS109/firevizz/blob/main/fire_detection_model_local.pkl) tarined on this [dataset](https://github.com/RipunjayS109/firevizz/blob/main/synthetic_fire_sensor_data_with_gps.csv).

## 🧾 Input Data Format

The input CSV file should contain the following columns:
- 📍 `latitude`
- 📍 `longitude`
- 🧪 `co_level`
- 🌫️ `air_quality`
- 🌡️ `temperature`
- 💧 `humidity`
- ⚖️ `pressure`
- 🧴 `voc_level`

---

## 📊 Output

1. **Interactive HTML map** showing:
   - 📍 Sensor locations  
   - 🔥 Fire predictions  
   - 🌡️ Heatmaps for various parameters  
   - 🧭 Layer controls for toggling different visualizations  

2. **CSV file** containing:
   - 🌍 GPS coordinates of predicted fire locations  
   - 📋 Associated sensor readings  

---

## 🖼️ Example

Here’s a preview of the generated interactive fire map:

![FireVizz Output Map](https://raw.githubusercontent.com/RipunjayS109/firevizz/main/Output_Map_exp.png)  
*Example fire prediction and sensor overlay map.*

> ℹ️ Don't forget to open `fire_map.html` in your browser to explore the interactive features!

---

## 📄 License

📝 MIT License  

