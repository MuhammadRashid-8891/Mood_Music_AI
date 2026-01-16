"""
run.py - Main entry point for the Mood Music AI project
One script to rule them all: trains model, runs web app, or shows analysis
"""
import sys
import os
import subprocess
from mood_classifier import MoodClassifier

def show_banner():
    """Display fancy banner"""
    print("="*60)
    print("       🎵 MOOD-BASED MUSIC AI GENERATOR (ML Edition) 🎵")
    print("="*60)
    print()

def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")
    required = ['pandas', 'streamlit', 'sklearn', 'joblib', 'matplotlib', 'seaborn', 'plotly']
    missing = []
    
    for package in required:
        pkg_name = 'scikit-learn' if package == 'sklearn' else package
        try:
            # Handle import names vs package names
            import_name = package
            if package == 'scikit-learn': import_name = 'sklearn'
            
            __import__(import_name)
            print(f"   ✅ {pkg_name}")
        except ImportError:
            # Try finding spec
            try:
                import importlib.util
                if importlib.util.find_spec(import_name) is None:
                    raise ImportError
                print(f"   ✅ {pkg_name}")
            except ImportError:
                print(f"   ❌ {pkg_name} (missing)")
                missing.append(pkg_name)
    
    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        install = input("Do you want to install them? (y/n): ")
        if install.lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
            print("✅ Dependencies installed!")
        else:
            print(f"Please install manually: pip install {' '.join(missing)}")
            return False
    
    return True

def run_web_app():
    """Launch the Streamlit web application"""
    print("\n" + "="*60)
    print("🌐 LAUNCHING WEB APPLICATION")
    print("="*60)
    print("\nStarting Streamlit server...")
    print("➡️ The app will open in your browser at: http://localhost:8501")
    print("➡️ Press Ctrl+C in this terminal to stop the server")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting web app: {e}")

def train_ml_model():
    """Train the K-Means ML model"""
    print("\n" + "="*60)
    print("🤖 TRAINING ML MODEL")
    print("="*60)
    
    try:
        # Import dynamically to avoid top-level errors if dependencies are missing during check
        from train_model import train_model
        train_model()
    except ImportError:
        print("❌ Could not import train_model. Make sure dependencies are installed.")
    except Exception as e:
        print(f"❌ Error during training: {e}")

def show_menu():
    """Display interactive menu"""
    print("\n" + "="*60)
    print("📱 MAIN MENU")
    print("="*60)
    print("1️⃣  Launch Web App (Streamlit)")
    print("2️⃣  Retrain AI Model")
    print("3️⃣  Verify Model Predictions")
    print("4️⃣  Exit")
    print("\n" + "="*60)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        run_web_app()
    elif choice == '2':
        train_ml_model()
        input("\nPress Enter to return to menu...")
        show_menu()
    elif choice == '3':
        subprocess.run([sys.executable, "test_classifier.py"])
        input("\nPress Enter to return to menu...")
        show_menu()
    elif choice == '4':
        print("\n👋 Goodbye!")
        sys.exit(0)
    else:
        print("❌ Invalid choice.")
        show_menu()

def main():
    show_banner()
    if not check_dependencies():
        sys.exit(1)
    
    # Check if model exists, if not, offer to train
    if not os.path.exists('model/kmeans_model.pkl'):
        print("\n⚠️ AI Model not found!")
        print("Training model now for the first time...")
        train_ml_model()
        
    show_menu()

if __name__ == "__main__":
    main()