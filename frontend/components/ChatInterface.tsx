'use client';

import { useState, useRef, useEffect, FormEvent } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { MessageBubble } from './MessageBubble';

// Define the shape of a message
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

// Define the props our component will accept
interface ChatInterfaceProps {
  filename: string;
  onSendMessage: (message: string) => Promise<{ answer: string }>;
}

export function ChatInterface({ filename, onSendMessage }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // This ref is for auto-scrolling to the bottom of the chat
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Add the initial welcome message from the assistant
  useEffect(() => {
    setMessages([
      {
        id: 'initial',
        role: 'assistant',
        content: `Ready! Ask me any questions about ${filename}.`,
      },
    ]);
  }, [filename]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault(); // Prevent page reload
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
    };

    // Add user message to UI
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setInput(''); // Clear input

    // --- THIS IS THE REAL API CALL ---
    try {
      // Call the function passed from page.tsx
      const { answer } = await onSendMessage(input);
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: answer,
      };
      
      setMessages((prev) => [...prev, assistantMessage]);

    } catch (error) {
      console.error(error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I ran into an error. Please try again.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col rounded-xl bg-gray-800 shadow-xl">
      {/* Header */}
      <div className="flex-shrink-0 rounded-t-xl border-b border-gray-600 bg-gray-700 p-4">
        <p className="text-center text-lg font-semibold text-white">
          Chat with: <span className="text-blue-300">{filename}</span>
        </p>
      </div>

      {/* Message List */}
      <div className="flex-1 space-y-6 overflow-y-auto p-4">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {/* This is the invisible element we scroll to */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="flex-shrink-0 border-t border-gray-600 p-4">
        <form onSubmit={handleSubmit} className="flex items-center gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            placeholder="Ask anything about your document..."
            className="flex-1 rounded-lg border border-gray-600 bg-gray-900 px-4 py-2 text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="rounded-full bg-blue-600 p-2 text-white transition-all hover:bg-blue-700 disabled:bg-gray-600"
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </form>
      </div>
    </div>
  );
}