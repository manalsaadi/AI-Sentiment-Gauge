# AI Sentiment Gauge API

A FastAPI-based REST API for analyzing multilingual comments and reviews, with local translation and processing capabilities.

## Features

- RESTful API endpoints for sentiment analysis and translation
- Support for multiple languages (French, German, Spanish, English)
- Local translation using Argos Translate
- Web scraping support with URL-based analysis
- Sentiment analysis (positive, negative, neutral) with confidence scores
- Automatic language detection
- Interactive API documentation with Swagger UI

## Setup

1. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```
 (must be done before running the CLI)

3. Install required NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

## API Endpoints

### 1. Analyze Text
```http
POST /analyze/text
```
Analyzes the sentiment of provided text with optional translation.

**Request Body:**
```json
{
    "text": "Your text here",
    "source_language": "fr",  // optional, auto-detected if not provided
    "target_language": "en"   // defaults to English
}
```

### 2. Analyze URL Content
```http
POST /analyze/url
```
Scrapes text from a URL and analyzes its sentiment.

**Request Body:**
```json
{
    "url": "https://example.com",
    "target_language": "en"  // defaults to English
}
```

### 3. Translate Text
```http
POST /translate
```
Translates text between supported languages.

**Request Body:**
```json
{
    "text": "Your text here",
    "source_language": "fr",  // optional, auto-detected if not provided
    "target_language": "en"
}
```

## Project Structure

```
/project_root
├── src/
│   ├── input/          # Web scraping and text input handling
│   ├── translation/    # Language detection & translation
│   ├── preprocessing/  # Text cleaning and normalization
│   ├── analysis/      # Sentiment analysis
│   ├── models.py      # Pydantic models for API
│   └── main.py        # FastAPI application
├── tests/             # Test suite
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Development

1. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Install required NLTK data:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

4. Run the API server:
```powershell
cd src
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`

