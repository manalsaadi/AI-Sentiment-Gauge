"use client";
import React, { useState } from 'react';
import ProgressCard from '../components/ProgressCard';

interface ScrapeResult {
  comments_found: number;
  sentiment?: {
    positive: number;
    neutral: number;
    negative: number;
  };
  keywords?: string[];
  url?: string;
}

export default function ScrapePage() {
  const [url, setUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [results, setResults] = useState<ScrapeResult | null>(null);
  const [error, setError] = useState('');

  const isValidUrl = (urlString: string) => {
    try {
      new URL(urlString);
      return true;
    } catch {
      return false;
    }
  };

  const handleScrape = async () => {
    if (!url.trim() || !isValidUrl(url)) {
      setError('Please enter a valid URL');
      return;
    }
    
    setError('');
    setIsProcessing(true);
    try {
      const response = await fetch('http://localhost:8000/analyze/url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Scraping failed:', error);
      setError('Failed to scrape the URL. Please check the URL and try again.');
    }
    setIsProcessing(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h1 className="text-2xl font-bold text-white mb-2">Web Scraping Analysis</h1>
        <p className="text-gray-300">Extract and analyze comments from web pages automatically</p>
      </div>

      {/* URL Input Section */}
      <div className="bg-gray-800 rounded-lg p-6">
        <label className="block text-sm font-medium text-gray-300 mb-3">
          Website URL to scrape
        </label>
        <div className="space-y-3">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            placeholder="https://example.com/article-with-comments"
            disabled={isProcessing}
          />
          {error && (
            <div className="text-red-400 text-sm flex items-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {error}
            </div>
          )}
        </div>

        <div className="flex justify-between items-center mt-6">
          <div className="flex items-center space-x-4">
            <label className="flex items-center">
              <input type="checkbox" className="rounded bg-gray-700 border-gray-600" defaultChecked />
              <span className="ml-2 text-sm text-gray-300">Auto-translate to English</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="rounded bg-gray-700 border-gray-600" defaultChecked />
              <span className="ml-2 text-sm text-gray-300">Extract keywords</span>
            </label>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={() => setUrl('')}
              className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
              disabled={!url || isProcessing}
            >
              Clear
            </button>
            <button
              onClick={handleScrape}
              disabled={!url.trim() || isProcessing}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors flex items-center"
            >
              {isProcessing ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                  Processing...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9"/>
                  </svg>
                  Scrape & Analyze
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Progress Section */}
      {isProcessing && (
        <ProgressCard 
          steps={["Fetching Page", "Extracting Comments", "Translating", "Analyzing"]}
          currentIndex={2}
        />
      )}

      {/* Results Section */}
      {results && (
        <div className="space-y-4">
          {/* Overview */}
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Scraping Results</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-600/20 border border-blue-600/30 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-blue-400">
                  {results.comments_found || 0}
                </div>
                <div className="text-sm text-blue-300">Comments Found</div>
              </div>
              <div className="bg-green-600/20 border border-green-600/30 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-green-400">
                  {results.sentiment?.positive || 0}%
                </div>
                <div className="text-sm text-green-300">Positive</div>
              </div>
              <div className="bg-purple-600/20 border border-purple-600/30 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-purple-400">
                  {results.keywords?.length || 0}
                </div>
                <div className="text-sm text-purple-300">Keywords</div>
              </div>
            </div>
          </div>

          {/* Sentiment Breakdown */}
          {results.sentiment && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Sentiment Distribution</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-green-300">Positive</span>
                  <div className="flex-1 mx-4 bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-green-500 h-2 rounded-full" 
                      style={{width: `${results.sentiment.positive}%`}}
                    ></div>
                  </div>
                  <span className="text-green-400 font-medium">{results.sentiment.positive}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Neutral</span>
                  <div className="flex-1 mx-4 bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-gray-500 h-2 rounded-full" 
                      style={{width: `${results.sentiment.neutral}%`}}
                    ></div>
                  </div>
                  <span className="text-gray-400 font-medium">{results.sentiment.neutral}%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-red-300">Negative</span>
                  <div className="flex-1 mx-4 bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-red-500 h-2 rounded-full" 
                      style={{width: `${results.sentiment.negative}%`}}
                    ></div>
                  </div>
                  <span className="text-red-400 font-medium">{results.sentiment.negative}%</span>
                </div>
              </div>
            </div>
          )}

          {/* Keywords */}
          {results.keywords && results.keywords.length > 0 && (
            <div className="bg-gray-800 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Top Keywords</h3>
              <div className="flex flex-wrap gap-2">
                {results.keywords.map((keyword: string, index: number) => (
                  <span key={index} className="px-3 py-1 bg-purple-600/20 border border-purple-600/30 text-purple-300 rounded-full text-sm">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end space-x-3">
            <a 
              href="/results"
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
            >
              View Detailed Results
            </a>
            <button 
              onClick={() => {
                setUrl('');
                setResults(null);
                setError('');
              }}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              Scrape Another URL
            </button>
          </div>
        </div>
      )}

      {/* Tips Section */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-3">Scraping Tips</h3>
        <ul className="space-y-2 text-sm text-gray-400">
          <li className="flex items-start">
            <span className="text-blue-400 mr-2">•</span>
            Works best with news articles, blog posts, and product pages
          </li>
          <li className="flex items-start">
            <span className="text-blue-400 mr-2">•</span>
            Some sites may block automated scraping - this is normal
          </li>
          <li className="flex items-start">
            <span className="text-blue-400 mr-2">•</span>
            Processing time depends on the number of comments found
          </li>
        </ul>
      </div>
    </div>
  );
}
