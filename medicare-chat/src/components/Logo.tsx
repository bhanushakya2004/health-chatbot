import { Heart } from 'lucide-react';

interface LogoProps {
  collapsed?: boolean;
}

export function Logo({ collapsed }: LogoProps) {
  return (
    <div className="flex items-center gap-2.5">
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary">
        <Heart className="h-5 w-5 text-primary-foreground" fill="currentColor" />
      </div>
      {!collapsed && (
        <span className="text-lg font-semibold tracking-tight">MediHelp</span>
      )}
    </div>
  );
}
