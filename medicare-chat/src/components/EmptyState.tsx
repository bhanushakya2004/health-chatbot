import { MessageSquarePlus, Sparkles, FileText, History } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface EmptyStateProps {
  onNewChat: () => void;
}

export function EmptyState({ onNewChat }: EmptyStateProps) {
  const features = [
    {
      icon: Sparkles,
      title: 'Ask health questions',
      description: 'Get helpful information about symptoms, conditions, and wellness',
    },
    {
      icon: FileText,
      title: 'Upload reports',
      description: 'Share medical documents and get help understanding them',
    },
    {
      icon: History,
      title: 'Access records',
      description: 'Type "fetch my old records" to view your medical history',
    },
  ];

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 text-center">
      <div className="max-w-md space-y-8 animate-fade-in">
        <div className="space-y-4">
          <div className="h-16 w-16 rounded-2xl bg-blue-100 flex items-center justify-center mx-auto shadow-sm">
            <MessageSquarePlus className="h-8 w-8 text-blue-600" />
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-slate-900">Welcome to Medi<span className="text-blue-600">Help</span></h2>
          <p className="text-muted-foreground">
            Your AI healthcare assistant is ready to help. Start a conversation to ask questions
            about your health or upload medical reports.
          </p>
        </div>

        <div className="grid gap-4">
          {features.map((feature, i) => (
            <div
              key={i}
              className="flex items-start gap-4 rounded-xl bg-white border border-slate-100 shadow-sm p-4 text-left transition-smooth hover:border-blue-200 hover:bg-blue-50/30"
            >
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-blue-50">
                <feature.icon className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <h3 className="font-medium text-slate-900">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>

        <Button size="lg" onClick={onNewChat} className="gap-2 bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-100">
          <MessageSquarePlus className="h-5 w-5" />
          Start a conversation
        </Button>
      </div>
    </div>
  );
}
