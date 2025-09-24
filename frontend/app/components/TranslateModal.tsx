"use client";
import React from 'react';

export default function TranslateModal({isOpen=false,onClose=()=>{}}:{isOpen?:boolean,onClose?:()=>void}){
  if(!isOpen) return null;
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-gray-900 p-6 rounded w-96">
        <h3 className="text-lg font-semibold mb-2">Translate</h3>
        <input className="w-full p-2 rounded bg-gray-800 border border-gray-700" placeholder="Type a sentence..." />
        <div className="mt-4 flex justify-end">
          <button onClick={onClose} className="px-3 py-2 bg-blue-600 rounded text-white">Close</button>
        </div>
      </div>
    </div>
  );
}
