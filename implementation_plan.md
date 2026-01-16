# Music Playback Implementation Plan

## Goal
Enable users to "hear" the music recommended by the AI.

## Limitation
The current `dataset/spotify.csv` only contains metadata (Track Name, Artist, Energy, Valence), but no actual audio files or streaming URLs.

## Solution
We will add dynamic **"Listen" buttons** to the `app.py` interface. These buttons will open a search query on YouTube or Spotify for the specific song.

## Proposed Changes

### `app.py`
- In the `Playlist` tab loop:
    - Construct a search query string: `{song_name} {artist_name}`.
    - Create a YouTube Search URL: `https://www.youtube.com/results?search_query=...`
    - Create a Spotify Web Player Search URL: `https://open.spotify.com/search/...`
    - specific Spotify URL: `https://open.spotify.com/search/{encoded_query}`
    - Add UI columns to display these links as buttons/icons next to each song.

## Verification
- Run the app.
- Click "Listen on YouTube".
- Verify it opens the correct search results page.
