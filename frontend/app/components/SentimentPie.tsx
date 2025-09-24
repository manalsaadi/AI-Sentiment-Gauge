"use client";
import React from 'react';

export default function SentimentPie({positive=65, neutral=25, negative=10}:{positive?:number, neutral?:number, negative?:number}){
  // Calculate the circumference and offsets for the pie chart
  const total = positive + neutral + negative;
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  
  const positiveOffset = 0;
  const neutralOffset = (positive / 100) * circumference;
  const negativeOffset = ((positive + neutral) / 100) * circumference;

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Sentiment Analysis</h3>
      
      <div className="flex items-center justify-center">
        <div className="relative">
          {/* SVG Pie Chart */}
          <svg className="transform -rotate-90" width="140" height="140">
            <circle
              cx="70"
              cy="70"
              r={radius}
              fill="none"
              stroke="#374151"
              strokeWidth="12"
            />
            
            {/* Positive segment */}
            <circle
              cx="70"
              cy="70"
              r={radius}
              fill="none"
              stroke="#10b981"
              strokeWidth="12"
              strokeDasharray={circumference}
              strokeDashoffset={circumference - (positive / 100) * circumference}
              className="transition-all duration-500"
            />
            
            {/* Neutral segment */}
            <circle
              cx="70"
              cy="70"
              r={radius}
              fill="none"
              stroke="#6b7280"
              strokeWidth="12"
              strokeDasharray={circumference}
              strokeDashoffset={circumference - (neutral / 100) * circumference}
              style={{
                transform: `rotate(${(positive / 100) * 360}deg)`,
                transformOrigin: '70px 70px'
              }}
              className="transition-all duration-500"
            />
            
            {/* Negative segment */}
            <circle
              cx="70"
              cy="70"
              r={radius}
              fill="none"
              stroke="#ef4444"
              strokeWidth="12"
              strokeDasharray={circumference}
              strokeDashoffset={circumference - (negative / 100) * circumference}
              style={{
                transform: `rotate(${((positive + neutral) / 100) * 360}deg)`,
                transformOrigin: '70px 70px'
              }}
              className="transition-all duration-500"
            />
          </svg>
          
          {/* Center label */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <div className="text-2xl font-bold text-white">{positive}%</div>
              <div className="text-sm text-gray-400">Positive</div>
            </div>
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
            <span className="text-gray-300">Positive</span>
          </div>
          <span className="text-green-400 font-semibold">{positive}%</span>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-gray-500 rounded-full mr-3"></div>
            <span className="text-gray-300">Neutral</span>
          </div>
          <span className="text-gray-400 font-semibold">{neutral}%</span>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-red-500 rounded-full mr-3"></div>
            <span className="text-gray-300">Negative</span>
          </div>
          <span className="text-red-400 font-semibold">{negative}%</span>
        </div>
      </div>
    </div>
  );
}
