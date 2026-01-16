"""
mood_classifier.py - ML Classifier Class
Handles loading the trained model and making predictions.
"""
import joblib
import pandas as pd
import numpy as np
import os

class MoodClassifier:
    def __init__(self):
        """Load trained ML model and artifacts"""
        self.model = None
        self.scaler = None
        self.cluster_mapping = None
        
        try:
            if os.path.exists('model/kmeans_model.pkl'):
                self.model = joblib.load('model/kmeans_model.pkl')
                self.scaler = joblib.load('model/scaler.pkl')
                
                # Load mapping if exists, else use default (fallback)
                if os.path.exists('model/cluster_mapping.pkl'):
                    self.cluster_mapping = joblib.load('model/cluster_mapping.pkl')
                else:
                    self.cluster_mapping = {0: 'Energetic', 1: 'Happy', 2: 'Calm', 3: 'Sad'}
                    
                print("✅ ML Model loaded successfully")
            else:
                print("⚠️ Model files not found. Please run train_model.py")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None

    def predict_mood(self, energy, valence):
        """
        Predict mood using the ML model.
        Returns: mood (str), confidence (float), cluster (int)
        """
        if self.model is None:
            # Fallback to rule-based if model fails
            return self._fallback_rule_based(energy, valence)
            
        try:
            # Prepare input
            features = np.array([[energy, valence]])
            features_scaled = self.scaler.transform(features)
            
            # Predict cluster
            cluster = int(self.model.predict(features_scaled)[0])
            
            # Get Mood
            mood = self.cluster_mapping.get(cluster, "Unknown")
            
            # Calculate Confidence based on distance to center
            # transform returns distance to all centroids
            distances = self.model.transform(features_scaled)
            dist_to_center = distances[0][cluster]
            
            # Heuristic for confidence: exp(-distance)
            # Closer to centroid = higher confidence
            confidence = np.exp(-dist_to_center) # This usually gives 0.5-1.0 range well
            
            return mood, confidence, cluster
            
        except Exception as e:
            print(f"Prediction Error: {e}")
            return self._fallback_rule_based(energy, valence)

    def _fallback_rule_based(self, energy, valence):
        """Simple fallback logic if ML model is missing"""
        confidence = 0.85 # Mock confidence
        cluster = -1
        
        if energy > 0.5 and valence > 0.5:
            return "Happy", confidence, cluster
        elif energy > 0.5 and valence <= 0.5:
            return "Energetic", confidence, cluster
        elif energy <= 0.5 and valence > 0.5:
            return "Calm", confidence, cluster
        else:
            return "Sad", confidence, cluster

    def get_mood_stats(self, df):
        """Get mood distribution stats from a dataframe"""
        if 'mood' in df.columns:
            return df['mood'].value_counts().to_dict()
        return {}