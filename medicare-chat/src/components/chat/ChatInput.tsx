import { useState, useRef, KeyboardEvent } from 'react';
import { Send, Paperclip, Mic, X, FileText, ImageIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { cn } from '@/lib/utils';
import { Attachment } from '@/types/chat';
import { toast } from '@/hooks/use-toast';

interface ChatInputProps {
  onSend: (message: string, attachments?: Attachment[]) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [attachments, setAttachments] = useState<Attachment[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (message.trim() || attachments.length > 0) {
      onSend(message.trim(), attachments.length > 0 ? attachments : undefined);
      setMessage('');
      setAttachments([]);
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    // Auto-resize
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files) {
      const newAttachments: Attachment[] = Array.from(files).map((file, i) => ({
        id: `${Date.now()}-${i}`,
        name: file.name,
        type: file.type.includes('pdf') ? 'pdf' : 'image',
        size: `${(file.size / 1024).toFixed(0)} KB`,
      }));
      setAttachments([...attachments, ...newAttachments]);
      toast({
        title: 'File attached',
        description: `${files.length} file(s) ready to upload`,
      });
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeAttachment = (id: string) => {
    setAttachments(attachments.filter((a) => a.id !== id));
  };

  const handleVoiceInput = () => {
    toast({
      title: 'Voice input',
      description: 'Voice input feature coming soon!',
    });
  };

  return (
    <div className="border-t border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 p-4">
      {/* Attachments Preview */}
      {attachments.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {attachments.map((attachment) => (
            <div
              key={attachment.id}
              className="flex items-center gap-2 rounded-lg bg-muted px-3 py-2 text-sm"
            >
              {attachment.type === 'pdf' ? (
                <FileText className="h-4 w-4 text-destructive" />
              ) : (
                <ImageIcon className="h-4 w-4 text-health-info" />
              )}
              <span className="max-w-[150px] truncate">{attachment.name}</span>
              <Button
                variant="ghost"
                size="icon"
                className="h-5 w-5 hover:bg-destructive/20"
                onClick={() => removeAttachment(attachment.id)}
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
          ))}
        </div>
      )}

      {/* Input Area */}
      <div className="flex items-end gap-2">
        {/* File Upload */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          multiple
          className="hidden"
          onChange={handleFileSelect}
        />
        <Button
          variant="ghost"
          size="icon"
          className="shrink-0 h-10 w-10 rounded-xl hover:bg-accent"
          onClick={() => fileInputRef.current?.click()}
          disabled={disabled}
        >
          <Paperclip className="h-5 w-5" />
          <span className="sr-only">Attach file</span>
        </Button>

        {/* Text Input */}
        <div className="relative flex-1">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your health question..."
            disabled={disabled}
            className={cn(
              'min-h-[44px] max-h-[200px] resize-none rounded-xl border-border bg-muted/50 py-3 pr-24',
              'focus-visible:ring-1 focus-visible:ring-primary focus-visible:border-primary',
              'placeholder:text-muted-foreground/70'
            )}
            rows={1}
          />
          <div className="absolute right-2 bottom-2 flex items-center gap-1">
            {/* Voice Input */}
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8 rounded-lg hover:bg-accent"
              onClick={handleVoiceInput}
              disabled={disabled}
            >
              <Mic className="h-4 w-4" />
              <span className="sr-only">Voice input</span>
            </Button>

            {/* Send Button */}
            <Button
              size="icon"
              className={cn(
                'h-8 w-8 rounded-lg transition-smooth',
                message.trim() || attachments.length > 0
                  ? 'bg-primary hover:bg-primary/90'
                  : 'bg-muted text-muted-foreground'
              )}
              onClick={handleSend}
              disabled={disabled || (!message.trim() && attachments.length === 0)}
            >
              <Send className="h-4 w-4" />
              <span className="sr-only">Send message</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <p className="text-xs text-muted-foreground text-center mt-3">
        MediHelp provides general health information only. Always consult a healthcare professional for medical advice.
      </p>
    </div>
  );
}
