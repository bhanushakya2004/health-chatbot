import { Heart } from 'lucide-react';

interface LogoProps {
  collapsed?: boolean;
}

export function Logo({ collapsed }: LogoProps) {
  return (
    <div className="flex items-center gap-2.5">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 shadow-md shadow-blue-200">
        <Heart className="h-6 w-6 text-white" fill="currentColor" />
      </div>
      {!collapsed && (
        <span className="text-xl font-bold tracking-tight text-slate-900">Health<span className="text-blue-600">Bot</span></span>
      )}
    </div>
  );
}
