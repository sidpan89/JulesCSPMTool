"use client";

import { useState, useEffect } from "react";

// --- START INLINE HELPER: apiFetch ---
async function apiFetch(endpoint: string, options: RequestInit = {}): Promise<any> {
  const BASE_URL = "http://localhost:8000/api/v1";
  const token = typeof window !== 'undefined' ? localStorage.getItem("access_token") : null;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
}
// --- END INLINE HELPER: apiFetch ---


// --- START INLINE COMPONENT: Table ---
const Table = ({ columns, data }: { columns: any[], data: any[] }) => {
  if (!data || data.length === 0) {
    return <p className="text-gray-500">No data available.</p>;
  }
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full bg-white rounded-lg shadow">
        <thead>
          <tr className="w-full bg-gray-100 text-left text-gray-600 uppercase text-sm">
            {columns.map((col) => (
              <th key={col.accessor} className="p-4">{col.Header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="border-b border-gray-200">
              {columns.map((col) => (
                <td key={col.accessor} className="p-4">{row[col.accessor]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
// --- END INLINE COMPONENT: Table ---


export default function KSPMPage() {
  const [findings, setFindings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [clusterId, setClusterId] = useState("aks-cluster-123"); // Default or from a selector

  const fetchFindings = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch("/kspm/findings");
      setFindings(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleScan = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await apiFetch("/kspm/scans", {
        method: "POST",
        body: JSON.stringify({ cluster_id: clusterId })
      });
      await fetchFindings();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Initially, don't fetch findings until a scan is run for a cluster
    setIsLoading(false);
    // Or fetch findings for a default/last scanned cluster
    // fetchFindings();
  }, []);

  const columns = [
    { Header: "Resource ID", accessor: "resource_id" },
    { Header: "Type", accessor: "resource_type" },
    { Header: "Namespace", accessor: "namespace" },
    { Header: "Issue", accessor: "issue" },
    { Header: "Severity", accessor: "severity" },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">KSPM Findings</h1>
        <div className="flex items-center space-x-4">
           <input
              type="text"
              value={clusterId}
              onChange={(e) => setClusterId(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="Enter Cluster ID"
            />
          <button
            onClick={handleScan}
            disabled={isLoading || !clusterId}
            className="px-4 py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:bg-gray-400"
          >
            {isLoading ? "Scanning..." : "Scan Cluster"}
          </button>
        </div>
      </div>
      {error && <p className="text-red-500 mb-4">Error: {error}</p>}
      {isLoading ? (
        <p>Loading findings...</p>
      ) : (
        <Table columns={columns} data={findings} />
      )}
    </div>
  );
}
