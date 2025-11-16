'use client';

import { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { ChatInterface } from '@/components/ChatInterface';
import { SiGithub } from '@icons-pack/react-simple-icons';

export default function Home() {
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // This is the "glue" function for FileUpload
  const handleUploadSuccess = (filename: string) => {
    setUploadedFile(filename);
    setUploadError(null);
  };

  // This is the "glue" function for FileUpload
  const handleUploadError = (error: string) => {
    setUploadError(error);
    setUploadedFile(null);
  };

  // --- THIS IS THE REAL CHAT LOGIC ---
  const handleSendMessage = async (message: string) => {
    console.log('Sending real message to backend:', message);

    try {
      const response = await fetch('document-intelligence-production-6269.up.railway.app/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: message,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Chat request failed');
      }

      const result = await response.json();
      console.log('Received answer from backend:', result.answer);
      return {
        answer: result.answer,
      };
      
    } catch (error: any) {
      console.error('Chat error:', error);
      // Return an error message to be displayed in the chat
      return {
        answer: `Sorry, I ran into an error: ${error.message}`,
      };
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4 py-12 md:p-24">
      <div className="w-full max-w-2xl flex-1">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">Document Intelligence</h1>
          <p className="text-lg text-gray-400">
            Upload a PDF and ask questions about its content.
          </p>
        </div>

        {/* Conditional Logic: Show Upload or Chat */}
        {!uploadedFile ? (
          <FileUpload
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />
        ) : (
          <ChatInterface
            filename={uploadedFile}
            onSendMessage={handleSendMessage} // This now passes our REAL function
          />
        )}
      </div>

      {/* Footer Link */}
      <footer className="text-gray-500 pt-6">
        <a
          href="https://github.com/your-username/document-intelligence" // <-- TODO: Change this to your GitHub repo link
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 hover:text-white"
        >
          <SiGithub className="h-4 w-4" />
          View on GitHub
        </a>
      </footer>
    </main>
  );
}