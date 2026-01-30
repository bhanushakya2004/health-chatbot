export function TypingIndicator() {
  return (
    <div className="flex gap-4 animate-fade-in">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary">
        <svg
          className="h-5 w-5"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z"
            fill="currentColor"
            opacity="0.2"
          />
          <path
            d="M12 6C8.69 6 6 8.69 6 12C6 15.31 8.69 18 12 18C15.31 18 18 15.31 18 12"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            className="animate-spin origin-center"
            style={{ animationDuration: '1s' }}
          />
        </svg>
      </div>
      <div className="flex items-center gap-1 rounded-2xl rounded-bl-md bg-chat-assistant px-4 py-3 shadow-sm border border-border/50">
        <span className="h-2 w-2 rounded-full bg-muted-foreground animate-typing" style={{ animationDelay: '0s' }} />
        <span className="h-2 w-2 rounded-full bg-muted-foreground animate-typing" style={{ animationDelay: '0.2s' }} />
        <span className="h-2 w-2 rounded-full bg-muted-foreground animate-typing" style={{ animationDelay: '0.4s' }} />
      </div>
    </div>
  );
}
