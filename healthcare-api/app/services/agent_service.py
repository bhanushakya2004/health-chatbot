# agent_service.py
import os
from typing import AsyncIterator
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.db.mongo import MongoDb
from agno.tools.duckduckgo import DuckDuckGoTools
from app.utils.tools import get_patient_info, get_patient_reports, get_latest_report
from app.services.context_builder import ContextBuilderService
from app.services.prompts import HEALTHCARE_AGENT_SYSTEM_PROMPT, build_enhanced_prompt, FEW_SHOT_EXAMPLES
from app.services.guardrails import PromptGuardrail, ResponseGuardrail, tool_limiter
from app.config.database import get_users_collection
from app.utils.logger import info, warning, error as log_error
from app.exceptions import ServiceError, ValidationError


class HealthcareAgentService:
    _agent = None
    
    @classmethod
    def get_agent(cls):
        if cls._agent is None:
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY not set")
            
            try:
                # MongoDB for session & memory persistence
                db = MongoDb(
                    db_url=os.getenv("MONGODB_URL", "mongodb://mongo:27017"),
                    db_name="healthcare_db",
                    session_collection="agent_sessions",
                )
                
                cls._agent = Agent(
                    name="Health Consultant",
                    model=OpenRouter(id="google/gemini-2.0-flash-001", api_key=api_key),
                    tools=[
                        get_patient_info, 
                        get_patient_reports, 
                        get_latest_report,
                        DuckDuckGoTools(),
                    ],
                    instructions=[HEALTHCARE_AGENT_SYSTEM_PROMPT],
                    # Session & Memory
                    db=db,
                    add_history_to_context=True,
                    num_history_runs=5,
                    update_memory_on_run=True,
                    markdown=True,
                )
                
                info("Healthcare agent initialized successfully with OpenRouter")
            except Exception as e:
                log_error(f"Failed to initialize agent: {str(e)}", exc_info=True)
                raise ServiceError("Failed to initialize AI service", details={"error": str(e)})
        
        return cls._agent
    
    @classmethod
    def _get_user_health_summary(cls, user_id: str) -> tuple:
        """Fetch user's health summary and profile from database"""
        try:
            users_collection = get_users_collection()
            user = users_collection.find_one({"user_id": user_id})
            
            if user:
                return (
                    user.get("health_summary"),
                    user.get("age"),
                    user.get("gender")
                )
            
            return None, None, None
        except Exception as e:
            log_error(f"Failed to fetch user health summary: {str(e)}", exc_info=True)
            return None, None, None
    
    @classmethod
    def _validate_and_enhance_query(cls, query: str, user_id: str) -> tuple:
        """
        Validate input and build enhanced query with context.
        Returns: (enhanced_query, metadata)
        """
        # Validate input with guardrails
        is_valid, error_msg, metadata = PromptGuardrail.validate_input(query)
        
        if not is_valid:
            raise ValidationError(error_msg, details=metadata or {})
        
        # Get user health data
        health_summary, age, gender = cls._get_user_health_summary(user_id)
        
        # Search for relevant documents
        relevant_docs = ContextBuilderService.search_relevant_documents(
            query=query,
            user_id=user_id,
            n_results=3
        )
        
        # Build enhanced prompt
        enhanced_query = build_enhanced_prompt(
            user_query=query,
            health_summary=health_summary,
            relevant_docs=relevant_docs,
            age=age,
            gender=gender
        )
        
        info(f"Enhanced query for user {user_id}, emergency={metadata.get('is_emergency')}, sensitive={metadata.get('is_sensitive')}")
        
        return enhanced_query, metadata
    
    @classmethod
    def _post_process_response(cls, response: str, metadata: dict) -> str:
        """Post-process response with guardrails"""
        # Validate response
        is_valid, error_msg = ResponseGuardrail.validate_response(response)
        
        if not is_valid:
            warning(f"Response validation failed: {error_msg}")
            response = "I apologize, but I couldn't generate an appropriate response. Please try rephrasing your question."
        
        # Add emergency alert if needed
        if metadata.get('is_emergency'):
            response = ResponseGuardrail.add_emergency_response(response)
        
        # Add sensitive topic disclaimer if needed
        if metadata.get('is_sensitive'):
            topic = metadata.get('sensitive_topic', '')
            response = ResponseGuardrail.add_sensitive_topic_disclaimer(response, topic)
        
        return response
    
    @classmethod
    def get_response_stream(cls, query: str, session_id: str, user_id: str):
        """Stream response from healthcare agent with context and guardrails"""
        try:
            # Check tool call limits
            can_call, remaining = tool_limiter.can_call_tool(session_id)
            if not can_call:
                raise ValidationError(
                    "Tool call limit reached. Please start a new conversation.",
                    details={"remaining_calls": 0}
                )
            
            # Validate and enhance query
            enhanced_query, metadata = cls._validate_and_enhance_query(query, user_id)
            
            # Get agent
            agent = cls.get_agent()
            
            # Increment tool call counter
            tool_limiter.increment_call(session_id)
            
            info(f"Streaming response for user {user_id}, session {session_id}")
            
            # Stream response
            response_stream = agent.run(
                enhanced_query, 
                stream=True, 
                session_id=session_id, 
                user_id=user_id
            )
            
            # Collect full response for post-processing
            full_response = []
            for chunk in response_stream:
                full_response.append(chunk)
                yield chunk
            
            # Post-process complete response (for metadata handling)
            complete_response = "".join(full_response)
            processed = cls._post_process_response(complete_response, metadata)
            
            # If post-processing added warnings, yield them
            if processed != complete_response:
                additional_content = processed[:len(processed) - len(complete_response)]
                if additional_content:
                    yield additional_content
            
        except ValidationError:
            raise
        except Exception as e:
            log_error(f"Error in stream response: {str(e)}", exc_info=True)
            raise ServiceError("Failed to generate response", details={"error": str(e)})
    
    @classmethod
    def get_response(cls, query: str, session_id: str, user_id: str) -> str:
        """Non-streaming response with context and guardrails"""
        try:
            # Check tool call limits
            can_call, remaining = tool_limiter.can_call_tool(session_id)
            if not can_call:
                raise ValidationError(
                    "Tool call limit reached. Please start a new conversation.",
                    details={"remaining_calls": 0}
                )
            
            # Validate and enhance query
            enhanced_query, metadata = cls._validate_and_enhance_query(query, user_id)
            
            # Get agent
            agent = cls.get_agent()
            
            # Increment tool call counter
            tool_limiter.increment_call(session_id)
            
            info(f"Getting response for user {user_id}, session {session_id}")
            
            # Get response
            response = agent.run(enhanced_query, session_id=session_id, user_id=user_id)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Post-process response
            processed_response = cls._post_process_response(response_text, metadata)
            
            return processed_response
            
        except ValidationError:
            raise
        except Exception as e:
            log_error(f"Error in get response: {str(e)}", exc_info=True)
            raise ServiceError("Failed to generate response", details={"error": str(e)})
