"""Command-line interface for the AI-powered Comment Analyzer."""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from src.input.comment_input import CommentInput
from src.input.web_scraper import WebScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="AI-powered Comment Analyzer for multilingual comments"
    )
    parser.add_argument(
        "--input-type",
        choices=["paste", "file", "url"],
        required=True,
        help="Type of input: paste for direct input, file for text file, url for web scraping"
    )
    parser.add_argument(
        "--input",
        help="Input content: text for paste, file path for file, URL for web scraping"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Directory to save the analysis reports (default: ./reports)"
    )
    return parser

def main() -> None:
    # --- Ensure required NLTK resources are downloaded ---
    try:
        import nltk
        nltk.download('punkt', force=True)
        nltk.download('stopwords', force=True)
        nltk.download('wordnet', force=True)
        nltk.download('omw-1.4', force=True)
    except Exception as e:
        logger.warning(f"Could not auto-download NLTK resources: {e}")
    """Main entry point for the comment analyzer CLI."""
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    args.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.input_type == "paste":
            if not args.input:
                # If no input provided, read from stdin
                logger.info("Reading comments from standard input...")
                text = sys.stdin.read().strip()
            else:
                text = args.input
            comments = CommentInput.process_text_input(text)
            
        elif args.input_type == "file":
            if not args.input:
                parser.error("--input is required for file input type")
            file_path = Path(args.input)
            comments = CommentInput.process_file_input(file_path)
            
        elif args.input_type == "url":
            if not args.input:
                parser.error("--input is required for url input type")
            scraper = WebScraper()
            comments = scraper.scrape_comments(args.input)
        
        if not comments:
            logger.warning("No comments found in the input")
            return

        # --- Full processing pipeline ---

        # --- Ensure Argos Translate language models are installed ---
        try:
            import argostranslate.package, argostranslate.translate
            import requests, os
            # List of language model URLs (add more as needed)
            urls = [
                "https://www.argosopentech.com/argospm/index/translate-fr_en.argosmodel",
                "https://www.argosopentech.com/argospm/index/translate-de_en.argosmodel",
                "https://www.argosopentech.com/argospm/index/translate-es_en.argosmodel"
            ]
            installed_langs = [
                (pkg.from_code, pkg.to_code)
                for pkg in argostranslate.package.get_installed_packages()
            ]
            needed_langs = [("fr", "en"), ("de", "en"), ("es", "en")]
            for url, (from_code, to_code) in zip(urls, needed_langs):
                if (from_code, to_code) not in installed_langs:
                    filename = url.split("/")[-1]
                    logger.info(f"Downloading Argos model: {filename}")
                    r = requests.get(url)
                    with open(filename, "wb") as f:
                        f.write(r.content)
                    logger.info(f"Installing Argos model: {filename}")
                    argostranslate.package.install_from_path(filename)
                    os.remove(filename)
                    logger.info(f"Installed and removed {filename}")
        except Exception as e:
            logger.warning(f"Could not auto-install Argos Translate models: {e}")

        from src.translation.translator import Translator
        from src.preprocessing.preprocessor import TextPreprocessor
        from src.analysis.sentiment_analyzer import SentimentAnalyzer
        from src.analysis.keyword_extractor import KeywordExtractor
        from src.reporting.report_generator import ReportGenerator

        # 1. Detect language and translate to English
        translator = Translator()
        translated_comments = []
        for comment in comments:
            try:
                translated = translator.translate_to_english(comment)
                translated_comments.append(translated)
            except Exception as e:
                logger.warning(f"Translation failed for comment: {comment} | Error: {e}")
                translated_comments.append("")

        # 2. Preprocess text
        preprocessor = TextPreprocessor()
        preprocessed_comments = preprocessor.batch_preprocess(translated_comments)

        # 3. Analyze sentiment and extract keywords
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_results = sentiment_analyzer.batch_analyze(preprocessed_comments)
        sentiment_dist = sentiment_analyzer.get_sentiment_distribution(preprocessed_comments)

        keyword_extractor = KeywordExtractor()
        keyword_results = keyword_extractor.get_common_keywords(preprocessed_comments)

        # 4. Generate report
        report_generator = ReportGenerator()
        output_file = args.output_dir / "report.md"
        report_generator.generate_report(
            comments,  # original comments
            sentiment_results,
            keyword_results,
            sentiment_dist,
            output_file
        )

        logger.info(f"Analysis complete. Report saved in {output_file}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()