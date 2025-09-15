# AI-Powered Comment Analyzer

A Python-based tool for analyzing multilingual comments and reviews, with local translation and processing capabilities.

## Features

- Support for multiple languages (French, German, Spanish, English)
- Local translation using Argos Translate
- Web scraping support for social media and e-commerce platforms
- Single and batch comment analysis
- Sentiment analysis (positive, negative, neutral)
- Keyword extraction using frequency-based and TF-IDF approaches
- Markdown report generation

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

## Project Structure

```
/project_root
├── src/
│   ├── input/          # CLI and web scraping
│   ├── translation/    # Language detection & translation
│   ├── preprocessing/  # Text cleaning and normalization
│   ├── analysis/      # Sentiment and keyword analysis
│   └── reporting/     # Markdown report generation
├── tests/             # Test suite
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## Development
go

