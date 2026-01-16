"""
debug_dist.py - Enhanced debug script with error handling and better visualization
Run this to check mood distribution in your dataset
"""

import pandas as pd
import sys
import os
from mood_classifier import MoodClassifier

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_dataset_exists():
    """Check if dataset file exists"""
    dataset_path = 'dataset/spotify.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: Dataset not found at '{dataset_path}'")
        print("Please make sure:")
        print("1. The 'dataset' folder exists")
        print("2. 'spotify.csv' is inside it")
        print("3. File name is exactly 'spotify.csv'")
        return False
    
    return True

def load_and_analyze():
    """Load dataset and analyze mood distribution"""
    
    if not check_dataset_exists():
        return None
    
    try:
        print_header("DATASET DEBUG & ANALYSIS")
        
        # Initialize classifier
        print("🔍 Loading classifier...")
        classifier = MoodClassifier('dataset/spotify.csv')
        
        # Load data
        print("📊 Loading dataset...")
        classifier.load_data()
        
        # Prepare data (add mood column)
        print("🧠 Classifying moods...")
        classifier.prepare_data()
        
        return classifier
        
    except FileNotFoundError:
        print("❌ File not found. Check the path.")
        return None
    except pd.errors.EmptyDataError:
        print("❌ CSV file is empty.")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__} - {e}")
        return None

def show_mood_distribution(classifier):
    """Display mood distribution with visual bars"""
    print_header("MOOD DISTRIBUTION")
    
    df = classifier.df
    mood_counts = df['Mood'].value_counts()
    total_songs = len(df)
    
    # Mood emojis for better visualization
    mood_emojis = {
        'Happy': '😊',
        'Sad': '😢',
        'Energetic': '⚡',
        'Calm': '😌'
    }
    
    print(f"Total songs in dataset: {total_songs}")
    print("\nMood Counts:")
    print("-"*40)
    
    for mood, count in mood_counts.items():
        emoji = mood_emojis.get(mood, '🎵')
        percentage = (count / total_songs) * 100
        
        # Create visual bar (each █ = 2%)
        bar_length = int(percentage / 2)
        bar = '█' * bar_length
        
        print(f"{emoji} {mood:12}: {count:4} songs ({percentage:5.1f}%) {bar}")
    
    # Check balance
    print("\n📈 Balance Check:")
    max_count = mood_counts.max()
    min_count = mood_counts.min()
    imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
    
    if imbalance_ratio < 2:
        print("✅ Dataset is well-balanced")
    elif imbalance_ratio < 5:
        print("⚠️  Dataset has moderate imbalance")
    else:
        print("❌ Dataset is highly imbalanced - consider adding more data")

def show_sample_data(classifier, num_samples=20):
    """Display sample data with formatting"""
    print_header(f"SAMPLE DATA (First {num_samples} Songs)")
    
    df = classifier.df
    sample_df = df[['track_name', 'energy', 'valence', 'Mood']].head(num_samples)
    
    # Format for better readability
    print(f"{'#':<3} {'Track Name':<35} {'Energy':<8} {'Valence':<9} {'Mood':<12}")
    print("-"*70)
    
    for idx, row in sample_df.iterrows():
        # Truncate long track names
        track_name = str(row['track_name'])
        if len(track_name) > 32:
            track_name = track_name[:29] + "..."
        
        # Add emoji based on mood
        mood_emoji = {
            'Happy': '😊',
            'Sad': '😢',
            'Energetic': '⚡',
            'Calm': '😌'
        }.get(row['Mood'], '🎵')
        
        print(f"{idx+1:<3} {track_name:<35} "
              f"{row['energy']:<8.2f} "
              f"{row['valence']:<9.2f} "
              f"{mood_emoji} {row['Mood']}")

def show_feature_statistics(classifier):
    """Show statistics about energy and valence features"""
    print_header("FEATURE STATISTICS")
    
    df = classifier.df
    
    print("📊 Energy Statistics:")
    print(f"  Min: {df['energy'].min():.3f}")
    print(f"  Max: {df['energy'].max():.3f}")
    print(f"  Mean: {df['energy'].mean():.3f}")
    print(f"  Std Dev: {df['energy'].std():.3f}")
    
    print("\n📊 Valence Statistics:")
    print(f"  Min: {df['valence'].min():.3f}")
    print(f"  Max: {df['valence'].max():.3f}")
    print(f"  Mean: {df['valence'].mean():.3f}")
    print(f"  Std Dev: {df['valence'].std():.3f}")
    
    # Check if values are in expected range (0-1)
    print("\n✅ Range Check:")
    if df['energy'].min() >= 0 and df['energy'].max() <= 1:
        print("  Energy: Within expected range (0-1)")
    else:
        print(f"  ⚠️  Energy: Outside 0-1 range ({df['energy'].min():.2f} to {df['energy'].max():.2f})")
    
    if df['valence'].min() >= 0 and df['valence'].max() <= 1:
        print("  Valence: Within expected range (0-1)")
    else:
        print(f"  ⚠️  Valence: Outside 0-1 range ({df['valence'].min():.2f} to {df['valence'].max():.2f})")

def test_classification_rules(classifier):
    """Test the classification rules with edge cases"""
    print_header("CLASSIFICATION RULE TEST")
    
    test_cases = [
        ("Very Happy", 0.9, 0.9, "Should be Happy"),
        ("Very Sad", 0.1, 0.1, "Should be Sad"),
        ("Energetic Rock", 0.9, 0.3, "Should be Energetic"),
        ("Calm Meditation", 0.2, 0.8, "Should be Calm"),
        ("Boundary Case 1", 0.5, 0.5, "Boundary - check your rule"),
        ("Boundary Case 2", 0.5, 0.49, "Boundary - check your rule"),
    ]
    
    print("Testing classification rules:")
    print("-"*60)
    print(f"{'Description':<20} {'Energy':<8} {'Valence':<9} {'Predicted':<12} {'Note':<20}")
    print("-"*60)
    
    for desc, energy, valence, note in test_cases:
        mood = classifier.classify_mood(energy, valence)
        print(f"{desc:<20} {energy:<8.2f} {valence:<9.2f} {mood:<12} {note:<20}")

def check_for_issues(classifier):
    """Check for potential issues in the dataset"""
    print_header("POTENTIAL ISSUES CHECK")
    
    df = classifier.df
    issues_found = 0
    
    # 1. Check for missing values
    missing_values = df[['track_name', 'energy', 'valence']].isnull().sum()
    for col, count in missing_values.items():
        if count > 0:
            print(f"❌ Missing values in '{col}': {count}")
            issues_found += 1
    
    # 2. Check for duplicate track names
    duplicates = df['track_name'].duplicated().sum()
    if duplicates > 0:
        print(f"⚠️  Duplicate track names: {duplicates}")
        issues_found += 1
    
    # 3. Check for songs with exactly same features
    feature_duplicates = df.duplicated(subset=['energy', 'valence']).sum()
    if feature_duplicates > 0:
        print(f"⚠️  Songs with identical energy/valence: {feature_duplicates}")
        issues_found += 1
    
    # 4. Check classification consistency
    print("\n🔍 Checking classification consistency...")
    
    # Get songs that might be misclassified based on extreme values
    misclassified_candidates = []
    
    for idx, row in df.iterrows():
        energy, valence, mood = row['energy'], row['valence'], row['Mood']
        
        # Check if classification matches extreme values
        if energy > 0.8 and valence > 0.8 and mood != 'Happy':
            misclassified_candidates.append((idx, 'Should be Happy', mood))
        elif energy < 0.2 and valence < 0.2 and mood != 'Sad':
            misclassified_candidates.append((idx, 'Should be Sad', mood))
    
    if misclassified_candidates:
        print(f"⚠️  Possible misclassifications: {len(misclassified_candidates)}")
        for idx, expected, actual in misclassified_candidates[:5]:  # Show first 5
            track_name = df.loc[idx, 'track_name'][:30] + "..." if len(df.loc[idx, 'track_name']) > 30 else df.loc[idx, 'track_name']
            print(f"    '{track_name}' - {expected}, but classified as {actual}")
        issues_found += 1
    
    if issues_found == 0:
        print("✅ No major issues found!")
    else:
        print(f"\nTotal issues found: {issues_found}")

def main():
    """Main function"""
    print("\n" + "="*60)
    print("         🎵 MOOD CLASSIFIER DEBUG TOOL 🎵")
    print("="*60)
    
    # Load and analyze
    classifier = load_and_analyze()
    
    if classifier is None:
        print("\n❌ Cannot continue. Fix the errors above.")
        sys.exit(1)
    
    # Show all analyses
    show_mood_distribution(classifier)
    show_sample_data(classifier)
    show_feature_statistics(classifier)
    test_classification_rules(classifier)
    check_for_issues(classifier)
    
    print_header("DEBUG COMPLETE")
    print("\n✅ Debug analysis finished!")
    print("\nNext steps:")
    print("1. Run 'python run.py' for interactive menu")
    print("2. Run 'streamlit run app.py' for web app")
    print("3. Run 'python test_classifier.py' for comprehensive testing")

if __name__ == "__main__":
    main()