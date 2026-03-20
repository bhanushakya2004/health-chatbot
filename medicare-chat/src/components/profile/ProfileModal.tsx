import { useState, useEffect } from 'react';
import { format } from 'date-fns';
import { X, Upload, FileText, Trash2, RefreshCw, Loader2, CheckCircle, Clock } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Separator } from '@/components/ui/separator';
import { toast } from '@/hooks/use-toast';
import { userService, UserProfile, DocumentResponse, HealthSummaryResponse } from '@/lib/user';

interface ProfileModalProps {
  open: boolean;
  onClose: () => void;
}

export function ProfileModal({ open, onClose }: ProfileModalProps) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [documents, setDocuments] = useState<DocumentResponse[]>([]);
  const [healthSummary, setHealthSummary] = useState<HealthSummaryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);
  
  // Form states
  const [fullName, setFullName] = useState('');
  const [age, setAge] = useState<number | ''>('');
  const [gender, setGender] = useState('');

  useEffect(() => {
    if (open) {
      loadUserData();
    }
  }, [open]);

  const loadUserData = async () => {
    setLoading(true);
    try {
      const [userData, docs, summary] = await Promise.all([
        userService.getCurrentUser(),
        userService.getDocuments(),
        userService.getHealthSummary().catch(() => null),
      ]);

      if (userData) {
        setUser(userData);
        setFullName(userData.full_name || '');
        setAge(userData.age || '');
        setGender(userData.gender || '');
      }
      setDocuments(docs);
      setHealthSummary(summary);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to load profile data',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async () => {
    setLoading(true);
    try {
      const updated = await userService.updateCurrentUser({
        full_name: fullName,
        age: age === '' ? undefined : Number(age),
        gender: gender || undefined,
      });
      setUser(updated);
      toast({
        title: 'Profile updated',
        description: 'Your profile has been saved successfully.',
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update profile',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const doc = await userService.uploadDocument(formData);
      setDocuments([...documents, doc]);
      toast({
        title: 'Document uploaded',
        description: 'Your document is being processed for OCR extraction.',
      });
      event.target.value = '';
    } catch (error) {
      toast({
        title: 'Upload failed',
        description: 'Failed to upload document',
        variant: 'destructive',
      });
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (docId: string) => {
    try {
      await userService.deleteDocument(docId);
      setDocuments(documents.filter(d => d.document_id !== docId));
      toast({
        title: 'Document deleted',
        description: 'Document has been removed successfully.',
      });
    } catch (error) {
      toast({
        title: 'Delete failed',
        description: 'Failed to delete document',
        variant: 'destructive',
      });
    }
  };

  const handleGenerateHealthSummary = async () => {
    setGenerating(true);
    try {
      const summary = await userService.generateHealthSummary();
      setHealthSummary(summary);
      toast({
        title: 'Health summary generated',
        description: 'Your AI health summary has been updated.',
      });
    } catch (error) {
      toast({
        title: 'Generation failed',
        description: 'Failed to generate health summary',
        variant: 'destructive',
      });
    } finally {
      setGenerating(false);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px] max-h-[85vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="text-xl font-semibold">My Profile</DialogTitle>
        </DialogHeader>

        {loading && !user ? (
          <div className="flex justify-center items-center py-8">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : (
          <Tabs defaultValue="profile" className="flex-1 overflow-hidden flex flex-col">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="profile">Profile</TabsTrigger>
              <TabsTrigger value="documents">Documents</TabsTrigger>
              <TabsTrigger value="health">Health Summary</TabsTrigger>
            </TabsList>

            {/* Profile Tab */}
            <TabsContent value="profile" className="flex-1 overflow-y-auto mt-4 space-y-4">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    value={user?.email || ''}
                    disabled
                    className="bg-gray-50"
                  />
                </div>

                <div>
                  <Label htmlFor="fullName">Full Name</Label>
                  <Input
                    id="fullName"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Enter your full name"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="age">Age</Label>
                    <Input
                      id="age"
                      type="number"
                      value={age}
                      onChange={(e) => setAge(e.target.value === '' ? '' : Number(e.target.value))}
                      placeholder="Your age"
                    />
                  </div>

                  <div>
                    <Label htmlFor="gender">Gender</Label>
                    <Select value={gender} onValueChange={setGender}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select gender" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Male">Male</SelectItem>
                        <SelectItem value="Female">Female</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <Separator />

                <div className="flex justify-end">
                  <Button onClick={handleSaveProfile} disabled={loading}>
                    {loading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Saving...
                      </>
                    ) : (
                      'Save Profile'
                    )}
                  </Button>
                </div>
              </div>
            </TabsContent>

            {/* Documents Tab */}
            <TabsContent value="documents" className="flex-1 overflow-y-auto mt-4 space-y-4">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium">Medical Documents</h3>
                  <div className="relative">
                    <input
                      type="file"
                      id="file-upload"
                      className="hidden"
                      accept=".pdf,.jpg,.jpeg,.png"
                      onChange={handleFileUpload}
                      disabled={uploading}
                    />
                    <Button
                      onClick={() => document.getElementById('file-upload')?.click()}
                      disabled={uploading}
                      size="sm"
                    >
                      {uploading ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Uploading...
                        </>
                      ) : (
                        <>
                          <Upload className="mr-2 h-4 w-4" />
                          Upload
                        </>
                      )}
                    </Button>
                  </div>
                </div>

                <Separator />

                {documents.length === 0 ? (
                  <div className="text-center py-8 text-muted-foreground">
                    <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p>No documents uploaded yet</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {documents.map((doc) => (
                      <div
                        key={doc.document_id}
                        className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50"
                      >
                        <div className="flex items-center gap-3 flex-1">
                          <FileText className="h-5 w-5 text-primary" />
                          <div className="flex-1 min-w-0">
                            <p className="font-medium truncate">{doc.filename}</p>
                            <div className="flex items-center gap-2 text-sm text-muted-foreground">
                              <span>{formatFileSize(doc.file_size)}</span>
                              <span>•</span>
                              <span>{format(new Date(doc.uploaded_at), 'MMM d, yyyy')}</span>
                              {doc.processed ? (
                                <>
                                  <span>•</span>
                                  <CheckCircle className="h-3 w-3 text-blue-600" />
                                  <span className="text-blue-600">Processed</span>
                                </>
                              ) : (
                                <>
                                  <span>•</span>
                                  <Clock className="h-3 w-3 text-amber-600" />
                                  <span className="text-amber-600">Processing...</span>
                                </>
                              )}
                            </div>
                          </div>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeleteDocument(doc.document_id)}
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </TabsContent>

            {/* Health Summary Tab */}
            <TabsContent value="health" className="flex-1 overflow-y-auto mt-4 space-y-4">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium">AI Health Summary</h3>
                  <Button
                    onClick={handleGenerateHealthSummary}
                    disabled={generating}
                    size="sm"
                  >
                    {generating ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <RefreshCw className="mr-2 h-4 w-4" />
                        Regenerate
                      </>
                    )}
                  </Button>
                </div>

                <Separator />

                {healthSummary ? (
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium mb-2">Summary</h4>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {healthSummary.summary}
                      </p>
                    </div>

                    {healthSummary.medical_conditions.length > 0 && (
                      <div>
                        <h4 className="font-medium mb-2">Medical Conditions</h4>
                        <div className="flex flex-wrap gap-2">
                          {healthSummary.medical_conditions.map((condition, idx) => (
                            <span
                              key={idx}
                              className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                            >
                              {condition}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="text-xs text-muted-foreground">
                      Last updated: {format(new Date(healthSummary.last_updated), 'PPpp')}
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <RefreshCw className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p className="mb-4">No health summary generated yet</p>
                    <Button onClick={handleGenerateHealthSummary} disabled={generating}>
                      {generating ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Generating...
                        </>
                      ) : (
                        'Generate Health Summary'
                      )}
                    </Button>
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
        )}
      </DialogContent>
    </Dialog>
  );
}
