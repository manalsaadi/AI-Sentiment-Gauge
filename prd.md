# PRD: AI-Powered Comment Analyzer (Local, Python-Based, Translation-First)

## 1. Introduction
This document defines the requirements for an AI-powered application that analyzes online comments and reviews. Its purpose is to provide marketers and product managers with actionable insights about brand perception and user sentiment without needing manual review. The application will run locally, use only free and lightweight Python libraries, and focus on producing quick, reliable insights.  

In order to support **multiple European languages**, the tool will first **detect the language of each comment, translate comments into English locally (no LLMs or cloud APIs), and then process only the English translations**.  

## 2. The Problem
Marketers and product managers waste significant time manually reviewing web comments and product reviews. Identifying sentiment trends, common feedback themes, and key discussion topics at scale is labor-intensive. Existing enterprise solutions often rely on cloud LLMs or paid APIs, which may introduce latency, cost, and compliance risks.  

The challenge is to provide robust, accurate insights locally and for free using classical NLP methods, while also handling **multilingual European comments consistently through English translation**.  

## 3. The Solution
A Python-based comment analyzer that:  
- Accepts user input as pasted text or automatically scraped website comments.  
- **Detects the language of each comment.**  
- **Translates all comments into English locally using offline translation libraries.**  
- Cleans and preprocesses translated text (lowercasing, stop-word removal, handling punctuation, and emojis).  
- Performs sentiment analysis (positive, negative, neutral).  
- Extracts key topics and keywords using statistical methods (frequency, TF-IDF, POS filtering).  
- Generates a concise, shareable Markdown report summarizing results.  
- Runs quickly and locally with no reliance on commercial APIs.  

The first release will support multilingual input but will conduct analysis only on translated English text.  

## 4. User Stories & Core Features

### Persona: The Marketer
- Wants to quickly understand audience sentiment on a campaign.  
- Needs a concise report to share with leadership.  

### Persona: The Product Manager
- Wants to discover feature requests, bugs, and key user concerns.  
- Needs keyword/topic clustering to prioritize roadmap items.  

### Core User Stories
1. **Analyze Text Block**  
   "As a marketer, I want to paste comments (in any European language) and get a sentiment breakdown, so I can quickly gauge public opinion."  
   - Output: All comments are auto-detected, translated into English, then analyzed for sentiment percentages.  

2. **Scrape Website Comments**  
   "As a product manager, I want the tool to extract comments from a specified web page so I don’t have to copy/paste them manually."  
   - Includes support for common HTML comment patterns, error handling for invalid or blocked URLs, robust scraping that respects `robots.txt`, and automatic translation into English for further processing.  

3. **Identify Key Topics**  
   "As a marketer/product manager, I want the tool to identify the most common and meaningful nouns/adjectives in the translated text, so I can understand common concerns or praise."  
   - Method: translation → keyword extraction via frequency counts, lemmatization, and TF-IDF scoring.  

4. **Generate Markdown Report**  
   "As a marketer or product manager, I want a concise report that I can share with my team."  
   - Report includes: sentiment breakdown, top 5–10 keywords with counts, and optional JSON/CSV export for structured data.  

5. **Optional Visualization (Future)**  
   - Simple charts (sentiment pie chart, keyword frequency bar chart) using Matplotlib for better readability.  

## 5. Test-Driven Development (TDD) Approach
All core functionality will follow a "Red, Green, Refactor" cycle. Tests are written first, then code is implemented.  

### Translation Workflow Tests
- German input *Das Produkt ist großartig* → Correct translation: "The product is great."  
- French input *J'aime ce service* → "I like this service."  
- Spanish input *No me gusta la actualización* → "I don't like the update."  
- Edge cases: slang, misspellings, empty input → translated gracefully.  

### Sentiment Analysis Tests
- Positive statement ("I love this product") → Positive.  
- Negative statement ("This is terrible") → Negative.  
- Neutral statement ("It was delivered on Tuesday") → Neutral.  
- Edge cases: empty strings, sarcasm, mixed sentiment.  

### Keyword Extraction Tests
- Text with repeated keyword in various capitalizations.  
- Stop words removed correctly.  
- Numbers/symbols ignored.  
- Verify TF-IDF ranks terms above basic frequency in longer passages.  

### Web Scraping Tests
- Valid URL with identifiable comments class → Extracts comments.  
- Invalid URL → Error handled gracefully.  
- Page without comments → Returns empty set without crashing.  
- Pages requiring headers/UA → Ensure configurable user-agent and retry logic.  
- **Translated output tested end-to-end.**  

### Report Generation Tests
- Markdown output includes sentiment summary and keyword list.  
- JSON/CSV option exports correct structure.  

### Performance Tests
- 500 multilingual comments translated and processed in <15 seconds on modern hardware.  
- Memory footprint stable for medium-scale datasets (up to ~5,000 comments).  

## 6. Success Metrics
- **Translation Accuracy**: ≥80% meaning preservation across European languages.  
- **Analysis Accuracy**: ≥70% agreement with manually labeled test sets (after translation).  
- **Performance**: 500 comments translated + processed in under 15 seconds.  
- **Usability**: Reports readable by non-technical stakeholders without modification.  
- **Actionability**: Insights directly inform campaign changes or roadmap prioritization.  

## 7. Technical Requirements

### Tools & Stack
- **Language Detection**: `langdetect` or `fasttext`.  
- **Translation (Offline)**: `Argos Translate` (OpenNMT-based) or MarianMT models (Hugging Face, pre-downloaded for offline use).  
- **Text Processing**: spaCy, NLTK, or TextBlob (for English-only sentiment baselines).  
- **Keyword Extraction**: scikit-learn (TF-IDF), spaCy (POS tagging).  
- **Web Scraping**: Beautiful Soup, Requests.  
- **Reporting**: Markdown templates, optional Matplotlib for visualization.  

### Architecture
- **Input Module**: CLI paste or web scraping.  
- **Language Detection Module**: Determines source language for each comment.  
- **Translation Module**: Offline local translation into English.  
- **Preprocessing Module**: clean translated text.  
- **Analysis Module**: sentiment + topic extraction in English.  
- **Report Module**: Markdown/JSON/CSV output.  

### Constraints
- No cloud APIs or LLM dependencies.  
- Runs locally on standard laptops without GPU.  
- Scraper respects robots.txt settings.  

## 8. Future Roadmap
- Improved local translation models for domain-specific vocabulary.  
- Dashboard UI (web-based interface instead of CLI).  
- Advanced topic clustering (LDA or BERTopic with English embeddings).  
- Side-by-side display: original text + translated English text.  
- Batch ingestion of comments from CSV/Excel.  
