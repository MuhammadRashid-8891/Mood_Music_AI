"""
train_model.py - Real AI/ML Training Script
Trains a K-means Clustering model on Spotify audio features to classify moods.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Create model directory
if not os.path.exists('model'):
    os.makedirs('model')

def train_model():
    print("🚀 Starting AI Model Training...")
    
    # 1. Load Data
    input_path = 'dataset/spotify.csv'
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found!")
        return False
        
    df = pd.read_csv(input_path)
    print(f"📊 Loaded {len(df)} songs from dataset")
    
    # 2. Feature Selection & Preprocessing
    features = ['energy', 'valence']
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 3. Train K-means Model
    print("🧠 Training K-means clustering model...")
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    # 4. Map Clusters to Mood Labels
    # We map based on the centroid position relative to the 4 quadrants of valence/energy
    centroids = kmeans.cluster_centers_
    # Inverse transform to get back to original scale (0-1 approx)
    centroids_orig = scaler.inverse_transform(centroids)
    
    cluster_mapping = {}
    
    # Ideal centers for each mood based on Russell's Circumplex Model
    ideal_centers = {
        'Happy': np.array([0.75, 0.75]),     # High Energy, High Valence
        'Energetic': np.array([0.75, 0.25]), # High Energy, Low Valence
        'Sad': np.array([0.25, 0.25]),       # Low Energy, Low Valence
        'Calm': np.array([0.25, 0.75])       # Low Energy, High Valence
    }
    
    used_moods = set()
    
    # For each cluster, find the closest ideal mood
    # Note: A Greedy approach might duplicate, but with k=4 and distinct quadrants, it usually aligns well.
    # A better approach: linear assignment, but let's keep it simple and robust enough.
    
    # Calculate distances matrix
    distances = []
    for i in range(4):
        c = centroids_orig[i]
        # order: energy, valence
        c_point = np.array([c[0], c[1]]) 
        
        row_dists = []
        for mood, ideal in ideal_centers.items():
            dist = np.linalg.norm(c_point - ideal)
            row_dists.append((dist, i, mood))
        distances.extend(row_dists)
    
    # Sort by smallest distance and assign unique moods
    distances.sort(key=lambda x: x[0])
    
    assigned_clusters = set()
    
    for dist, cluster_idx, mood in distances:
        if cluster_idx not in assigned_clusters and mood not in used_moods:
            cluster_mapping[cluster_idx] = mood
            assigned_clusters.add(cluster_idx)
            used_moods.add(mood)
            
    # Fill any gaps (fallback, shouldn't happen with 4x4)
    remaining_clusters = set(range(4)) - assigned_clusters
    remaining_moods = set(ideal_centers.keys()) - used_moods
    for c, m in zip(remaining_clusters, remaining_moods):
        cluster_mapping[c] = m

    print("✅ Cluster Mapping Established:")
    for c, m in cluster_mapping.items():
        print(f"   Cluster {c} -> {m} (Centroid: E={centroids_orig[c][0]:.2f}, V={centroids_orig[c][1]:.2f})")
        
    # Apply mapping
    df['cluster'] = clusters
    df['mood'] = df['cluster'].map(cluster_mapping)
    
    # 5. Save Artifacts
    print("💾 Saving model artifacts...")
    joblib.dump(kmeans, 'model/kmeans_model.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')
    joblib.dump(cluster_mapping, 'model/cluster_mapping.pkl')
    
    df.to_csv('dataset/spotify_with_moods.csv', index=False)
    
    # 6. Generate Visualization
    print("🎨 Generating visualization...")
    plt.figure(figsize=(10, 8))
    
    # Define colors for moods
    mood_colors = {'Happy': '#FFD700', 'Energetic': '#FF4500', 'Sad': '#1E90FF', 'Calm': '#32CD32'}
    colors = [mood_colors[m] for m in df['mood']]
    
    plt.scatter(df['valence'], df['energy'], c=colors, alpha=0.6, s=50)
    
    # Plot centroids
    for i in range(4):
        c = centroids_orig[i]
        plt.scatter(c[1], c[0], s=200, c='black', marker='X', edgecolor='white')
        plt.annotate(cluster_mapping[i], (c[1], c[0]), xytext=(10, 10), 
                     textcoords='offset points', fontsize=12, fontweight='bold',
                     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.8))
                     
    plt.title('Music Mood Clusters (AI Analysis)', fontsize=15)
    plt.xlabel('Valence (Musical Positiveness)', fontsize=12)
    plt.ylabel('Energy (Intensity)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.savefig('model/cluster_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n" + "="*50)
    print("🎉 TRAINING COMPLETE!")
    print("="*50)
    print(f"Files saved:")
    print("- model/kmeans_model.pkl")
    print("- model/scaler.pkl")
    print("- model/cluster_mapping.pkl")
    print("- model/cluster_visualization.png")
    print("- dataset/spotify_with_moods.csv")
    
    return True

if __name__ == "__main__":
    train_model()