"use client";
import React, { useState } from 'react';

interface CommentRow {
  id: number;
  original: string;
  detected: string;
  translated: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  confidence: number;
  source: string;
  timestamp: string;
}

export default function CommentTable({
  rows = [
    {id: 1, original: 'J\'adore ce service, très efficace!', detected: 'fr', translated: 'I love this service, very efficient!', sentiment: 'positive', confidence: 0.95, source: 'website', timestamp: '2024-01-15 10:30'},
    {id: 2, original: 'Great product, fast shipping!', detected: 'en', translated: 'Great product, fast shipping!', sentiment: 'positive', confidence: 0.89, source: 'review', timestamp: '2024-01-15 09:15'},
    {id: 3, original: 'Servicio regular, puede mejorar', detected: 'es', translated: 'Regular service, could improve', sentiment: 'neutral', confidence: 0.76, source: 'survey', timestamp: '2024-01-15 08:45'},
    {id: 4, original: 'Disappointed with the quality', detected: 'en', translated: 'Disappointed with the quality', sentiment: 'negative', confidence: 0.92, source: 'review', timestamp: '2024-01-15 07:20'},
    {id: 5, original: 'Ottimo supporto clienti!', detected: 'it', translated: 'Excellent customer support!', sentiment: 'positive', confidence: 0.94, source: 'feedback', timestamp: '2024-01-14 16:30'}
  ]
}:{rows?: CommentRow[]}) {
  
  const [sortBy, setSortBy] = useState<keyof CommentRow>('timestamp');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  const getSentimentColor = (sentiment: string) => {
    switch(sentiment) {
      case 'positive': return 'text-green-400 bg-green-400/20';
      case 'negative': return 'text-red-400 bg-red-400/20';
      case 'neutral': return 'text-gray-400 bg-gray-400/20';
      default: return 'text-gray-400 bg-gray-400/20';
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch(sentiment) {
      case 'positive': return '😊';
      case 'negative': return '😔';
      case 'neutral': return '😐';
      default: return '❓';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const sortedRows = [...rows].sort((a, b) => {
    const aVal = a[sortBy];
    const bVal = b[sortBy];
    const modifier = sortOrder === 'desc' ? -1 : 1;
    
    if (aVal < bVal) return -1 * modifier;
    if (aVal > bVal) return 1 * modifier;
    return 0;
  });

  const paginatedRows = sortedRows.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const totalPages = Math.ceil(rows.length / itemsPerPage);

  return (
    <div className="bg-gray-800 rounded-lg overflow-hidden">
      <div className="p-4 border-b border-gray-700">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold text-white">Comment Analysis Details</h3>
          <div className="flex items-center space-x-2 text-sm">
            <span className="text-gray-400">
              Showing {((currentPage - 1) * itemsPerPage) + 1}-{Math.min(currentPage * itemsPerPage, rows.length)} of {rows.length}
            </span>
            <div className="flex space-x-1">
              <button 
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="px-2 py-1 bg-gray-700 hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded transition-colors"
              >
                ←
              </button>
              <button 
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="px-2 py-1 bg-gray-700 hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded transition-colors"
              >
                →
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-700/50">
            <tr>
              <th className="text-left p-4 text-sm font-medium text-gray-300">
                <button 
                  onClick={() => {
                    setSortBy('original');
                    setSortOrder(sortBy === 'original' && sortOrder === 'asc' ? 'desc' : 'asc');
                  }}
                  className="flex items-center hover:text-white transition-colors"
                >
                  Original Comment
                  <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"/>
                  </svg>
                </button>
              </th>
              <th className="text-left p-4 text-sm font-medium text-gray-300">Language</th>
              <th className="text-left p-4 text-sm font-medium text-gray-300">Translation</th>
              <th className="text-center p-4 text-sm font-medium text-gray-300">
                <button 
                  onClick={() => {
                    setSortBy('sentiment');
                    setSortOrder(sortBy === 'sentiment' && sortOrder === 'asc' ? 'desc' : 'asc');
                  }}
                  className="flex items-center hover:text-white transition-colors mx-auto"
                >
                  Sentiment
                  <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"/>
                  </svg>
                </button>
              </th>
              <th className="text-center p-4 text-sm font-medium text-gray-300">Confidence</th>
              <th className="text-left p-4 text-sm font-medium text-gray-300">Source</th>
              <th className="text-left p-4 text-sm font-medium text-gray-300">
                <button 
                  onClick={() => {
                    setSortBy('timestamp');
                    setSortOrder(sortBy === 'timestamp' && sortOrder === 'asc' ? 'desc' : 'asc');
                  }}
                  className="flex items-center hover:text-white transition-colors"
                >
                  Time
                  <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"/>
                  </svg>
                </button>
              </th>
            </tr>
          </thead>
          <tbody>
            {paginatedRows.map((row, index) => (
              <tr key={row.id} className="border-t border-gray-700 hover:bg-gray-700/30 transition-colors">
                <td className="p-4 max-w-xs">
                  <div className="text-white text-sm line-clamp-2">{row.original}</div>
                </td>
                <td className="p-4">
                  <span className="inline-block px-2 py-1 bg-blue-600/20 text-blue-300 text-xs rounded-full font-medium uppercase">
                    {row.detected}
                  </span>
                </td>
                <td className="p-4 max-w-xs">
                  <div className="text-gray-300 text-sm line-clamp-2">{row.translated}</div>
                </td>
                <td className="p-4 text-center">
                  <div className="flex items-center justify-center">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getSentimentColor(row.sentiment)}`}>
                      <span className="mr-1">{getSentimentIcon(row.sentiment)}</span>
                      {row.sentiment}
                    </span>
                  </div>
                </td>
                <td className="p-4 text-center">
                  <div className="flex items-center justify-center">
                    <div className={`text-sm font-medium ${
                      row.confidence >= 0.9 ? 'text-green-400' : 
                      row.confidence >= 0.7 ? 'text-yellow-400' : 
                      'text-red-400'
                    }`}>
                      {Math.round(row.confidence * 100)}%
                    </div>
                  </div>
                </td>
                <td className="p-4">
                  <span className="inline-block px-2 py-1 bg-purple-600/20 text-purple-300 text-xs rounded font-medium">
                    {row.source}
                  </span>
                </td>
                <td className="p-4">
                  <div className="text-gray-400 text-xs">{formatTimestamp(row.timestamp)}</div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {paginatedRows.length === 0 && (
        <div className="p-8 text-center">
          <div className="text-gray-400">
            <svg className="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-4.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
            </svg>
            <p>No comments to display</p>
            <p className="text-sm mt-1">Start analyzing some text to see results here</p>
          </div>
        </div>
      )}
    </div>
  );
}
