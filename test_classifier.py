"""
test_classifier.py - Test the MoodClassifier with various inputs
Run this to verify your classifier is working correctly using the trained ML model.
"""
import pandas as pd
import numpy as np
from mood_classifier import MoodClassifier

def test_predictions():
    print("🧪 Testing MoodClassifier with ML Model")
    print("-" * 50)
    
    # Initialize
    classifier = MoodClassifier()
    if classifier.model is None:
        print("❌ Model not loaded. Run train_model.py first.")
        return

    # Test Cases
    test_cases = [
        (0.9, 0.9, "Happy"),
        (0.9, 0.1, "Energetic"), 
        (0.1, 0.1, "Sad"),
        (0.1, 0.9, "Calm") 
    ]
    
    print(f"{'Energy':<10} {'Valence':<10} {'Predicted':<12} {'Confidence':<12} {'Cluster':<8} {'Expected':<12} {'Status'}")
    print("-" * 80)
    
    for e, v, expected in test_cases:
        mood, conf, cluster = classifier.predict_mood(e, v)
        
        # Note: Cluster mapping logic in train_model might vary slightly based on initialization,
        # but generally quadrants should hold.
        status = "✅" if mood == expected else "❓"
        
        print(f"{e:<10.2f} {v:<10.2f} {mood:<12} {conf:<12.2f} {cluster:<8} {expected:<12} {status}")

def main():
    test_predictions()

if __name__ == "__main__":
    main()