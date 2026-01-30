from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Message(BaseModel):
    id: str = Field(default_factory=lambda: f"M{uuid.uuid4().hex[:8].upper()}")
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class Chat(BaseModel):
    id: str = Field(default_factory=lambda: f"C{uuid.uuid4().hex[:8].upper()}")
    user_id: str
    title: str
    messages: List[Message]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class ChatCreate(BaseModel):
    title: str
    message: str

class ChatResponse(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime

class ChatHistoryResponse(BaseModel):
    id: str
    title: str
    updated_at: datetime
    last_message: Optional[str]

class ChatMessageRequest(BaseModel):
    content: str

