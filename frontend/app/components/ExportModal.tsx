"use client";
import React from 'react';

export default function ExportModal({isOpen=false,onClose=()=>{}}:{isOpen?:boolean,onClose?:()=>void}){
  if(!isOpen) return null;
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-gray-900 p-6 rounded w-96">
        <h3 className="text-lg font-semibold mb-2">Export</h3>
        <div className="space-y-2">
          <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Include original</label>
          <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Include translations</label>
          <label className="flex items-center gap-2"><input type="checkbox" defaultChecked /> Include keyword counts</label>
        </div>
        <div className="mt-4 flex justify-end">
          <button onClick={onClose} className="px-3 py-2 bg-blue-600 rounded text-white">Download Markdown</button>
        </div>
      </div>
    </div>
  );
}
