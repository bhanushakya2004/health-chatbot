import { useRef, useEffect } from 'react';
import { ChatMessage } from './ChatMessage';
import { TypingIndicator } from './TypingIndicator';
import { Message } from '@/types/chat';

interface ChatAreaProps {
  messages: Message[];
  isTyping?: boolean;
}

export function ChatArea({ messages, isTyping }: ChatAreaProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto scrollbar-thin px-4 md:px-8 lg:px-16 py-6"
    >
      <div className="max-w-3xl mx-auto space-y-6">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isTyping && <TypingIndicator />}
      </div>
    </div>
  );
}
