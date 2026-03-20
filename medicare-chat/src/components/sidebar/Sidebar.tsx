import { useState } from 'react';
import { Plus, PanelLeftClose, PanelLeft, LogIn, UserPlus, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Logo } from '@/components/Logo';
import { ChatHistoryItem } from './ChatHistoryItem';
import { ChatHistoryResponse } from '@/types/chat';
import { cn } from '@/lib/utils';
import { Separator } from '@/components/ui/separator';
import { useAuth } from '@/hooks/useAuth';

interface SidebarProps {
  chats: ChatHistoryResponse[];
  activeChatId: string | null;
  onChatSelect: (chatId: string) => void;
  onNewChat: () => void;
  onDeleteChat: (chatId: string) => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  onLoginClick: () => void;
  onSignupClick: () => void;
}

export function Sidebar({
  chats,
  activeChatId,
  onChatSelect,
  onNewChat,
  onDeleteChat,
  isCollapsed,
  onToggleCollapse,
  onLoginClick,
  onSignupClick,
}: SidebarProps) {
  const { isAuthenticated, logout } = useAuth();

  return (
    <aside
      className={cn(
        'flex flex-col h-full bg-sidebar border-r border-sidebar-border transition-all duration-300',
        isCollapsed ? 'w-16' : 'w-64'
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4">
        <Logo collapsed={isCollapsed} />
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleCollapse}
          className="h-8 w-8 shrink-0"
        >
          {isCollapsed ? (
            <PanelLeft className="h-4 w-4" />
          ) : (
            <PanelLeftClose className="h-4 w-4" />
          )}
        </Button>
      </div>

      <div className="px-3">
        <Button
          onClick={onNewChat}
          className={cn(
            'w-full justify-start gap-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white shadow-md shadow-blue-100',
            isCollapsed && 'justify-center px-0'
          )}
        >
          <Plus className="h-4 w-4" />
          {!isCollapsed && <span>New Chat</span>}
        </Button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto scrollbar-thin px-3 py-4">
        {!isCollapsed && (
          <>
            <p className="text-xs font-medium text-muted-foreground mb-2 px-3">
              Recent Chats
            </p>
            <div className="space-y-1">
              {chats.map((chat) => (
                <ChatHistoryItem
                  key={chat.id}
                  chat={chat}
                  isActive={chat.id === activeChatId}
                  onClick={() => onChatSelect(chat.id)}
                  onDelete={() => onDeleteChat(chat.id)}
                />
              ))}
            </div>
          </>
        )}
      </div>

      {/* Auth Section */}
      <div className="p-3 border-t border-sidebar-border">
        {isAuthenticated ? (
          isCollapsed ? (
            <Button variant="ghost" size="icon" onClick={logout} title="Logout">
              <LogOut className="h-4 w-4" />
            </Button>
          ) : (
            <Button variant="outline" className="w-full justify-start gap-2" onClick={logout}>
              <LogOut className="h-4 w-4" />
              Log out
            </Button>
          )
        ) : (
          isCollapsed ? (
            <div className="flex flex-col gap-2">
              <Button variant="ghost" size="icon" onClick={onLoginClick}>
                <LogIn className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" onClick={onSignupClick}>
                <UserPlus className="h-4 w-4" />
              </Button>
            </div>
          ) : (
            <div className="flex flex-col gap-2">
              <Button variant="outline" className="w-full justify-start gap-2" onClick={onLoginClick}>
                <LogIn className="h-4 w-4" />
                Log in
              </Button>
              <Button variant="ghost" className="w-full justify-start gap-2" onClick={onSignupClick}>
                <UserPlus className="h-4 w-4" />
                Sign up
              </Button>
            </div>
          )
        )}
      </div>
    </aside>
  );
}
