import streamlit as st
import requests
from urllib.parse import quote
import warnings
import json
import os
from dotenv import load_dotenv
warnings.filterwarnings('ignore')

# Load environment variables from .env file
load_dotenv()

try:
    import speech_recognition as sr
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Decibel - Lyrics Finder",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with modern design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Hero Header */
    .hero-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.1) 0%, rgba(30, 215, 96, 0.05) 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #b3b3b3;
        font-weight: 300;
        margin-top: 0;
    }
    
    .hero-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    /* Lyrics Display */
    .lyrics-box {
        background: linear-gradient(135deg, rgba(18, 18, 18, 0.95) 0%, rgba(28, 28, 28, 0.9) 100%);
        padding: 3rem;
        border-radius: 20px;
        border: 2px solid rgba(29, 185, 84, 0.3);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
        white-space: pre-wrap;
        font-family: 'Courier New', monospace;
        max-height: 600px;
        overflow-y: auto;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.8;
        backdrop-filter: blur(10px);
    }
    
    .lyrics-box::-webkit-scrollbar {
        width: 8px;
    }
    
    .lyrics-box::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    .lyrics-box::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        border-radius: 10px;
    }
    
    /* Message Boxes */
    .success-message {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.2) 0%, rgba(30, 215, 96, 0.1) 100%);
        border-left: 5px solid #1DB954;
        border-radius: 15px;
        color: #1ed760;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .error-message {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(220, 53, 69, 0.2) 0%, rgba(255, 107, 107, 0.1) 100%);
        border-left: 5px solid #dc3545;
        border-radius: 15px;
        color: #ff6b6b;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .info-message {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(23, 162, 184, 0.2) 0%, rgba(93, 173, 226, 0.1) 100%);
        border-left: 5px solid #17a2b8;
        border-radius: 15px;
        color: #5dade2;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Song Cards */
    .song-card {
        background: linear-gradient(135deg, rgba(29, 185, 84, 0.15) 0%, rgba(30, 215, 96, 0.08) 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid rgba(29, 185, 84, 0.4);
        margin: 0.8rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .song-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(29, 185, 84, 0.3);
        border-color: #1DB954;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(18, 18, 18, 0.6);
        border-radius: 15px;
        padding: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background: transparent;
        border-radius: 10px;
        color: #b3b3b3;
        font-weight: 500;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(29, 185, 84, 0.1);
        color: #1ed760;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(29, 185, 84, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(29, 185, 84, 0.5);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(18, 18, 18, 0.8);
        border: 2px solid rgba(29, 185, 84, 0.3);
        border-radius: 12px;
        color: #e0e0e0;
        font-size: 1rem;
        padding: 0.75rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #1DB954;
        box-shadow: 0 0 20px rgba(29, 185, 84, 0.3);
    }
    
    /* Section Headers */
    h3 {
        color: #1ed760;
        font-weight: 600;
        margin-bottom: 1.5rem;
        font-size: 1.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 0.85em;
        font-weight: 600;
        margin-left: 8px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(18, 18, 18, 0.6);
        border-radius: 10px;
        color: #b3b3b3;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        color: #1ed760;
    }
    </style>
""", unsafe_allow_html=True)

def fetch_lyrics(artist, song):
    """Fetch lyrics from multiple APIs"""
    # Try API 1: lyrics-api.fly.dev
    try:
        url = f'https://lyrics-api.fly.dev/api/lyrics/{quote(artist)}/{quote(song)}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'lyrics' in data and data['lyrics']:
                return {
                    'title': data.get('title', song),
                    'artist': data.get('artist', artist),
                    'lyrics': data['lyrics'],
                    'source': 'lyrics-api.fly.dev'
                }
    except:
        pass
    
    # Try API 2: lrclib.net
    try:
        url = 'https://lrclib.net/api/get'
        params = {'artist_name': artist, 'track_name': song}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            lyrics = data.get('plainLyrics', '')
            if lyrics:
                return {
                    'title': data.get('trackName', song),
                    'artist': data.get('artistName', artist),
                    'lyrics': lyrics,
                    'source': 'lrclib.net'
                }
    except:
        pass
    
    return None

def identify_song_with_gemini(lyrics_text, api_key):
    """Use Gemini to identify song from lyrics with improved prompting"""
    if not GEMINI_AVAILABLE or not api_key:
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Enhanced prompt with better instructions
        prompt = f"""You are an expert music librarian with extensive knowledge of songs across all genres, languages, and eras.

A user has provided these lyrics or sung words:
"{lyrics_text}"

TASK: Identify the most likely songs that contain these lyrics.

ANALYSIS INSTRUCTIONS:
1. Consider exact phrase matches first
2. Look for distinctive phrases or memorable lines
3. Consider phonetic similarities (the user might have misheard)
4. Consider translations or alternate versions
5. Include songs from all languages and regions
6. Consider both popular hits and lesser-known tracks

CONFIDENCE SCORING:
- 90-100: Exact or near-exact lyric match
- 70-89: Strong match with minor variations
- 50-69: Partial match or similar phrasing
- 30-49: Possible match based on keywords
- Below 30: Low confidence match

OUTPUT FORMAT (JSON ONLY):
[
  {{
    "title": "Exact Song Title",
    "artist": "Artist Name (or Multiple Artists if applicable)",
    "album": "Album Name",
    "year": "Release Year",
    "language": "Language",
    "confidence": 95,
    "matching_phrase": "the specific phrase that matched",
    "genre": "Genre"
  }}
]

REQUIREMENTS:
- Return TOP 8 matches, ordered by confidence (highest first)
- Only include songs with confidence >= 30
- If no matches found, return empty array: []
- Provide accurate metadata (double-check artist spelling)
- RESPOND WITH ONLY THE JSON ARRAY - NO OTHER TEXT

Begin analysis:"""

        # Configure generation parameters for better results
        generation_config = {
            'temperature': 0.3,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        result_text = response.text.strip()
        
        # Clean up response - remove markdown code blocks if present
        if result_text.startswith('```'):
            lines = result_text.split('\n')
            result_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else result_text
            result_text = result_text.replace('```json', '').replace('```', '').strip()
        
        # Extract JSON from response
        if result_text.startswith('['):
            songs = json.loads(result_text)
            
            # Filter out low confidence results
            filtered_songs = [s for s in songs if s.get('confidence', 0) >= 30]
            
            # Sort by confidence
            filtered_songs.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            
            return filtered_songs[:8] if filtered_songs else None
        
        return None
        
    except json.JSONDecodeError as e:
        st.warning(f"⚠️ Gemini returned invalid format. Trying fallback search...")
        return None
    except Exception as e:
        st.error(f"Gemini API error: {str(e)}")
        return None

def search_by_lyrics_text(lyrics_text, api_key):
    """Search for songs using lyrics text - enhanced version with better preprocessing"""
    songs_found = []
    
    # Preprocess the input
    cleaned_lyrics = lyrics_text.strip()
    
    # Remove common filler words for better matching
    filler_words = ['like', 'um', 'uh', 'you know', 'i mean', 'basically']
    for filler in filler_words:
        cleaned_lyrics = cleaned_lyrics.replace(filler, ' ')
    
    # Normalize spaces
    cleaned_lyrics = ' '.join(cleaned_lyrics.split())
    
    # Priority 1: Use Gemini AI if available
    if GEMINI_AVAILABLE and api_key:
        with st.spinner("🤖 Using Gemini AI to identify the song..."):
            gemini_results = identify_song_with_gemini(cleaned_lyrics, api_key)
        
        if gemini_results:
            for song in gemini_results:
                songs_found.append({
                    'title': song.get('title', 'Unknown'),
                    'artist': song.get('artist', 'Unknown'),
                    'album': song.get('album', ''),
                    'year': song.get('year', ''),
                    'language': song.get('language', ''),
                    'confidence': song.get('confidence', 0),
                    'matching_phrase': song.get('matching_phrase', ''),
                    'genre': song.get('genre', ''),
                    'source': 'gemini_ai'
                })
            
            if songs_found:
                return songs_found
    
    # Fallback: Try lrclib.net search with cleaned input
    try:
        url = 'https://lrclib.net/api/search'
        params = {'q': cleaned_lyrics[:100]}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                for item in data[:8]:
                    songs_found.append({
                        'title': item.get('trackName', item.get('name', 'Unknown')),
                        'artist': item.get('artistName', item.get('artist', 'Unknown')),
                        'album': item.get('albumName', ''),
                        'source': 'lrclib'
                    })
                if songs_found:
                    return songs_found
    except Exception as e:
        pass
    
    # Try search by partial match with better keyword extraction
    try:
        # Extract meaningful words (longer than 3 characters)
        words = cleaned_lyrics.strip().split()
        meaningful_words = [w for w in words if len(w) > 3][:5]
        
        if not meaningful_words:
            meaningful_words = words[:5]
        
        search_query = ' '.join(meaningful_words)
        
        url = f'https://lrclib.net/api/search'
        params = {'q': search_query}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list):
                for item in data[:8]:
                    songs_found.append({
                        'title': item.get('trackName', 'Unknown'),
                        'artist': item.get('artistName', 'Unknown'),
                        'album': item.get('albumName', ''),
                        'source': 'lrclib'
                    })
    except Exception as e:
        pass
    
    return songs_found

def record_audio():
    """Record audio from microphone"""
    if not VOICE_AVAILABLE:
        return None, "SpeechRecognition library not installed"
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            st.info("🎤 Adjusting for background noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            st.warning("🎤 **LISTENING NOW! Speak or sing the lyrics...**")
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
            
            st.info("🔄 Processing audio...")
            text = recognizer.recognize_google(audio)
            return text, None
            
    except sr.WaitTimeoutError:
        return None, "No audio detected. Please try again."
    except sr.UnknownValueError:
        return None, "Could not understand audio. Please speak more clearly."
    except sr.RequestError as e:
        return None, f"Google Speech API error: {e}"
    except Exception as e:
        return None, f"Microphone error: {e}"

# Initialize session state
if 'current_lyrics' not in st.session_state:
    st.session_state.current_lyrics = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'recognized_text' not in st.session_state:
    st.session_state.recognized_text = ""
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = os.getenv('GEMINI_API_KEY', '')

# Configure Gemini if available
if st.session_state.gemini_api_key and GEMINI_AVAILABLE:
    try:
        genai.configure(api_key=st.session_state.gemini_api_key)
    except Exception as e:
        st.error(f"❌ Failed to configure Gemini API: {str(e)}")

# Hero Header
st.markdown("""
    <div class="hero-header">
        <div class="hero-icon">🎧</div>
        <h1 class="hero-title">DECIBEL</h1>
        <p class="hero-subtitle">Your AI-Powered Lyrics Discovery Platform</p>
    </div>
""", unsafe_allow_html=True)

# Show warning if no API key
if not st.session_state.gemini_api_key and GEMINI_AVAILABLE:
    st.warning("⚠️ No Gemini API key found. AI-powered search will be disabled. Add GEMINI_API_KEY to your .env file for the best experience.")
elif not GEMINI_AVAILABLE:
    st.info("ℹ️ Install google-generativeai for AI-powered search: `pip install google-generativeai`")

# Create centered layout with columns
col_left, col_center, col_right = st.columns([1, 6, 1])

with col_center:
    # Create tabs
    tab1, tab2 = st.tabs(["🔍 Search by Name", "🎤 Search by Lyrics"])

    # TAB 1: Traditional Search
    with tab1:
        st.markdown("### Enter artist and song name")
        
        col1, col2 = st.columns(2)
        with col1:
            artist_input = st.text_input("🎤 Artist Name", placeholder="e.g., Arijit Singh, Taylor Swift")
        with col2:
            song_input = st.text_input("🎵 Song Title", placeholder="e.g., Tum Hi Ho, Blank Space")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔍 Find Lyrics", type="primary", use_container_width=True):
            if artist_input and song_input:
                with st.spinner(f"🎵 Searching for **{song_input}** by **{artist_input}**..."):
                    result = fetch_lyrics(artist_input, song_input)
                
                if result:
                    st.session_state.current_lyrics = result
                    st.session_state.search_results = []
                    st.rerun()
                else:
                    st.error("❌ Lyrics not found. Please check the spelling and try again.")
            else:
                st.warning("⚠️ Please enter both artist and song name")

    # TAB 2: Lyrics Search
    with tab2:
        st.markdown("### Search by typing or speaking lyrics")
        
        # Text input method
        st.markdown("**Method 1: Type the lyrics you remember**")
        lyrics_input = st.text_area(
            "💭 Enter any lyrics you remember:",
            placeholder="e.g., 'all of me loves all of you' or 'tum hi ho bandhu'",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Search by Text", use_container_width=True, type="primary"):
                if lyrics_input.strip():
                    results = search_by_lyrics_text(lyrics_input.strip(), st.session_state.gemini_api_key)
                    
                    if results:
                        st.session_state.search_results = results
                        st.session_state.current_lyrics = None
                        st.success(f"✅ Found {len(results)} matching songs!")
                        st.rerun()
                    else:
                        st.error("❌ No songs found. Try different lyrics or phrases.")
                else:
                    st.warning("⚠️ Please enter some lyrics first")
        
        with col2:
            # Voice input method
            if not VOICE_AVAILABLE:
                st.button("🎤 Voice Search (Not Available)", disabled=True, use_container_width=True)
                st.caption("Install: `pip install SpeechRecognition pyaudio`")
            else:
                voice_btn = st.button("🎤 Voice Search", use_container_width=True, type="secondary")
        
        if VOICE_AVAILABLE and voice_btn:
            st.markdown("---")
            st.info("🎤 **Get ready! Recording starts in 3 seconds...**")
            
            import time
            progress_bar = st.progress(0)
            for i in range(3):
                time.sleep(1)
                progress_bar.progress((i + 1) / 3)
            progress_bar.empty()
            
            st.warning("🔴 **RECORDING NOW! Speak or sing the lyrics...**")
            
            text, error = record_audio()
            
            if text:
                st.session_state.recognized_text = text
                st.success(f"✅ Recognized: **'{text}'**")
                
                results = search_by_lyrics_text(text, st.session_state.gemini_api_key)
                
                if results:
                    st.session_state.search_results = results
                    st.session_state.current_lyrics = None
                    st.rerun()
                else:
                    st.warning(f"⚠️ No exact matches found for '{text}'")
                    st.info(f"""
                    💡 **Suggestions:**
                    - Try searching on Google: `{text} lyrics`
                    - Use the "Search by Name" tab once you find the song
                    - Try typing different keywords in the text box above
                    """)
            else:
                st.error(f"❌ {error}")

    # Display search results with enhanced metadata
    if st.session_state.search_results:
        st.markdown("---")
        st.markdown("## 🎯 Matching Songs")
        
        for idx, song in enumerate(st.session_state.search_results):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Confidence badge
                confidence_badge = ""
                if song.get('confidence'):
                    conf = song['confidence']
                    if conf >= 80:
                        color = "#1ed760"
                        emoji = "🎯"
                    elif conf >= 60:
                        color = "#ffd54f"
                        emoji = "👍"
                    else:
                        color = "#ff6b6b"
                        emoji = "❓"
                    confidence_badge = f"<span class='badge' style='background-color: {color};'>{emoji} {conf}%</span>"
                
                # Source badge
                source_badge = ""
                if song.get('source') == 'gemini_ai':
                    source_badge = "<span class='badge' style='background-color: rgba(66, 133, 244, 0.3); color: #4285f4;'>🤖 AI</span>"
                
                # Build metadata string
                metadata_parts = []
                if song.get('year'):
                    metadata_parts.append(f"📅 {song['year']}")
                if song.get('language'):
                    metadata_parts.append(f"🌐 {song['language']}")
                if song.get('genre'):
                    metadata_parts.append(f"🎸 {song['genre']}")
                
                metadata_str = " • ".join(metadata_parts)
                
                # Matching phrase display
                matching_phrase = ""
                if song.get('matching_phrase'):
                    phrase = song['matching_phrase'][:60]
                    if len(song['matching_phrase']) > 60:
                        phrase += "..."
                    matching_phrase = f"<br><span style='color: #888; font-size: 0.9em; font-style: italic;'>💬 \"{phrase}\"</span>"
                
                st.markdown(f"""
                <div class="song-card">
                    <div style="margin-bottom: 0.5rem;">
                        <strong style="font-size: 1.3em; color: #1ed760;">🎵 {song['title']}</strong> 
                        {confidence_badge} {source_badge}
                    </div>
                    <div style="color: #b3b3b3; font-size: 1.1em; margin-bottom: 0.3rem;">
                        🎤 {song['artist']}
                    </div>
                    {f"<div style='color: #888; margin-bottom: 0.3rem;'>💿 {song['album']}</div>" if song.get('album') else ""}
                    {f"<div style='color: #666; font-size: 0.9em;'>{metadata_str}</div>" if metadata_str else ""}
                    {matching_phrase}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("View Lyrics", key=f"btn_{idx}", use_container_width=True):
                    with st.spinner("Loading lyrics..."):
                        lyrics = fetch_lyrics(song['artist'], song['title'])
                    
                    if lyrics:
                        st.session_state.current_lyrics = lyrics
                        st.session_state.search_results = []
                        st.rerun()
                    else:
                        st.error("Lyrics not available for this song")

    # Display lyrics
    if st.session_state.current_lyrics:
        st.markdown("---")
        data = st.session_state.current_lyrics
        
        st.success(f"✅ Lyrics loaded from **{data['source']}**")
        
        st.markdown(f"## 🎵 {data['title']}")
        st.markdown(f"### 🎤 {data['artist']}")
        
        st.markdown(f'<div class="lyrics-box">{data["lyrics"]}</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            lyrics_text = f"{data['title']} - {data['artist']}\n\n{data['lyrics']}"
            st.download_button(
                "📥 Download Lyrics",
                lyrics_text,
                f"{data['artist']}_{data['title']}.txt",
                use_container_width=True
            )
        with col2:
            if st.button("🔄 New Search", use_container_width=True):
                st.session_state.current_lyrics = None
                st.session_state.search_results = []
                st.rerun()
        with col3:
            if st.button("🔗 Share", use_container_width=True):
                st.info("Copy this page URL to share!")

# Footer
st.markdown("---")
st.markdown("""
    <div class="footer">
        <p><strong>DECIBEL</strong> - Powered by AI 🤖 | Made with ❤️ for music lovers</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            Search through millions of songs • AI-powered matching • Voice recognition
        </p>
    </div>
""", unsafe_allow_html=True)

# Debug info in sidebar
with st.expander("🔧 System Information"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Features Status:**")
        st.write(f"✅ Voice Search" if VOICE_AVAILABLE else "❌ Voice Search")
        st.write(f"✅ AI Search" if GEMINI_AVAILABLE else "❌ AI Search")
        st.write(f"✅ API Key Set" if st.session_state.gemini_api_key else "❌ API Key Set")
    with col2:
        st.write("**Session Data:**")
        st.write(f"Search Results: {len(st.session_state.search_results)}")
        st.write(f"Lyrics Loaded: {'Yes' if st.session_state.current_lyrics else 'No'}")
        if st.session_state.recognized_text:
            st.write(f"Last Voice: {st.session_state.recognized_text[:30]}...")