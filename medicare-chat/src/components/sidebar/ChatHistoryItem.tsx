import { MessageSquare, MoreHorizontal, Trash2, Edit2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { ChatHistoryResponse } from '@/types/chat';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';

interface ChatHistoryItemProps {
  chat: ChatHistoryResponse;
  isActive: boolean;
  onClick: () => void;
  onDelete: () => void;
}

export function ChatHistoryItem({ chat, isActive, onClick, onDelete }: ChatHistoryItemProps) {
  return (
    <div
      className={cn(
        'group flex items-center gap-2 rounded-lg px-3 py-2.5 cursor-pointer transition-smooth',
        isActive
          ? 'bg-blue-600 text-white shadow-sm shadow-blue-200'
          : 'hover:bg-blue-50 text-slate-600 hover:text-blue-700'
      )}
      onClick={onClick}
    >
      <MessageSquare className="h-4 w-4 shrink-0" />
      <span className="flex-1 truncate text-sm">{chat.title}</span>
      <DropdownMenu>
        <DropdownMenuTrigger asChild onClick={(e) => e.stopPropagation()}>
          <Button
            variant="ghost"
            size="icon"
            className={cn(
              'h-7 w-7 opacity-0 group-hover:opacity-100 transition-opacity',
              isActive && 'opacity-100'
            )}
          >
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-40">
          <DropdownMenuItem>
            <Edit2 className="h-4 w-4 mr-2" />
            Rename
          </DropdownMenuItem>
          <DropdownMenuItem 
            className="text-destructive focus:text-destructive"
            onClick={(e) => {
              e.stopPropagation();
              onDelete();
            }}
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Delete
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
