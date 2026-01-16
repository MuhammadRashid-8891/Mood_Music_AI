import sys
import os
from mood_classifier import MoodClassifier

def verify():
    print("🔍 Verifying MoodClassifier...")
    
    # 1. Initialize
    try:
        classifier = MoodClassifier()
    except Exception as e:
        print(f"❌ Failed to initialize MoodClassifier: {e}")
        return False
        
    if classifier.model is None:
        print("❌ Model failed to load (classifier.model is None)")
        return False
        
    print("✅ Model loaded successfully")
    
    # 2. Test Prediction
    # Test Happy case (High Energy, High Valence)
    print("\n🧪 Testing Happy Prediction (E=0.8, V=0.8)...")
    mood, conf, cluster = classifier.predict_mood(0.8, 0.8)
    print(f"   Result: Mood={mood}, Conf={conf:.4f}, Cluster={cluster}")
    
    if mood == 'Happy':
         print("   ✅ Happy prediction correct")
    else:
         print(f"   ⚠️ Unexpected mood: {mood} (Check cluster mapping)")

    # Test Sad case (Low Energy, Low Valence)
    print("\n🧪 Testing Sad Prediction (E=0.2, V=0.2)...")
    mood, conf, cluster = classifier.predict_mood(0.2, 0.2)
    print(f"   Result: Mood={mood}, Conf={conf:.4f}, Cluster={cluster}")

    if mood == 'Sad':
         print("   ✅ Sad prediction correct")
    else:
         print(f"   ⚠️ Unexpected mood: {mood}")

    print("\n✨ Verification Complete!")
    return True

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
