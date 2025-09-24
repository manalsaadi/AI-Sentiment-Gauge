"use client";
import React, { useState } from 'react';
import SentimentPie from '../components/SentimentPie';
import KeywordTagList from '../components/KeywordTagList';
import CommentTable from '../components/CommentTable';

export default function ResultsPage() {
  const [selectedFilter, setSelectedFilter] = useState('all');
  const [dateRange, setDateRange] = useState('last_7_days');

  // Mock data - in real app this would come from API
  const analysisData = {
    total_comments: 1247,
    sentiment: {
      positive: 65,
      neutral: 25,
      negative: 10
    },
    languages_detected: 8,
    keywords: ['excellent', 'quality', 'fast', 'support', 'reliable'],
    source_urls: 3,
    last_updated: '2 minutes ago'
  };

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <div className="bg-gray-800 rounded-lg p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-2xl font-bold text-white mb-2">Analysis Results</h1>
            <p className="text-gray-300">Comprehensive sentiment analysis and insights</p>
          </div>
          <div className="flex space-x-3">
            <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors flex items-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Export Report
            </button>
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Refresh
            </button>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-4 items-center">
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-300">Filter:</label>
            <select 
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="bg-gray-700 border border-gray-600 text-white rounded px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Comments</option>
              <option value="positive">Positive Only</option>
              <option value="negative">Negative Only</option>
              <option value="neutral">Neutral Only</option>
            </select>
          </div>
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-300">Date Range:</label>
            <select 
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="bg-gray-700 border border-gray-600 text-white rounded px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="last_7_days">Last 7 Days</option>
              <option value="last_30_days">Last 30 Days</option>
              <option value="last_90_days">Last 90 Days</option>
              <option value="all_time">All Time</option>
            </select>
          </div>
          <span className="text-sm text-gray-400 ml-auto">Last updated: {analysisData.last_updated}</span>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Total Comments</p>
              <p className="text-2xl font-bold text-white">{analysisData.total_comments.toLocaleString()}</p>
            </div>
            <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Overall Sentiment</p>
              <p className="text-2xl font-bold text-green-400">{analysisData.sentiment.positive}% Positive</p>
            </div>
            <div className="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.01M15 10h1.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Languages</p>
              <p className="text-2xl font-bold text-purple-400">{analysisData.languages_detected}</p>
            </div>
            <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-400">Sources</p>
              <p className="text-2xl font-bold text-orange-400">{analysisData.source_urls}</p>
            </div>
            <div className="w-12 h-12 bg-orange-500/20 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Charts and Analysis Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sentiment Chart */}
        <div className="lg:col-span-1">
          <SentimentPie />
        </div>

        {/* Keywords */}
        <div className="lg:col-span-1">
          <KeywordTagList />
        </div>

        {/* Summary Statistics */}
        <div className="lg:col-span-1">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Quick Stats</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Average Rating</span>
                <div className="flex items-center">
                  <div className="flex text-yellow-400">
                    {'★'.repeat(4)}{'☆'.repeat(1)}
                  </div>
                  <span className="ml-2 text-white font-medium">4.2</span>
                </div>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Response Rate</span>
                <span className="text-green-400 font-medium">87%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Peak Activity</span>
                <span className="text-blue-400 font-medium">2:00 PM</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Avg Comment Length</span>
                <span className="text-purple-400 font-medium">127 chars</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Detailed Comments Table */}
      <div className="bg-gray-800 rounded-lg p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-white">Comment Details</h3>
          <div className="flex space-x-2">
            <button className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors">
              Export CSV
            </button>
            <button className="px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors">
              Filter
            </button>
          </div>
        </div>
        <CommentTable />
      </div>

      {/* Trend Analysis */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Sentiment Trend</h3>
        <div className="h-64 flex items-center justify-center border border-gray-700 rounded-lg">
          <div className="text-center text-gray-400">
            <svg className="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            <p>Trend Chart Coming Soon</p>
            <p className="text-sm">Historical sentiment analysis over time</p>
          </div>
        </div>
      </div>
    </div>
  );
}
