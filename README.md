# 🎵 MOOD-BASED AI MUSIC PLAYLIST GENERATOR

**An intelligent music recommendation system powered by Unsupervised Machine Learning.**

---

## 📋 Table of Contents
1.  [Project Overview](#project-overview)
2.  [Key Features](#key-features)
3.  [The Science Behind It (AI/ML)](#the-science-behind-it)
4.  [Technology Stack](#technology-stack)
5.  [Installation & Setup](#installation--setup)
6.  [How to Use](#how-to-use)
7.  [Project Structure](#project-structure)
8.  [Troubleshooting](#troubleshooting)

---

## 1. Project Overview
This project is an **AI-powered web application** capable of generating music playlists based on the user's current emotional state. Unlike traditional playlists that rely on manual curation, this system uses **Machine Learning algorithms** to analyze the audio properties of songs (such as tempo, energy, and acousticness) to mathematically determine their emotional mood.

The system was built to demonstrate the practical application of **K-Means Clustering** in the domain of Music Information Retrieval (MIR).

---

## 2. Key Features
*   **🧠 Intelligent Mood Classification**: Automatically categorizes songs into **Happy**, **Sad**, **Energetic**, or **Calm** without human intervention.
*   **🎹 Audio Feature Analysis**: Analyzes songs based on deep audio metrics like *Danceability*, *Energy*, and *Valence*.
*   **🎧 Smart Playback Integration**: Provides instant **YouTube** and **Spotify** listening links for every recommended song.
*   **💻 Interactive Web Interface**: A sleek, user-friendly dashboard built with **Streamlit** for real-time interaction.
*   **📊 Dynamic Playlist Generation**: Generates unique, randomized playlists every time, ensuring a fresh listening experience.

---

## 3. The Science Behind It (The "AI" Part)
This project is not just a set of `if-else` rules. It uses a **Machine Learning** approach known as **k-Means Clustering** (Unsupervised Learning).

### The Dataset
We utilize a dataset of Spotify tracks that includes specific audio feature metrics:
*   **Energy (0.0 - 1.0)**: A measure of intensity and activity. Fast, loud, and noisy tracks have high energy.
*   **Valence (0.0 - 1.0)**: A measure of "musical positiveness". High valence sounds happy/cheerful; low valence sounds sad/depressed.

### The Algorithm: K-Means Clustering
1.  **Feature Mapping**: Every song is plotted as a point on a 2D graph (Energy vs. Valence).
2.  **Clustering**: The K-Means algorithm identifies **4 distinct groups (clusters)** of songs that are close to each other in this 2D space.
3.  **Labeling**: We map these math clusters to human emotions using **Russell's Circumplex Model**:

| Cluster | Energy | Valence | Emotion |
| :--- | :--- | :--- | :--- |
| **Cluster A** | High ⬆️ | High ⬆️ | ** 😊 Happy** |
| **Cluster B** | High ⬆️ | Low ⬇️ | ** ⚡ Energetic / Aggressive** |
| **Cluster C** | Low ⬇️ | High ⬆️ | ** 😌 Calm / Chill** |
| **Cluster D** | Low ⬇️ | Low ⬇️ | ** 😢 Sad / Melancholic** |

*This means the AI "learns" what a sad song sounds like by looking at the data, rather than being explicitly told.*

---

## 4. Technology Stack
*   **Language**: Python 3.9+
*   **Frontend**: Streamlit (Web Framework)
*   **Machine Learning**: Scikit-Learn (KMeans, StandardScaler)
*   **Data Processing**: Pandas, NumPy
*   **Visualization**: Matplotlib, Seaborn
*   **Model Persistence**: Joblib (Saving/Loading the trained model)

---

## 5. Installation & Setup

### Prerequisites
*   Python installed on your system.
*   An internet connection (for library installation).

### Step-by-Step Guide

1.  **Unzip/Navigation**:
    Open your terminal or command prompt and navigate to the project folder:
    ```bash
    cd path/to/Mood_Music_AI
    ```

2.  **Install Dependencies**:
    We need to install the required Python libraries listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Train the Model**:
    Before running the app, we must train the AI on our dataset. Run:
    ```bash
    python run.py
    ```
    *Select Option 2: "Retrain AI Model"*

---

## 6. How to Use

1.  **Start the Application**:
    Run the unified launcher script:
    ```bash
    python run.py
    ```
    *Select Option 1: "Launch Web App"*

2.  **Interact**:
    *   The app will open in your default browser at `http://localhost:8501`.
    *   Use the **Sidebar** to select your desired mood (e.g., "Hit me with some Happy tunes").
    *   Adjust the slider to choose how many songs you want.

3.  **Listen**:
    *   The playlist will appear in the main window.
    *   Click the **▶️ YouTube** button to watch the video.
    *   Click the **🟢 Spotify** button to open the track in Spotify.
    *   Click "Download CSV" to save the playlist to your computer.

---

## 7. Project Structure

| File/Folder | Description |
| :--- | :--- |
| `run.py` | **Main Entry Point**. Handles setup, training, and launching the app. |
| `app.py` | **The Frontend**. Contains the Streamlit user interface code. |
| `train_model.py` | **The Training Script**. Loads data, trains K-Means, and saves the model. |
| `mood_classifier.py` | **The AI Logic**. A class that loads the saved model and makes predictions. |
| `dataset/` | Contains `spotify.csv` (raw data) and `spotify_with_moods.csv` (processed). |
| `model/` | Stores the trained AI artifacts (`.pkl` binary files). |
| `requirements.txt` | List of all Python libraries used in the project. |

---

## 8. Troubleshooting

*   **"Model not found" Error**:
    *   You forgot to train the model! Run `python run.py` and choose the *Retrain* option.
*   **"Unknown" songs in playlist**:
    *   Ensure your `dataset/spotify.csv` has the columns `track_name` and `artist_name`.
*   **App not opening**:
    *   Check your terminal for errors. Ensure you are in the correct directory.

---
**Created for AI Course Certificate Submission**
