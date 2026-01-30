import { ReactNode, useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { AuthModal } from './auth/AuthModal';

interface ProtectedRouteProps {
  children: ReactNode;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { isAuthenticated, isLoading } = useAuth();
  const [authOpen, setAuthOpen] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      setAuthOpen(true);
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <>
        <AuthModal 
          open={authOpen} 
          onClose={() => setAuthOpen(false)} 
          mode={authMode}
          onModeChange={setAuthMode}
        />
        <div className="flex items-center justify-center min-h-screen bg-background">
          <div className="text-center space-y-4">
            <h1 className="text-2xl font-bold">Welcome to MediHelp</h1>
            <p className="text-muted-foreground">Please sign in to continue</p>
          </div>
        </div>
      </>
    );
  }

  return <>{children}</>;
};
