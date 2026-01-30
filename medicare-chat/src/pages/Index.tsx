import { useState, useCallback, useEffect } from 'react';
import { Sidebar } from '@/components/sidebar/Sidebar';
import { ChatArea } from '@/components/chat/ChatArea';
import { ChatInput } from '@/components/chat/ChatInput';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { ProfileModal } from '@/components/profile/ProfileModal';
import { AboutModal } from '@/components/AboutModal';
import { AuthModal } from '@/components/auth/AuthModal';
import { EmptyState } from '@/components/EmptyState';
import { Chat, Message, MedicalRecord, UserProfile, Attachment, ChatHistoryResponse } from '@/types/chat';
import { cn } from '@/lib/utils';
import { chatService } from '@/lib/chat';
import { userService } from '@/lib/user';
import { toast } from '@/hooks/use-toast';
import { useAuth } from '@/hooks/useAuth';

const Index = () => {
  const { isAuthenticated } = useAuth();

  // Sidebar state
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  // Chat state
  const [chats, setChats] = useState<ChatHistoryResponse[]>([]);
  const [activeChat, setActiveChat] = useState<Chat | null>(null);
  const [isTyping, setIsTyping] = useState(false);

  // User state
  const [user, setUser] = useState<UserProfile | null>(null);
  const [medicalRecords, setMedicalRecords] = useState<MedicalRecord[]>([]);

  // Modal state
  const [profileOpen, setProfileOpen] = useState(false);
  const [aboutOpen, setAboutOpen] = useState(false);
  const [authOpen, setAuthOpen] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');

  const loadChatHistory = useCallback(async () => {
    if (!isAuthenticated) return;
    try {
      const chatHistory = await chatService.getChatHistory();
      setChats(chatHistory);
    } catch (error) {
      console.error('Failed to load chat history:', error);
      toast({
        title: 'Error',
        description: 'Failed to load chat history.',
        variant: 'destructive',
      });
    }
  }, [isAuthenticated]);

  useEffect(() => {
    loadChatHistory();
  }, [loadChatHistory]);

  useEffect(() => {
    const loadUserData = async () => {
      if (!isAuthenticated) return;

      try {
        const userProfile = await userService.getCurrentUser();
        setUser(userProfile);

        const documents = await userService.getDocuments();
        const records: MedicalRecord[] = documents.map((doc) => ({
          id: doc.document_id,
          name: doc.title,
          date: new Date(doc.upload_date),
          fileType: doc.mime_type.includes('pdf') ? 'pdf' : doc.mime_type.includes('image') ? 'jpg' : 'png',
          size: `${Math.round(doc.file_size / 1024)} KB`,
        }));
        setMedicalRecords(records);
      } catch (error) {
        console.error('Failed to load user data:', error);
      }
    };

    loadUserData();
  }, [isAuthenticated]);

  const handleNewChat = useCallback(async () => {
    if (!isAuthenticated) return;
    try {
      const newChat = await chatService.createChat("New Chat", "Hello");
      setActiveChat(newChat);
      loadChatHistory();
      setMobileSidebarOpen(false);
    } catch (error) {
      console.error('Failed to create new chat:', error);
      toast({
        title: 'Error',
        description: 'Failed to create a new chat.',
        variant: 'destructive',
      });
    }
  }, [isAuthenticated, loadChatHistory]);

  const handleDeleteChat = useCallback(async (chatId: string) => {
    if (!isAuthenticated) return;
    try {
      await chatService.deleteChat(chatId);
      setChats((prev) => prev.filter((c) => c.id !== chatId));
      if (activeChat?.id === chatId) {
        setActiveChat(null);
      }
    } catch (error) {
      console.error('Failed to delete chat:', error);
      toast({
        title: 'Error',
        description: 'Failed to delete chat.',
        variant: 'destructive',
      });
    }
  }, [isAuthenticated, activeChat]);

  const handleSendMessage = useCallback(async (content: string, attachments?: Attachment[]) => {
    if (!activeChat) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
      attachments,
    };

    setActiveChat((prev) => prev ? { ...prev, messages: [...prev.messages, userMessage] } : null);
    setIsTyping(true);

    try {
      const assistantMessage = await chatService.addMessageToChat(activeChat.id, content);
      setActiveChat((prev) => prev ? { ...prev, messages: [...prev.messages, assistantMessage] } : null);
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.message || 'Failed to get response from AI',
        variant: 'destructive',
      });
    } finally {
      setIsTyping(false);
    }
  }, [activeChat]);

  const handleChatSelect = useCallback(async (chatId: string) => {
    if (!isAuthenticated) return;
    try {
      const selectedChat = await chatService.getChat(chatId);
      setActiveChat(selectedChat);
      setMobileSidebarOpen(false);
    } catch (error) {
      console.error('Failed to load chat:', error);
      toast({
        title: 'Error',
        description: 'Failed to load chat.',
        variant: 'destructive',
      });
    }
  }, [isAuthenticated]);

  const handleLoginClick = () => {
    setAuthMode('login');
    setAuthOpen(true);
  };

  const handleSignupClick = () => {
    setAuthMode('signup');
    setAuthOpen(true);
  };

  const handleUpdateUser = async (updatedUser: UserProfile) => {
    if (!user) return;
    try {
      const result = await userService.updateCurrentUser({ full_name: updatedUser.full_name });
      setUser(result);
      toast({
        title: 'Success',
        description: 'Your profile has been updated.',
      });
    } catch (error) {
      console.error('Failed to update user:', error);
      toast({
        title: 'Error',
        description: 'Failed to update your profile.',
        variant: 'destructive',
      });
    }
  };

  const handleAddRecord = async (record: MedicalRecord) => {
    // This should be handled by a file upload service
  };

  const handleDeleteRecord = async (id: string) => {
    try {
      await userService.deleteDocument(id);
      setMedicalRecords((prev) => prev.filter((r) => r.id !== id));
      toast({
        title: 'Success',
        description: 'The medical record has been deleted.',
      });
    } catch (error) {
      console.error('Failed to delete medical record:', error);
      toast({
        title: 'Error',
        description: 'Failed to delete the medical record.',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      <div
        className={cn(
          'fixed inset-y-0 left-0 z-50 md:relative md:z-0',
          'transform transition-transform duration-300 ease-out',
          mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        )}
      >
        <Sidebar
          chats={chats}
          activeChatId={activeChat?.id}
          onChatSelect={handleChatSelect}
          onNewChat={handleNewChat}
          onDeleteChat={handleDeleteChat}
          isCollapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          onLoginClick={handleLoginClick}
          onSignupClick={handleSignupClick}
        />
      </div>

      <main className="flex flex-1 flex-col min-w-0">
        <ChatHeader
          onMenuClick={() => setMobileSidebarOpen(true)}
          onProfileClick={() => setProfileOpen(true)}
          onAboutClick={() => setAboutOpen(true)}
          showMenuButton={!mobileSidebarOpen}
        />

        {activeChat ? (
          <>
            <ChatArea messages={activeChat.messages} isTyping={isTyping} />
            <ChatInput onSend={handleSendMessage} disabled={isTyping} />
          </>
        ) : (
          <EmptyState onNewChat={handleNewChat} />
        )}
      </main>

      {user && (
        <ProfileModal
          open={profileOpen}
          onClose={() => setProfileOpen(false)}
          user={user}
          records={medicalRecords}
          onUpdateUser={handleUpdateUser}
          onAddRecord={handleAddRecord}
          onDeleteRecord={handleDeleteRecord}
        />
      )}

      <AboutModal open={aboutOpen} onClose={() => setAboutOpen(false)} />

      <AuthModal
        open={authOpen}
        onClose={() => setAuthOpen(false)}
        mode={authMode}
        onModeChange={setAuthMode}
      />
    </div>
  );
};

export default Index;
