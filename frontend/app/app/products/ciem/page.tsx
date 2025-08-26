"use client";

import { useState, useEffect } from "react";

// --- START INLINE HELPER: apiFetch ---
// Workaround: Defining apiFetch in the same file due to file creation issues.
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


// --- START INLINE COMPONENT: Table ---
// Workaround: Defining Table component in the same file.
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


export default function CIEMPage() {
  const [findings, setFindings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFindings = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch("/ciem/findings");
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
      await apiFetch("/ciem/scans", { method: "POST" });
      await fetchFindings();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFindings();
  }, []);

  const columns = [
    { Header: "Identity ID", accessor: "identity_id" },
    { Header: "Type", accessor: "identity_type" },
    { Header: "Issue", accessor: "issue" },
    { Header: "Severity", accessor: "severity" },
    { Header: "Description", accessor: "description" },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">CIEM Findings</h1>
        <button
          onClick={handleScan}
          disabled={isLoading}
          className="px-4 py-2 font-semibold text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:bg-gray-400"
        >
          {isLoading ? "Scanning..." : "Trigger New Scan"}
        </button>
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
