"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Shield, BarChart, FileText, Settings, LogOut, Users } from "lucide-react";

// --- START INLINE COMPONENT: Sidebar ---
// Workaround: Defining component in the same file due to file creation issues.
const Sidebar = () => {
  const router = useRouter();
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    router.push("/sign-in");
  };

  const navItems = [
    { href: "/app/dashboard", icon: BarChart, label: "Dashboard" },
    { href: "/app/products/cspm", icon: Shield, label: "CSPM-Lite" },
    { href: "/app/products/ciem", icon: Users, label: "CIEM-Lite" },
    { href: "/app/products/compliance", icon: FileText, label: "Compliance" },
    { href: "/app/settings", icon: Settings, label: "Settings" },
  ];

  return (
    <div className="flex flex-col h-full w-64 bg-gray-800 text-white">
      <div className="p-4 text-2xl font-bold">SecurAI</div>
      <nav className="flex-grow">
        <ul>
          {navItems.map((item) => (
            <li key={item.label} className="px-4 py-2 hover:bg-gray-700">
              <a href={item.href} className="flex items-center">
                <item.icon className="w-5 h-5 mr-3" />
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <div className="p-4 border-t border-gray-700">
        <button onClick={handleLogout} className="flex items-center w-full px-4 py-2 hover:bg-gray-700">
          <LogOut className="w-5 h-5 mr-3" />
          Logout
        </button>
      </div>
    </div>
  );
};
// --- END INLINE COMPONENT: Sidebar ---


export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // --- START INLINE HOOK: useAuth ---
  // Workaround: Auth check logic is included directly in the layout.
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/sign-in");
    } else {
      // TODO: In a real app, you should validate the token here.
      setIsAuthenticated(true);
    }
  }, [router]);
  // --- END INLINE HOOK: useAuth ---

  if (!isAuthenticated) {
    // Render a loading state or null while checking auth
    return (
        <div className="flex items-center justify-center min-h-screen">
            <p>Loading...</p>
        </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-900">
      <Sidebar />
      <main className="flex-1 p-8 overflow-y-auto">
        {children}
      </main>
    </div>
  );
}
