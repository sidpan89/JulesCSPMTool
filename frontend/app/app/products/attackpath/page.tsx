"use client";

import { useState, useEffect } from "react";

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
  return response.json();
}
// --- END INLINE HELPER: apiFetch ---

const GraphVisualization = ({ analysis }: { analysis: any }) => {
  if (!analysis || !analysis.nodes || analysis.nodes.length === 0) {
    return <p className="text-gray-500">No analysis data available. Run an analysis to see the graph.</p>;
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-4">Attack Path Graph</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h4 className="font-semibold mb-2">Nodes</h4>
          <ul className="list-disc list-inside">
            {analysis.nodes.map((node: any) => (
              <li key={node.node_id}>
                <strong>{node.label}</strong> ({node.node_type})
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h4 className="font-semibold mb-2">Edges</h4>
           <ul className="list-disc list-inside">
            {analysis.edges.map((edge: any, index: number) => (
              <li key={index}>
                {edge.source_node_id} -&gt; <strong>{edge.label}</strong> -&gt; {edge.target_node_id}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};


export default function AttackPathPage() {
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch("/attackpath/analysis");
      setAnalysis(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch("/attackpath/analysis", { method: "POST" });
      setAnalysis(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis();
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Attack Path Analysis</h1>
        <button
          onClick={handleAnalysis}
          disabled={isLoading}
          className="px-4 py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:bg-gray-400"
        >
          {isLoading ? "Analyzing..." : "Trigger New Analysis"}
        </button>
      </div>
      {error && <p className="text-red-500 mb-4">Error: {error}</p>}
      {isLoading ? (
        <p>Loading analysis...</p>
      ) : (
        <GraphVisualization analysis={analysis} />
      )}
    </div>
  );
}
