"use client";
import React, { useState } from "react";


const API_BASE = "http://localhost:8000";

export default function ApiDemo() {
  // State for each form
  const [textInput, setTextInput] = useState("");
  const [textLang, setTextLang] = useState("");
  const [textResult, setTextResult] = useState<any>(null);
  const [textError, setTextError] = useState("");

  const [urlInput, setUrlInput] = useState("");
  const [urlResult, setUrlResult] = useState<any>(null);
  const [urlError, setUrlError] = useState("");

  const [transInput, setTransInput] = useState("");
  const [transLang, setTransLang] = useState("");
  const [transResult, setTransResult] = useState<any>(null);
  const [transError, setTransError] = useState("");

  // Handlers
  async function handleAnalyzeText(e: React.FormEvent) {
    e.preventDefault();
    setTextError("");
    setTextResult(null);
    try {
      const res = await fetch(`${API_BASE}/analyze/text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: textInput, source_language: textLang, target_language: "en" })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setTextResult(data);
    } catch (err: any) {
      setTextError(err.message);
    }
  }

  async function handleAnalyzeUrl(e: React.FormEvent) {
    e.preventDefault();
    setUrlError("");
    setUrlResult(null);
    try {
      const res = await fetch(`${API_BASE}/analyze/url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: urlInput, target_language: "en" })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setUrlResult(data);
    } catch (err: any) {
      setUrlError(err.message);
    }
  }

  async function handleTranslate(e: React.FormEvent) {
    e.preventDefault();
    setTransError("");
    setTransResult(null);
    try {
      const res = await fetch(`${API_BASE}/translate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: transInput, source_language: transLang, target_language: "en" })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Error");
      setTransResult(data);
    } catch (err: any) {
      setTransError(err.message);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold mb-4">AI Sentiment Gauge Demo</h1>

      {/* Analyze Text */}
      <section className="bg-white rounded shadow p-4">
        <h2 className="text-xl font-semibold mb-2">Analyze Text</h2>
        <form onSubmit={handleAnalyzeText} className="space-y-2">
          <input
            className="border p-2 w-full"
            placeholder="Enter text..."
            value={textInput}
            onChange={e => setTextInput(e.target.value)}
            required
          />
          <input
            className="border p-2 w-full"
            placeholder="Source language (optional, e.g. 'en', 'fr')"
            value={textLang}
            onChange={e => setTextLang(e.target.value)}
          />
          <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">Analyze</button>
        </form>
        {textError && <div className="text-red-600 mt-2">{textError}</div>}
        {textResult && (
          <div className="mt-2 text-sm">
            <pre>{JSON.stringify(textResult, null, 2)}</pre>
          </div>
        )}
      </section>

      {/* Analyze URL */}
      <section className="bg-white rounded shadow p-4">
        <h2 className="text-xl font-semibold mb-2">Analyze URL</h2>
        <form onSubmit={handleAnalyzeUrl} className="space-y-2">
          <input
            className="border p-2 w-full"
            placeholder="Enter URL..."
            value={urlInput}
            onChange={e => setUrlInput(e.target.value)}
            required
          />
          <button className="bg-blue-600 text-white px-4 py-2 rounded" type="submit">Analyze</button>
        </form>
        {urlError && <div className="text-red-600 mt-2">{urlError}</div>}
        {urlResult && (
          <div className="mt-2 text-sm">
            <pre>{JSON.stringify(urlResult, null, 2)}</pre>
          </div>
        )}
      </section>

      {/* Translate */}
      <section className="bg-white rounded shadow p-4">
        <h2 className="text-xl font-semibold mb-2">Translate to English</h2>
        <form onSubmit={handleTranslate} className="space-y-2">
          <input
            className="border p-2 w-full"
            placeholder="Enter text to translate..."
            value={transInput}
            onChange={e => setTransInput(e.target.value)}
            required
          />
          <input
            className="border p-2 w-full"
            placeholder="Source language (optional, e.g. 'fr')"
            value={transLang}
            onChange={e => setTransLang(e.target.value)}
          />
          <button className="bg-green-600 text-white px-4 py-2 rounded" type="submit">Translate</button>
        </form>
        {transError && <div className="text-red-600 mt-2">{transError}</div>}
        {transResult && (
          <div className="mt-2 text-sm">
            <pre>{JSON.stringify(transResult, null, 2)}</pre>
          </div>
        )}
      </section>
    </div>
  );
}
