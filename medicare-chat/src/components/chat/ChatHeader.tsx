import { Menu, User, Info } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from '@/components/ThemeToggle';
import { Logo } from '@/components/Logo';

interface ChatHeaderProps {
  onMenuClick: () => void;
  onProfileClick: () => void;
  onAboutClick: () => void;
  showMenuButton?: boolean;
}

export function ChatHeader({
  onMenuClick,
  onProfileClick,
  onAboutClick,
  showMenuButton,
}: ChatHeaderProps) {
  return (
    <header className="flex items-center justify-between px-4 py-3 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80">
      <div className="flex items-center gap-2">
        {showMenuButton && (
          <Button variant="ghost" size="icon" onClick={onMenuClick} className="md:hidden">
            <Menu className="h-5 w-5" />
          </Button>
        )}
        <div className="md:hidden">
          <Logo />
        </div>
      </div>

      <div className="flex items-center gap-1">
        <Button
          variant="ghost"
          size="icon"
          onClick={onAboutClick}
          className="h-9 w-9 rounded-lg"
        >
          <Info className="h-4 w-4" />
          <span className="sr-only">About MediHelp</span>
        </Button>
        <ThemeToggle />
        <Button
          variant="ghost"
          size="icon"
          onClick={onProfileClick}
          className="h-9 w-9 rounded-lg"
        >
          <User className="h-4 w-4" />
          <span className="sr-only">Profile</span>
        </Button>
      </div>
    </header>
  );
}
