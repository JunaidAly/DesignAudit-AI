import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DesignAudit AI',
  description: 'Your AI-Powered Design Team Member',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
