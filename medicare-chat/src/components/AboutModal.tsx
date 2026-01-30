import { Heart, Shield, AlertCircle, Lock } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Separator } from '@/components/ui/separator';

interface AboutModalProps {
  open: boolean;
  onClose: () => void;
}

export function AboutModal({ open, onClose }: AboutModalProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary">
              <Heart className="h-5 w-5 text-primary-foreground" fill="currentColor" />
            </div>
            <DialogTitle className="text-xl font-semibold">About MediHelp</DialogTitle>
          </div>
        </DialogHeader>

        <div className="space-y-5 py-2">
          <p className="text-muted-foreground leading-relaxed">
            MediHelp is an AI-powered healthcare assistant designed to help patients understand 
            health information, review reports, and organize medical history.
          </p>

          <Separator />

          <div className="space-y-4">
            <h3 className="font-semibold flex items-center gap-2">
              <Shield className="h-4 w-4 text-primary" />
              What MediHelp Can Help With
            </h3>
            <ul className="space-y-2 text-sm text-muted-foreground ml-6">
              <li className="flex items-start gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-primary mt-2 shrink-0" />
                Answer general health-related questions
              </li>
              <li className="flex items-start gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-primary mt-2 shrink-0" />
                Help you understand medical reports and terminology
              </li>
              <li className="flex items-start gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-primary mt-2 shrink-0" />
                Organize and store your medical records
              </li>
              <li className="flex items-start gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-primary mt-2 shrink-0" />
                Provide health information and resources
              </li>
            </ul>
          </div>

          <Separator />

          <div className="rounded-lg bg-destructive/10 p-4 border border-destructive/20">
            <h3 className="font-semibold flex items-center gap-2 text-destructive">
              <AlertCircle className="h-4 w-4" />
              Important Disclaimer
            </h3>
            <p className="text-sm text-muted-foreground mt-2">
              MediHelp does not provide medical diagnoses, treatment recommendations, or 
              replace professional medical advice. Always consult a qualified healthcare 
              provider for medical concerns.
            </p>
          </div>

          <div className="rounded-lg bg-muted p-4">
            <h3 className="font-semibold flex items-center gap-2 text-sm">
              <Lock className="h-4 w-4 text-primary" />
              Privacy & Data
            </h3>
            <p className="text-sm text-muted-foreground mt-2">
              Your health data is stored securely and never shared with third parties. 
              You maintain full control over your medical records.
            </p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
