"""Reporting module for generating analysis reports in Markdown format."""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class MarkdownReport:
    """Generator for Markdown analysis reports."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.sections = []
        
    def add_header(self, title: str, level: int = 1) -> None:
        """Add a header to the report.
        
        Args:
            title: Header text
            level: Header level (1-6)
        """
        level = max(1, min(6, level))  # Ensure level is between 1 and 6
        self.sections.append(f"{'#' * level} {title}\n")
        
    def add_text(self, text: str) -> None:
        """Add plain text to the report.
        
        Args:
            text: Text content
        """
        self.sections.append(f"{text}\n")
        
    def add_bullet_list(self, items: List[str]) -> None:
        """Add a bullet point list to the report.
        
        Args:
            items: List of items to include
        """
        for item in items:
            self.sections.append(f"- {item}\n")
        self.sections.append("\n")
        
    def add_table(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> None:
        """Add a table to the report.
        
        Args:
            headers: List of column headers
            rows: List of row data
        """
        # Add header row
        self.sections.append("| " + " | ".join(headers) + " |\n")
        
        # Add separator row
        self.sections.append("| " + " | ".join(["---"] * len(headers)) + " |\n")
        
        # Add data rows
        for row in rows:
            self.sections.append("| " + " | ".join(str(cell) for cell in row) + " |\n")
        self.sections.append("\n")
        
    def add_code_block(self, code: str, language: str = "") -> None:
        """Add a code block to the report.
        
        Args:
            code: Code content
            language: Programming language for syntax highlighting
        """
        self.sections.append(f"```{language}\n{code}\n```\n")
        
    def get_content(self) -> str:
        """Get the complete report content.
        
        Returns:
            Complete report as a string
        """
        return "".join(self.sections)

class ReportGenerator:
    """Generator for comment analysis reports."""
    
    def generate_report(
        self,
        comments: List[str],
        sentiment_results: List[Dict[str, Any]],
        keyword_results: Dict[str, List[Dict[str, Any]]],
        sentiment_dist: Dict[str, float],
        output_file: Optional[Path] = None
    ) -> str:
        """Generate a complete analysis report.
        
        Args:
            comments: Original comments
            sentiment_results: Sentiment analysis results
            keyword_results: Keyword extraction results
            sentiment_dist: Sentiment distribution data
            output_file: Optional file path to save the report
            
        Returns:
            Report content as string
            
        Raises:
            ValueError: If input data is invalid
        """
        if not comments:
            raise ValueError("Comments list cannot be empty")
            
        report = MarkdownReport()
        
        # Add report header
        report.add_header("Comment Analysis Report")
        report.add_text(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.add_text(f"Total Comments Analyzed: {len(comments)}\n")
        
        # Add sentiment distribution
        report.add_header("Sentiment Analysis", 2)
        report.add_text("### Overall Sentiment Distribution")
        
        # Create sentiment table
        sentiment_table = [
            ["Sentiment", "Count", "Percentage"],
            ["Positive", str(sentiment_dist['positive_count']),
             f"{sentiment_dist['positive_percent']:.1f}%"],
            ["Negative", str(sentiment_dist['negative_count']),
             f"{sentiment_dist['negative_percent']:.1f}%"],
            ["Neutral", str(sentiment_dist['neutral_count']),
             f"{sentiment_dist['neutral_percent']:.1f}%"]
        ]
        report.add_table(sentiment_table[0], sentiment_table[1:])
        
        # Add keyword analysis
        report.add_header("Keyword Analysis", 2)
        
        # Frequency-based keywords
        report.add_text("### Most Frequent Keywords")
        freq_keywords = keyword_results['frequency_based']
        freq_table = [["Keyword", "Frequency"]]
        freq_table.extend([
            [kw['keyword'], str(kw['frequency'])]
            for kw in freq_keywords
        ])
        report.add_table(freq_table[0], freq_table[1:])
        
        # TF-IDF keywords
        report.add_text("### Important Keywords (TF-IDF)")
        tfidf_keywords = keyword_results['tfidf_based']
        tfidf_table = [["Keyword", "TF-IDF Score"]]
        tfidf_table.extend([
            [kw['keyword'], f"{kw['tfidf_score']:.4f}"]
            for kw in tfidf_keywords
        ])
        report.add_table(tfidf_table[0], tfidf_table[1:])
        
        # Table of all comments and their predicted sentiment
        report.add_header("Predicted Sentiment for Each Comment", 2)
        comment_sentiment_table = [["Comment", "Predicted Sentiment"]]
        for comment, result in zip(comments, sentiment_results):
            if not result:
                pred = "(error)"
            else:
                pred = result['sentiment']
            comment_sentiment_table.append([comment, pred])
        report.add_table(comment_sentiment_table[0], comment_sentiment_table[1:])
        
        # Get final report content
        content = report.get_content()
        
        # Save to file if path provided
        if output_file:
            try:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                output_file.write_text(content, encoding='utf-8')
                logger.info(f"Report saved to: {output_file}")
            except Exception as e:
                logger.error(f"Error saving report: {str(e)}")
                raise
                
        return content