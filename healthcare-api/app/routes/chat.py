from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import StreamingResponse
from typing import List
from app.dependencies import get_current_user
from app.models.user import UserResponse
from app.models.chat import (
    Chat,
    Message,
    ChatCreate,
    ChatResponse,
    ChatHistoryResponse,
    ChatMessageRequest,
)
from app.config.database import get_chats_collection
from app.services.agent_service import HealthcareAgentService
from datetime import datetime
import uuid
import json

router = APIRouter(prefix="/chats", tags=["Chat"])


@router.get("/", response_model=List[ChatHistoryResponse])
async def get_chat_history(current_user: UserResponse = Depends(get_current_user)):
    """
    Get all chat history for the current user.
    """
    chats_collection = get_chats_collection()
    chats = chats_collection.find({"user_id": current_user["user_id"]}).sort(
        "updated_at", -1
    )
    history = []
    for chat in chats:
        last_message = chat["messages"][-1]["content"] if chat["messages"] else None
        history.append(
            ChatHistoryResponse(
                id=chat["id"],
                title=chat["title"],
                updated_at=chat["updated_at"],
                last_message=last_message,
            )
        )
    return history


@router.get("/{chat_id}", response_model=Chat)
async def get_chat(chat_id: str, current_user: UserResponse = Depends(get_current_user)):
    """
    Get a specific chat by its ID.
    """
    chats_collection = get_chats_collection()
    chat = chats_collection.find_one(
        {"id": chat_id, "user_id": current_user["user_id"]}
    )
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    return Chat(**chat)


@router.post("/", response_model=Chat, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_create: ChatCreate, current_user: UserResponse = Depends(get_current_user)
):
    """
    Create a new chat.
    """
    chats_collection = get_chats_collection()
    chat_id = f"C{uuid.uuid4().hex[:8].upper()}"
    
    user_message = Message(
        id=f"M{uuid.uuid4().hex[:8].upper()}",
        role="user",
        content=chat_create.message,
        timestamp=datetime.now(),
    )
    
    assistant_response_content = HealthcareAgentService.get_response(
        query=chat_create.message,
        session_id=chat_id,
        user_id=current_user["user_id"]
    )
    
    assistant_message = Message(
        id=f"M{uuid.uuid4().hex[:8].upper()}",
        role="assistant",
        content=assistant_response_content,
        timestamp=datetime.now(),
    )
    
    chat = Chat(
        id=chat_id,
        user_id=current_user["user_id"],
        title=chat_create.title,
        messages=[user_message, assistant_message],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    chats_collection.insert_one(chat.model_dump())
    return chat


@router.post("/{chat_id}/messages", response_model=Message)
async def add_message_to_chat(
    chat_id: str,
    message_request: ChatMessageRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Add a new message to an existing chat (non-streaming).
    """
    chats_collection = get_chats_collection()
    chat = chats_collection.find_one(
        {"id": chat_id, "user_id": current_user["user_id"]}
    )
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    
    user_message = Message(
        id=f"M{uuid.uuid4().hex[:8].upper()}",
        role="user",
        content=message_request.content,
        timestamp=datetime.now(),
    )
    
    assistant_response_content = HealthcareAgentService.get_response(
        query=message_request.content,
        session_id=chat_id,
        user_id=current_user["user_id"]
    )
    
    assistant_message = Message(
        id=f"M{uuid.uuid4().hex[:8].upper()}",
        role="assistant",
        content=assistant_response_content,
        timestamp=datetime.now(),
    )
    
    chats_collection.update_one(
        {"id": chat_id},
        {
            "$push": {"messages": {"$each": [user_message.model_dump(), assistant_message.model_dump()]}},
            "$set": {"updated_at": datetime.now()},
        },
    )
    return assistant_message


@router.post("/{chat_id}/stream")
async def stream_chat_message(
    chat_id: str,
    message_request: ChatMessageRequest,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Add a message and stream the assistant's response using Server-Sent Events.
    """
    chats_collection = get_chats_collection()
    chat = chats_collection.find_one(
        {"id": chat_id, "user_id": current_user["user_id"]}
    )
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    
    user_message = Message(
        id=f"M{uuid.uuid4().hex[:8].upper()}",
        role="user",
        content=message_request.content,
        timestamp=datetime.now(),
    )
    
    # Save user message immediately
    chats_collection.update_one(
        {"id": chat_id},
        {
            "$push": {"messages": user_message.model_dump()},
            "$set": {"updated_at": datetime.now()},
        },
    )
    
    async def generate_stream():
        full_content = ""
        assistant_message_id = f"M{uuid.uuid4().hex[:8].upper()}"
        
        try:
            # Stream response from agent
            stream = HealthcareAgentService.get_response_stream(
                query=message_request.content,
                session_id=chat_id,
                user_id=current_user["user_id"]
            )
            
            for chunk in stream:
                if hasattr(chunk, 'content') and chunk.content:
                    content = chunk.content
                    full_content += content
                    
                    # Send SSE formatted data
                    yield f"data: {json.dumps({'content': content, 'done': False})}\n\n"
            
            # Save complete assistant message to database
            assistant_message = Message(
                id=assistant_message_id,
                role="assistant",
                content=full_content,
                timestamp=datetime.now(),
            )
            
            chats_collection.update_one(
                {"id": chat_id},
                {
                    "$push": {"messages": assistant_message.model_dump()},
                    "$set": {"updated_at": datetime.now()},
                },
            )
            
            # Send completion signal
            yield f"data: {json.dumps({'content': '', 'done': True, 'message_id': assistant_message_id})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'done': True})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: str, current_user: UserResponse = Depends(get_current_user)
):
    """
    Delete a chat by its ID.
    """
    chats_collection = get_chats_collection()
    result = chats_collection.delete_one(
        {"id": chat_id, "user_id": current_user["user_id"]}
    )
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    return None