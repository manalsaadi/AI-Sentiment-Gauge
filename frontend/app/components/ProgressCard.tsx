"use client";
import React from 'react';

export default function ProgressCard({steps, currentIndex}:{steps:string[], currentIndex:number}){
  return (
    <div className="p-4 bg-gray-800 rounded">
      <div className="flex items-center gap-4">
        {steps.map((s,i)=> (
          <div key={s} className={`flex items-center gap-2 ${i===currentIndex? 'text-green-400':'text-gray-400'}`}>
            <div className={`w-6 h-6 rounded-full flex items-center justify-center ${i<currentIndex? 'bg-green-400 text-gray-900':'bg-gray-700'}`}>{i<currentIndex? '✓': i+1}</div>
            <div>{s}</div>
          </div>
        ))}
      </div>
      <div className="mt-3 text-sm text-gray-400">Processing items — this may take a moment.</div>
    </div>
  );
}
