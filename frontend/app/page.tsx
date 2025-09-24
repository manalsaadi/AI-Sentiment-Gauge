"use client";
import React from 'react';

export default function Home() {
  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h1 className="text-2xl font-bold text-white mb-2">Welcome to AI Comment Analyzer</h1>
        <p className="text-gray-300">Analyze sentiment and extract insights from multilingual comments</p>
      </div>

      {/* Quick Actions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Paste Text Card */}
        <a href="/paste" className="bg-gray-800 hover:bg-gray-700 rounded-lg p-6 transition-colors group">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mr-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">Paste Text</h3>
              <p className="text-sm text-gray-400">Quick analysis from pasted comments</p>
            </div>
          </div>
          <div className="text-sm text-green-400 group-hover:text-green-300">Start analyzing →</div>
        </a>

        {/* Scrape URL Card */}
        <a href="/scrape" className="bg-gray-800 hover:bg-gray-700 rounded-lg p-6 transition-colors group">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/>
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">Scrape URL</h3>
              <p className="text-sm text-gray-400">Extract comments from web pages</p>
            </div>
          </div>
          <div className="text-sm text-blue-400 group-hover:text-blue-300">Start scraping →</div>
        </a>

        {/* View Results Card */}
        <a href="/results" className="bg-gray-800 hover:bg-gray-700 rounded-lg p-6 transition-colors group">
          <div className="flex items-center mb-4">
            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mr-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">View Results</h3>
              <p className="text-sm text-gray-400">See analysis and reports</p>
            </div>
          </div>
          <div className="text-sm text-purple-400 group-hover:text-purple-300">View reports →</div>
        </a>
      </div>

      {/* Recent Activity */}
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Recent Activity</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between py-2 border-b border-gray-700">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
              <span className="text-gray-300">Text analysis completed - 85% positive sentiment</span>
            </div>
            <span className="text-sm text-gray-500">2 min ago</span>
          </div>
          <div className="flex items-center justify-between py-2 border-b border-gray-700">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
              <span className="text-gray-300">URL scraped - 24 comments found</span>
            </div>
            <span className="text-sm text-gray-500">15 min ago</span>
          </div>
          <div className="flex items-center justify-between py-2">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
              <span className="text-gray-300">Report exported to Markdown</span>
            </div>
            <span className="text-sm text-gray-500">1 hour ago</span>
          </div>
        </div>
      </div>
    </div>
  );
}
