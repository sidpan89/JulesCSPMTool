"use client";

import { useState } from "react";

// --- START INLINE HELPER: apiFetch ---
async function apiFetch(endpoint: string, options: RequestInit = {}): Promise<any> {
  const BASE_URL = "http://localhost:8000/api/v1";
  const token = typeof window !== 'undefined' ? localStorage.getItem("access_token") : null;

  const headers = new Headers(options.headers);
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  // For HTML response, we need to handle it as text
  if (headers.get('Accept') === 'text/html') {
      return response.text();
  }

  return response.json();
}
// --- END INLINE HELPER: apiFetch ---


export default function CompliancePage() {
  const [reportHtml, setReportHtml] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateReport = async () => {
    setIsLoading(true);
    setError(null);
    setReportHtml(null);
    try {
      const html = await apiFetch("/compliance/reports", {
        method: "POST",
        headers: { 'Accept': 'text/html' },
        body: JSON.stringify({ report_type: "CIS_Benchmark_v1.4" }),
      });
      setReportHtml(html);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Compliance Reporter</h1>
        <button
          onClick={handleGenerateReport}
          disabled={isLoading}
          className="px-4 py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:bg-gray-400"
        >
          {isLoading ? "Generating..." : "Generate CIS Report"}
        </button>
      </div>

      {error && <p className="text-red-500 mb-4">Error: {error}</p>}

      <div className="p-4 bg-white rounded-lg shadow mt-4">
        <h2 className="text-xl font-semibold mb-4">Generated Report</h2>
        {isLoading && <p>Generating report, please wait...</p>}
        {reportHtml ? (
          <div dangerouslySetInnerHTML={{ __html: reportHtml }} />
        ) : (
          !isLoading && <p className="text-gray-500">Click the button to generate a new compliance report.</p>
        )}
      </div>
    </div>
  );
}
