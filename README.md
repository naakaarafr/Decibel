# 🎧 DECIBEL

**Your AI-Powered Lyrics Discovery Platform**

Decibel is a modern, feature-rich lyrics finder application that helps you discover songs through multiple search methods including traditional name search, text-based lyrics search, and voice recognition. Powered by AI and equipped with a beautiful, responsive interface.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Features

### 🔍 Multiple Search Methods
- **Search by Name**: Traditional search using artist and song title
- **Search by Lyrics**: Type any lyrics you remember to find matching songs
- **Voice Search**: Speak or sing lyrics to identify songs (with speech recognition)

### 🤖 AI-Powered Identification
- Integrated with Google's Gemini AI for intelligent song identification
- Advanced lyric matching with confidence scoring
- Multi-language and multi-genre support
- Handles phonetic similarities and misheard lyrics

### 🎨 Modern UI/UX
- Beautiful dark theme with gradient effects
- Responsive design that works on all devices
- Smooth animations and transitions
- Glassmorphism and modern design elements
- Custom styled components

### 📊 Rich Metadata Display
- Song titles, artists, and albums
- Release years and languages
- Genres and confidence scores
- Matching lyric phrases
- Source attribution

### 💾 Additional Features
- Download lyrics as text files
- Multiple API fallbacks for reliability
- Session state management
- Error handling and user feedback
- System status information

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/naakaarafr/Decibel.git
cd Decibel
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Getting a Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste it into your `.env` file

### Step 4: Install Optional Dependencies

For **Voice Search** functionality:
```bash
pip install SpeechRecognition pyaudio
```

**Note**: PyAudio installation may require additional system dependencies:
- **Windows**: Download wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- **macOS**: `brew install portaudio && pip install pyaudio`
- **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`

## 📦 Requirements

Create a `requirements.txt` file with:
```txt
streamlit>=1.28.0
requests>=2.31.0
python-dotenv>=1.0.0
google-generativeai>=0.3.0
SpeechRecognition>=3.10.0  # Optional, for voice search
PyAudio>=0.2.13  # Optional, for voice search
```

## 🎯 Usage

### Running the Application
```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`

### Search Methods

#### 1. Search by Name
- Navigate to the "🔍 Search by Name" tab
- Enter the artist name (e.g., "Arijit Singh")
- Enter the song title (e.g., "Tum Hi Ho")
- Click "Find Lyrics"

#### 2. Search by Typing Lyrics
- Navigate to the "🎤 Search by Lyrics" tab
- Type any lyrics you remember in the text area
- Click "Search by Text"
- Browse through matching songs
- Click "View Lyrics" on any result to see full lyrics

#### 3. Voice Search
- Navigate to the "🎤 Search by Lyrics" tab
- Click "Voice Search" button
- Wait for the countdown
- Speak or sing the lyrics clearly when prompted
- View the recognized text and matching results

## 🏗️ Project Structure

```
Decibel/
│
├── main.py              # Main application file
├── .env                 # Environment variables (create this)
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
│
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

### API Sources
The application uses multiple lyrics APIs for reliability:
1. **lyrics-api.fly.dev** - Primary lyrics source
2. **lrclib.net** - Secondary source with search capabilities
3. **Gemini AI** - AI-powered song identification

### Customization
You can customize the appearance by modifying the CSS in the `st.markdown()` sections of `main.py`.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Add support for more lyrics APIs
- Implement lyrics translation
- Add playlist creation features
- Improve AI song identification accuracy
- Add music video links
- Implement user favorites/history

## 📝 API Usage Notes

### Gemini AI
- Free tier: 60 requests per minute
- Required for AI-powered search
- Handles complex lyric matching and multi-language support

### Lyrics APIs
- No authentication required
- Rate limits may apply
- Fallback mechanisms implemented for reliability

## ⚠️ Known Limitations

- Voice recognition requires a working microphone
- Voice search accuracy depends on audio quality and pronunciation
- Some songs may not be available in the lyrics databases
- Gemini API has rate limits on free tier
- PyAudio installation can be challenging on some systems

## 🐛 Troubleshooting

### Common Issues

**1. Voice Search Not Working**
```bash
# Reinstall speech recognition
pip uninstall SpeechRecognition pyaudio
pip install SpeechRecognition pyaudio
```

**2. Gemini API Errors**
- Verify your API key is correct in `.env`
- Check if you've exceeded rate limits
- Ensure `google-generativeai` is installed

**3. No Lyrics Found**
- Try different spelling variations
- Use the voice search feature
- Search with partial lyrics
- Check if the song is in the database

**4. PyAudio Installation Fails**
- Install system dependencies first (see Installation section)
- Try using pre-built wheels for your platform

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI capabilities
- [lyrics-api.fly.dev](https://lyrics-api.fly.dev/) for lyrics data
- [lrclib.net](https://lrclib.net/) for lyrics search
- The open-source community for inspiration

## 📧 Contact

Project Link: [https://github.com/naakaarafr/Decibel](https://github.com/naakaarafr/Decibel)

---

*Search through millions of songs • AI-powered matching • Voice recognition*
