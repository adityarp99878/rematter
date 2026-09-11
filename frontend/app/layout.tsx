import './globals.css';
import { Outfit, Inter } from 'next/font/google';
import Navbar from '../components/layout/Navbar';

// Load fonts
const outfit = Outfit({ 
  subsets: ['latin'],
  variable: '--font-outfit',
});

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata = {
  title: 'Material Rebirth AI | Agentic Circular Construction',
  description: 'AI marketplace for recovered construction materials',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${outfit.variable} font-sans relative antialiased selection:bg-emerald-500/30 selection:text-emerald-200`}>
        {/* Animated Background Blobs */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none z-[-1]">
          <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-emerald-600/20 rounded-full mix-blend-screen filter blur-[100px] animate-blob"></div>
          <div className="absolute top-[20%] right-[-10%] w-96 h-96 bg-teal-600/20 rounded-full mix-blend-screen filter blur-[100px] animate-blob animation-delay-2000"></div>
          <div className="absolute bottom-[-20%] left-[20%] w-96 h-96 bg-cyan-600/20 rounded-full mix-blend-screen filter blur-[100px] animate-blob animation-delay-4000"></div>
          <div className="absolute inset-0 bg-grid-pattern opacity-30"></div>
        </div>
        
        <Navbar />
        <main className="pt-24 min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}
