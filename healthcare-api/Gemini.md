# Healthcare Consultant API - Gemini Integration

## Overview

The AI-powered health consultation feature of this API is deeply integrated with **Google Gemini** models, specifically using the `gemini-2.0-flash-001` model for its conversational capabilities. This integration is managed through the `agno` AI agent framework, which orchestrates interactions with the Gemini model and provides it with access to various tools for retrieving patient data.

## Key Components

### 1. `agno` Agent Framework

The `agno` library is used to define and manage the AI agent. It encapsulates the Gemini model, a set of defined tools, and a clear instruction set for the agent's behavior.

*   **Agent Definition:** The `HealthcareAgentService` (`app/services/agent_service.py`) initializes an `Agent` instance with:
    *   `name`: "Health Consultant"
    *   `model`: An instance of `agno.models.google.Gemini`, configured with `gemini-2.0-flash-001` and the `GOOGLE_API_KEY`.
    *   `tools`: A list of functions (e.g., `get_patient_info`, `get_patient_reports`, `get_latest_report`) that the Gemini model can call to interact with the MongoDB database and retrieve relevant patient data.
    *   `instructions`: A set of directives guiding the agent's persona and responsibilities.

### 2. Gemini Model Configuration

The Gemini model is configured within `app/services/agent_service.py`. It requires the `GOOGLE_API_KEY` for authentication.

*   **Environment Variable:** The `GOOGLE_API_KEY` must be set as an environment variable. When running locally, it's loaded from the `.env` file in the `healthcare-api` directory. When running with Docker Compose, it's passed as an environment variable to the backend service.

### 3. Tools for Data Access

The agent uses several tools to access and interpret patient data stored in MongoDB. These tools are Python functions that the Gemini model can invoke (via `agno`) to perform specific actions like fetching patient information or reports. This allows the AI to provide context-aware responses without directly accessing the database itself.

## API Endpoints for Chat

The chat functionality is exposed through the following API endpoints, now supporting chat history persistence:

*   **GET /chats/**
    *   Description: Get all chat history summaries for the current user, ordered by most recently updated.
    *   Response: `List[ChatHistoryResponse]`

*   **GET /chats/{chat_id}**
    *   Description: Retrieve the full conversation for a specific chat ID.
    *   Response: `Chat` (includes all messages in the conversation)

*   **POST /chats/**
    *   Description: Create a new chat. Initiates a conversation with an initial user message and receives an immediate AI response.
    *   Request Body: `ChatCreate` (e.g., `{"title": "New Consultation", "message": "What are common symptoms of flu?"}`)
    *   Response: `ChatResponse` (details of the newly created chat)

*   **POST /chats/{chat_id}/messages**
    *   Description: Add a new user message to an existing chat and get an AI response.
    *   Request Body: `ChatMessageRequest` (e.g., `{"content": "Tell me more about treatment."}`)
    *   Response: `Message` (the AI's response message)

*   **DELETE /chats/{chat_id}**
    *   Description: Delete an entire chat conversation.
    *   Response: `204 No Content`

## Setup and Environment

To enable Gemini integration, ensure your `GOOGLE_API_KEY` is correctly configured:

*   **Local Development:** Create a `.env` file in `healthcare-api/` and add `GOOGLE_API_KEY=your_gemini_api_key`.
*   **Docker Compose:** The `docker-compose.yml` file is configured to pass the `GOOGLE_API_KEY` from your host environment to the backend container.

Without a valid `GOOGLE_API_KEY`, the AI chat functionality will not work, and attempts to create or add messages to chats will result in a `500 Internal Server Error` due to the missing API key.
