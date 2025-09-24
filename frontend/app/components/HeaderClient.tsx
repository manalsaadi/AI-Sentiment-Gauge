"use client";
import React from 'react';
import TranslateModal from './TranslateModal';
import ExportModal from './ExportModal';

export default function HeaderClient(){
  const [translateOpen,setTranslateOpen]=React.useState(false);
  const [exportOpen,setExportOpen]=React.useState(false);

  return (
    <>
      <header className="flex items-center justify-between px-6 py-4 border-b border-gray-800">
        <div className="flex items-center gap-4">
          <img src="/Assets/Dashboard.png" alt="Dashboard preview" className="w-12 h-8 object-contain rounded" />
          <div>
            <h1 className="text-xl font-semibold">Dashboard</h1>
            <p className="text-sm text-gray-400">Analyze comments, translate and export reports</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button aria-label="Translate quick" onClick={()=>setTranslateOpen(true)} className="px-3 py-2 rounded bg-gray-800 hover:bg-gray-700" title="Quick translate">
            <span role="img" aria-hidden>🔁</span>
          </button>
          <button aria-label="Export" onClick={()=>setExportOpen(true)} className="px-3 py-2 rounded bg-blue-600 hover:bg-blue-500 text-white">Export</button>
        </div>
      </header>

      {/* Banner area for non-blocking warnings (translation unavailable, partial results) */}
      <div aria-live="polite" className="px-6 py-3">
        <div id="app-banner" className="hidden rounded-md bg-yellow-500 text-gray-900 px-4 py-2">Translation unavailable — continue analysis (best-effort)</div>
      </div>

      <TranslateModal isOpen={translateOpen} onClose={()=>setTranslateOpen(false)} />
      <ExportModal isOpen={exportOpen} onClose={()=>setExportOpen(false)} />
    </>
  );
}
