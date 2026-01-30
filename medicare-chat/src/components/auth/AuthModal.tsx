import { useState } from 'react';
import { X, Mail, Lock, User, Eye, EyeOff } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';
import { Separator } from '@/components/ui/separator';
import { Logo } from '@/components/Logo';
import { toast } from '@/hooks/use-toast';
import { useAuth } from '@/hooks/useAuth';

interface AuthModalProps {
  open: boolean;
  onClose: () => void;
  mode: 'login' | 'signup';
  onModeChange: (mode: 'login' | 'signup') => void;
}

export function AuthModal({ open, onClose, mode, onModeChange }: AuthModalProps) {
  const { login, signup } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (mode === 'login') {
        await login(email, password);
        toast({
          title: 'Login successful',
          description: 'Welcome back!',
        });
      } else {
        await signup(email, password, name);
        toast({
          title: 'Account created',
          description: 'Welcome to MediHelp!',
        });
      }
      onClose();
      setEmail('');
      setPassword('');
      setName('');
    } catch (error: any) {
      toast({
        title: 'Error',
        description: error.message || 'Authentication failed. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[400px]">
        <DialogHeader className="text-center pb-2">
          <div className="flex justify-center mb-4">
            <Logo />
          </div>
          <DialogTitle className="text-xl font-semibold">
            {mode === 'login' ? 'Welcome back' : 'Create an account'}
          </DialogTitle>
          <DialogDescription>
            {mode === 'login'
              ? 'Sign in to access your health records and chat history'
              : 'Join MediHelp to save your health journey'}
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'signup' && (
            <div className="grid gap-2">
              <Label htmlFor="name">Full Name</Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="name"
                  placeholder="Enter your name"
                  className="pl-10"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
            </div>
          )}

          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                className="pl-10"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                className="pl-10 pr-10"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="absolute right-1 top-1/2 -translate-y-1/2 h-7 w-7"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <Eye className="h-4 w-4 text-muted-foreground" />
                )}
              </Button>
            </div>
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? 'Please wait...' : mode === 'login' ? 'Sign in' : 'Create account'}
          </Button>
        </form>

        <Separator className="my-2" />

        <p className="text-center text-sm text-muted-foreground">
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <Button
            variant="link"
            className="p-0 h-auto font-semibold text-primary"
            onClick={() => onModeChange(mode === 'login' ? 'signup' : 'login')}
          >
            {mode === 'login' ? 'Sign up' : 'Sign in'}
          </Button>
        </p>
      </DialogContent>
    </Dialog>
  );
}
