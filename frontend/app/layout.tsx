import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Cloud Security Suite",
  description: "An AI-powered, multi-tenant cloud security platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
          {children}
      </body>
    </html>
  );
}
