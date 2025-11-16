'use client';

import { User, Bot } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div
      className={`flex items-start gap-4 ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      {/* Icon */}
      {!isUser && (
        <div className="flex-shrink-0 rounded-full bg-gray-600 p-2">
          <Bot className="h-5 w-5 text-white" />
        </div>
      )}

      {/* Message Content */}
      <div
        className={`max-w-[75%] rounded-xl px-4 py-3 ${
          isUser
            ? 'rounded-br-none bg-blue-600 text-white'
            : 'rounded-bl-none bg-gray-700 text-gray-200'
        }`}
      >
        <p>{message.content}</p>
      </div>

      {/* Icon */}
      {isUser && (
        <div className="flex-shrink-0 rounded-full bg-gray-600 p-2">
          <User className="h-5 w-5 text-white" />
        </div>
      )}
    </div>
  );
}