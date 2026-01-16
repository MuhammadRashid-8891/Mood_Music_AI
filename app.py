"""
Streamlit app with ML integration
"""
import streamlit as st
import pandas as pd
from mood_classifier import MoodClassifier
import base64

# Page config
st.set_page_config(
    page_title="AI Music Mood Classifier",
    page_icon="🎵",
    layout="wide"
)

# Initialize classifier
@st.cache_resource
def load_classifier():
    return MoodClassifier()

classifier = load_classifier()

# Title
st.title("🎵 AI-Powered Music Playlist Generator")
st.markdown("""
    ### Mood-Based Recommendation Engine
    Select your current mood, and our AI will curate the perfect playlist for you.
""")

# Sidebar
with st.sidebar:
    st.header("🎛️ Controls")
    
    # Mood selection
    selected_mood = st.radio(
        "Select Your Mood:",
        ["😊 Happy", "😌 Calm", "⚡ Energetic", "😢 Sad", "🎲 Surprise Me"],
        index=0
    )
    
    # Number of songs
    num_songs = st.slider("Number of songs:", 5, 20, 10)
    
    st.divider()
    
    # AI Logic explanation
    st.caption("🤖 **How it works**")
    st.info("""
    **Energy vs Valence Model**
    
    The AI plots songs on a map:
    *   **Happy**: High Energy + High Positivity
    *   **Sad**: Low Energy + Low Positivity
    *   **Energetic**: High Energy + Low Positivity (Aggressive)
    *   **Calm**: Low Energy + High Positivity (Chill)
    """)
    st.caption("Powered by K-Means Clustering")

# Main Content - Playlist Generation
try:
    df = pd.read_csv('dataset/spotify_with_moods.csv')
    
    # Filter by mood
    mood_map = {
        "😊 Happy": "Happy",
        "😌 Calm": "Calm", 
        "⚡ Energetic": "Energetic",
        "😢 Sad": "Sad"
    }
    
    if selected_mood == "🎲 Surprise Me":
        playlist_df = df.sample(n=min(num_songs, len(df)))
    else:
        target_mood = mood_map[selected_mood]
        filtered_df = df[df['mood'] == target_mood]
        
        if filtered_df.empty:
            st.warning(f"No songs found for mood: {target_mood}")
            playlist_df = pd.DataFrame()
        else:
            # Safe sampling
            n_samples = min(num_songs, len(filtered_df))
            playlist_df = filtered_df.sample(n=n_samples)
    
    # Display playlist
    if not playlist_df.empty:
        st.subheader(f"Your {selected_mood} Playlist")
        
        for i, (_, song) in enumerate(playlist_df.iterrows(), 1):
            col1, col2, col3 = st.columns([1, 4, 2])
            
            with col1:
                st.markdown(f"### {i}")
                
            with col2:
                st.markdown(f"**{song.get('track_name', 'Unknown')}**")
                st.markdown(f"*{song.get('artist_name', 'Unknown')}*")
                
                # Progress bars for features
                col_a, col_b = st.columns(2)
                with col_a:
                    st.progress(song.get('energy', 0.5))
                    st.caption(f"Energy: {song.get('energy', 0):.2f}")
                with col_b:
                    st.progress(song.get('valence', 0.5))
                    st.caption(f"Valence: {song.get('valence', 0):.2f}")
                
            with col3:
                st.caption(f"Mood: {song.get('mood', 'Unknown')}")
                
                 # Create search links
                query = f"{song.get('track_name', '')} {song.get('artist_name', '')}"
                youtube_url = f"https://www.youtube.com/results?search_query={query}"
                spotify_url = f"https://open.spotify.com/search/{query}"
                
                st.markdown(f"""
                    <div style="display: flex; gap: 10px;">
                        <a href="{youtube_url}" target="_blank" style="text-decoration: none;">
                            <button style="background-color: #FF0000; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">▶️ YouTube</button>
                        </a>
                        <a href="{spotify_url}" target="_blank" style="text-decoration: none;">
                            <button style="background-color: #1DB954; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">🟢 Spotify</button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
        
        # Download button
        st.markdown("---")
        csv = playlist_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="my_playlist.csv" style="text-decoration:none; color:white; background-color:#4CAF50; padding:10px 20px; border-radius:5px;">📥 Download Playlist as CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
        
    else:
        st.write("No matching songs found.")
        
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please run `python train_model.py` first to train the ML model")