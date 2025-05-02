import pandas as pd
import folium
import joblib
from folium.plugins import MarkerCluster, HeatMap, FeatureGroupSubGroup
from sklearn.base import BaseEstimator
from typing import Optional, List, Dict

class FireVizz:
    def __init__(self, data_path: str, model_path: Optional[str] = None):
        print("Initializing FireVizz...")
        print(f"Loading data from {data_path}")
        self.data = pd.read_csv(data_path)
        print("✓ Data loaded successfully")
        
        if model_path:
            print(f"Loading model from {model_path}")
            self.model: Optional[BaseEstimator] = joblib.load(model_path)
            print("✓ Model loaded successfully")
        else:
            print("No model path provided - predictions will not be available")
            self.model = None

        required_columns = {'latitude', 'longitude', 'co_level', 'air_quality', 'temperature', 'humidity', 'pressure', 'voc_level'}
        if not required_columns.issubset(self.data.columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")
        print("✓ Data validation successful")
        
        # Initialize list to store fire predictions
        self.fire_predictions: List[Dict] = []

    def _severity_color(self, value, threshold):
        if value >= threshold * 1.2:
            return 'darkred'
        elif value >= threshold:
            return 'orange'
        else:
            return 'green'

    def create_map(self, map_filename: str = "fire_data_map.html"):
        print("\nCreating interactive fire map...")
        print("Calculating map center coordinates...")
        center_lat = self.data['latitude'].mean()
        center_lon = self.data['longitude'].mean()
        fmap = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='CartoDB positron')
        print("✓ Base map created")

        print("Setting up marker clusters and prediction groups...")
        marker_cluster = MarkerCluster(name='Sensor Markers').add_to(fmap)
        prediction_group = folium.FeatureGroup(name='Fire Predictions').add_to(fmap)
        print("✓ Marker groups initialized")

        print("Creating heatmap layers...")
        heatmap_layers = {}
        for feature in ['co_level', 'air_quality', 'temperature', 'humidity', 'pressure', 'voc_level']:
            print(f"  Processing {feature} heatmap...")
            layer = folium.FeatureGroup(name=f"Heatmap: {feature.title().replace('_', ' ')}")
            heat_data = [[row['latitude'], row['longitude'], row[feature]] for _, row in self.data.iterrows()]
            HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(layer)
            heatmap_layers[feature] = layer
        print("✓ All heatmap layers created")

        print("Adding sensor markers and predictions...")
        total_rows = len(self.data)
        for idx, (_, row) in enumerate(self.data.iterrows(), 1):
            if idx % 10 == 0 or idx == total_rows:
                print(f"  Processing row {idx}/{total_rows}...")
            
            severity_info = f"""
                <b>CO Level:</b> {row['co_level']}<br>
                <b>Air Quality:</b> {row['air_quality']}<br>
                <b>Temperature:</b> {row['temperature']} °C<br>
                <b>Humidity:</b> {row['humidity']} %<br>
                <b>Pressure:</b> {row['pressure']} hPa<br>
                <b>VOC:</b> {row['voc_level']}<br>
            """

            if self.model:
                features = row[['co_level', 'air_quality', 'temperature', 'humidity', 'pressure', 'voc_level']].to_frame().T
                prediction = self.model.predict(features)[0]
                severity_info += f"<b>Prediction:</b> {'🔥 FIRE DETECTED' if prediction == 1 else '✅ SAFE'}<br>"
                if prediction == 1:
                    # Store fire prediction data
                    self.fire_predictions.append({
                        'latitude': row['latitude'],
                        'longitude': row['longitude'],
                        'co_level': row['co_level'],
                        'air_quality': row['air_quality'],
                        'temperature': row['temperature'],
                        'humidity': row['humidity'],
                        'pressure': row['pressure'],
                        'voc_level': row['voc_level']
                    })
                    folium.Marker(
                        location=(row['latitude'], row['longitude']),
                        icon=folium.Icon(color='red', icon='fire', prefix='fa'),
                        popup=folium.Popup(severity_info, max_width=300)
                    ).add_to(prediction_group)

            folium.CircleMarker(
                location=(row['latitude'], row['longitude']),
                radius=6,
                color=self._severity_color(row['co_level'], threshold=1.5),
                fill=True,
                fill_opacity=0.8,
                popup=folium.Popup(severity_info, max_width=300)
            ).add_to(marker_cluster)

        print("Adding heatmap layers to map...")
        for layer in heatmap_layers.values():
            layer.add_to(fmap)
        print("✓ Heatmap layers added")

        print("Adding layer control...")
        folium.LayerControl(collapsed=False).add_to(fmap)
        print("✓ Layer control added")

        print(f"Saving map to {map_filename}...")
        fmap.save(map_filename)
        print(f"✓ Map successfully saved to {map_filename}")

    def export_fire_predictions(self, output_file: str = "fire_predictions.csv") -> None:
        """
        Export the GPS coordinates and sensor data of predicted fire points to a CSV file.
        
        Args:
            output_file (str): Path to save the CSV file. Defaults to "fire_predictions.csv".
        """
        if not self.fire_predictions:
            print("No fire predictions to export.")
            return
            
        print(f"\nExporting fire predictions to {output_file}...")
        predictions_df = pd.DataFrame(self.fire_predictions)
        predictions_df.to_csv(output_file, index=False)
        print(f"✓ Successfully exported {len(self.fire_predictions)} fire predictions to {output_file}") 