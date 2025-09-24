"use client";
import React, { useState } from 'react';
import ProgressCard from '../components/ProgressCard';

interface AnalysisResult {
  sentiment?: {
    positive: number;
    neutral: number;
    negative: number;
  };
  keywords?: string[];
  summary?: string;
}

export default function PastePage() {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    
    setIsAnalyzing(true);
    try {
      const response = await fetch('http://localhost:8000/analyze/text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Analysis failed:', error);
    }
    setIsAnalyzing(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h1 className="text-2xl font-bold text-white mb-2">Paste Text Analysis</h1>
        <p className="text-gray-300">Analyze sentiment and extract keywords from your text</p>
      </div>

      {/* Input Section */}
      <div className="bg-gray-800 rounded-lg p-6">
        <label className="block text-sm font-medium text-gray-300 mb-3">
          Enter your text for analysis
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full h-48 px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-none"
          placeholder="Paste your comments here for sentiment analysis and keyword extraction..."
          disabled={isAnalyzing}
        />
        <div className="flex justify-between items-center mt-4">
          <span className="text-sm text-gray-400">
            {text.length} characters
          </span>
          <div className="flex space-x-3">
            <button
              onClick={() => setText('')}
              className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
              disabled={!text || isAnalyzing}
            >
              Clear
            </button>
            <button
              onClick={handleAnalyze}
              disabled={!text.trim() || isAnalyzing}
              className="px-6 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors flex items-center"
            >
              {isAnalyzing ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Analyzing...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                  Analyze Text
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Progress Section */}
      {isAnalyzing && (
        <ProgressCard 
          steps={["Detect Language", "Translate", "Analyze Sentiment"]}
          currentIndex={1}
        />
      )}

      {/* Results Section */}
      {results && (
        <div className="space-y-4">
          {/* Sentiment Results */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Sentiment Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-600/20 border border-green-600/30 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-green-400">
                  {results.sentiment?.positive || 0}%
                </div>
                <div className="text-sm text-green-300">Positive</div>
              </div>
              <div className="bg-gray-600/20 border border-gray-600/30 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-gray-400">
                  {results.sentiment?.neutral || 0}%
                </div>
                <div className="text-sm text-gray-300">Neutral</div>
              </div>
              <div className="bg-red-600/20 border border-red-600/30 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-red-400">
                  {results.sentiment?.negative || 0}%
                </div>
                <div className="text-sm text-red-300">Negative</div>
              </div>
            </div>
          </div>

          {/* Keywords Results */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Key Insights</h3>
            <div className="space-y-3">
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Top Keywords</h4>
                <div className="flex flex-wrap gap-2">
                  {(results.keywords || ['example', 'keywords', 'extracted']).map((keyword: string, index: number) => (
                    <span key={index} className="px-3 py-1 bg-blue-600/20 border border-blue-600/30 text-blue-300 rounded-full text-sm">
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-300 mb-2">Analysis Summary</h4>
                <p className="text-gray-400 text-sm">
                  {results.summary || 'Analysis complete. The text has been processed for sentiment analysis and keyword extraction.'}
                </p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-end space-x-3">
            <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors">
              Export Results
            </button>
            <button 
              onClick={() => {
                setText('');
                setResults(null);
              }}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              Analyze New Text
            </button>
          </div>
        </div>
      )}

      {/* Help Section */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-3">Tips for Better Analysis</h3>
        <ul className="space-y-2 text-sm text-gray-400">
          <li className="flex items-start">
            <span className="text-green-400 mr-2">•</span>
            Paste longer text for more accurate sentiment analysis
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">•</span>
            The system supports multiple languages and will auto-detect
          </li>
          <li className="flex items-start">
            <span className="text-green-400 mr-2">•</span>
            Keywords are extracted based on frequency and relevance
          </li>
        </ul>
      </div>
    </div>
  );
}
