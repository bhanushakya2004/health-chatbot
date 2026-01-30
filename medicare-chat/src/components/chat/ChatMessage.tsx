import { format } from 'date-fns';
import { User, Bot, FileText, ImageIcon } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Message } from '@/types/chat';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  return (
    <div
      className={cn(
        'flex gap-4 animate-fade-in',
        isUser ? 'flex-row-reverse' : 'flex-row'
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          'flex h-9 w-9 shrink-0 items-center justify-center rounded-full',
          isUser
            ? 'bg-primary text-primary-foreground'
            : isSystem
            ? 'bg-muted text-muted-foreground'
            : 'bg-primary/10 text-primary'
        )}
      >
        {isUser ? (
          <User className="h-5 w-5" />
        ) : (
          <Bot className="h-5 w-5" />
        )}
      </div>

      {/* Message Content */}
      <div
        className={cn(
          'flex flex-col max-w-[75%] gap-1',
          isUser ? 'items-end' : 'items-start'
        )}
      >
        <div
          className={cn(
            'rounded-2xl px-4 py-3 text-sm leading-relaxed',
            isUser
              ? 'bg-chat-user text-chat-user-foreground rounded-br-md'
              : isSystem
              ? 'bg-chat-system text-chat-system-foreground'
              : 'bg-chat-assistant text-chat-assistant-foreground shadow-sm border border-border/50 rounded-bl-md'
          )}
        >
          {/* Render markdown-like content */}
          <div className="prose prose-sm dark:prose-invert max-w-none">
            {message.content.split('\n').map((line, i) => {
              // Handle bold text
              const boldPattern = /\*\*(.+?)\*\*/g;
              const parts = line.split(boldPattern);
              
              return (
                <p key={i} className={cn('mb-2 last:mb-0', line === '' && 'h-2')}>
                  {parts.map((part, j) => 
                    j % 2 === 1 ? (
                      <strong key={j} className="font-semibold">{part}</strong>
                    ) : (
                      part
                    )
                  )}
                </p>
              );
            })}
          </div>

          {/* Attachments */}
          {message.attachments && message.attachments.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {message.attachments.map((attachment) => (
                <div
                  key={attachment.id}
                  className="flex items-center gap-2 rounded-lg bg-muted px-3 py-2 text-xs"
                >
                  {attachment.type === 'pdf' ? (
                    <FileText className="h-4 w-4 text-destructive" />
                  ) : (
                    <ImageIcon className="h-4 w-4 text-health-info" />
                  )}
                  <span className="max-w-[120px] truncate">{attachment.name}</span>
                  <span className="text-muted-foreground">{attachment.size}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Timestamp */}
        <span className="text-xs text-muted-foreground px-1">
          {format(message.timestamp, 'h:mm a')}
        </span>
      </div>
    </div>
  );
}
