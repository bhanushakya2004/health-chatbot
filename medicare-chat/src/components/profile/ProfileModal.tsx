import { useState } from 'react';
import { format } from 'date-fns';
import { X, Upload, FileText, ImageIcon, Trash2, Calendar, User, Mail } from 'lucide-react';
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
import { UserProfile, MedicalRecord } from '@/types/chat';
import { toast } from '@/hooks/use-toast';
import { cn } from '@/lib/utils';

interface ProfileModalProps {
  open: boolean;
  onClose: () => void;
  user: UserProfile;
  records: MedicalRecord[];
  onUpdateUser: (user: UserProfile) => void;
  onAddRecord: (record: MedicalRecord) => void;
  onDeleteRecord: (id: string) => void;
}

export function ProfileModal({
  open,
  onClose,
  user,
  records,
  onUpdateUser,
  onAddRecord,
  onDeleteRecord,
}: ProfileModalProps) {
  const [editedUser, setEditedUser] = useState(user);
  const [newRecordName, setNewRecordName] = useState('');
  const [newRecordDate, setNewRecordDate] = useState('');

  const handleSaveProfile = () => {
    onUpdateUser(editedUser);
    toast({
      title: 'Profile updated',
      description: 'Your profile has been saved successfully.',
    });
  };

  const handleFileUpload = () => {
    if (!newRecordName || !newRecordDate) {
      toast({
        title: 'Missing information',
        description: 'Please provide both a name and date for the record.',
        variant: 'destructive',
      });
      return;
    }

    const newRecord: MedicalRecord = {
      id: Date.now().toString(),
      name: newRecordName,
      date: new Date(newRecordDate),
      fileType: 'pdf',
      size: '125 KB',
    };

    onAddRecord(newRecord);
    setNewRecordName('');
    setNewRecordDate('');
    toast({
      title: 'Record uploaded',
      description: 'Your medical record has been added successfully.',
    });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px] max-h-[85vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="text-xl font-semibold">Patient Profile</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="profile" className="flex-1 overflow-hidden flex flex-col">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="profile">Profile</TabsTrigger>
            <TabsTrigger value="records">Medical Records</TabsTrigger>
          </TabsList>

          <TabsContent value="profile" className="flex-1 overflow-y-auto mt-4 space-y-6">
            {/* Avatar Section */}
            <div className="flex items-center gap-4">
              <div className="h-20 w-20 rounded-full bg-primary/10 flex items-center justify-center">
                <User className="h-10 w-10 text-primary" />
              </div>
              <Button variant="outline" size="sm">
                <Upload className="h-4 w-4 mr-2" />
                Upload Photo
              </Button>
            </div>

            <Separator />

            {/* Profile Form */}
            <div className="grid gap-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  value={editedUser.name}
                  onChange={(e) => setEditedUser({ ...editedUser, name: e.target.value })}
                  placeholder="Enter your full name"
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={editedUser.email}
                  onChange={(e) => setEditedUser({ ...editedUser, email: e.target.value })}
                  placeholder="Enter your email"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="age">Age</Label>
                  <Input
                    id="age"
                    type="number"
                    value={editedUser.age}
                    onChange={(e) => setEditedUser({ ...editedUser, age: parseInt(e.target.value) || 0 })}
                    placeholder="Age"
                  />
                </div>

                <div className="grid gap-2">
                  <Label htmlFor="gender">Gender</Label>
                  <Select
                    value={editedUser.gender}
                    onValueChange={(value: 'male' | 'female' | 'other') =>
                      setEditedUser({ ...editedUser, gender: value })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select gender" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Male</SelectItem>
                      <SelectItem value="female">Female</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button onClick={handleSaveProfile} className="mt-2">
                Save Profile
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="records" className="flex-1 overflow-y-auto mt-4 space-y-6">
            {/* Upload New Record */}
            <div className="rounded-xl border border-dashed border-border p-4 space-y-4">
              <h3 className="font-medium">Upload New Record</h3>
              <div className="grid gap-3">
                <Input
                  placeholder="Report name (e.g., Blood Test Results)"
                  value={newRecordName}
                  onChange={(e) => setNewRecordName(e.target.value)}
                />
                <div className="flex gap-2">
                  <Input
                    type="date"
                    value={newRecordDate}
                    onChange={(e) => setNewRecordDate(e.target.value)}
                    className="flex-1"
                  />
                  <Button onClick={handleFileUpload}>
                    <Upload className="h-4 w-4 mr-2" />
                    Upload
                  </Button>
                </div>
              </div>
            </div>

            <Separator />

            {/* Records List */}
            <div className="space-y-3">
              <h3 className="font-medium">Your Records</h3>
              {records.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">
                  <FileText className="h-12 w-12 mx-auto mb-3 opacity-50" />
                  <p>No medical records uploaded yet.</p>
                </div>
              ) : (
                <div className="space-y-2">
                  {records.map((record) => (
                    <div
                      key={record.id}
                      className="flex items-center gap-3 rounded-lg border border-border p-3 hover:bg-muted/50 transition-smooth"
                    >
                      {record.fileType === 'pdf' ? (
                        <FileText className="h-8 w-8 text-destructive shrink-0" />
                      ) : (
                        <ImageIcon className="h-8 w-8 text-health-info shrink-0" />
                      )}
                      <div className="flex-1 min-w-0">
                        <p className="font-medium truncate">{record.name}</p>
                        <p className="text-sm text-muted-foreground">
                          {format(record.date, 'MMM d, yyyy')} • {record.size}
                        </p>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="shrink-0 hover:bg-destructive/20 hover:text-destructive"
                        onClick={() => {
                          onDeleteRecord(record.id);
                          toast({
                            title: 'Record deleted',
                            description: 'The medical record has been removed.',
                          });
                        }}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
