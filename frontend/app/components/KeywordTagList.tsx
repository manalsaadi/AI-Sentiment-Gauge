"use client";
import React from 'react';

export default function KeywordTagList({
  items = [
    {term:'excellent', count:24},
    {term:'quality', count:18},
    {term:'fast', count:15},
    {term:'support', count:12},
    {term:'reliable', count:10},
    {term:'professional', count:8},
    {term:'responsive', count:6}
  ]
}:{items?:{term:string,count:number}[]}){
  
  const maxCount = Math.max(...items.map(item => item.count));
  
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Top Keywords</h3>
      
      <div className="space-y-3">
        {items.slice(0, 10).map((item, index) => {
          const percentage = (item.count / maxCount) * 100;
          
          return (
            <div key={item.term} className="flex items-center justify-between">
              <div className="flex items-center flex-1">
                <span className="text-gray-300 text-sm min-w-0 flex-1">{item.term}</span>
                <div className="flex-1 mx-3 bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-500" 
                    style={{width: `${percentage}%`}}
                  ></div>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-blue-400 font-semibold text-sm">{item.count}</span>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Tags View Toggle */}
      <div className="mt-6 pt-4 border-t border-gray-700">
        <div className="flex flex-wrap gap-2">
          {items.slice(0, 8).map(item => (
            <span 
              key={item.term} 
              className="px-3 py-1 bg-blue-600/20 border border-blue-600/30 text-blue-300 rounded-full text-xs font-medium hover:bg-blue-600/30 transition-colors cursor-pointer"
            >
              {item.term}
              <span className="ml-1 text-blue-400">{item.count}</span>
            </span>
          ))}
        </div>
        
        {items.length > 8 && (
          <button className="mt-3 text-sm text-gray-400 hover:text-white transition-colors">
            View all {items.length} keywords →
          </button>
        )}
      </div>
    </div>
  );
}
