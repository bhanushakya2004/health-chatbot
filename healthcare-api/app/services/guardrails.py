"""
Guardrails for the healthcare agent.
Implements safety checks, prompt injection detection, and content filtering.
"""
import re
from typing import Tuple, Optional
from app.utils.logger import warning


# Prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above|prior)\s+(instructions|prompts|commands)",
    r"disregard\s+(previous|all|above|prior)",
    r"forget\s+(everything|all|previous)",
    r"new\s+instructions?:",
    r"system\s*:\s*you\s+are",
    r"<\|im_start\|>",
    r"<\|endoftext\|>",
    r"###\s*(instruction|system)",
    r"\\n\\n(human|assistant):",
]

# Sensitive topics that require careful handling
SENSITIVE_TOPICS = [
    "suicide", "self-harm", "kill myself", "end my life",
    "overdose", "poison", "harmful substance",
    "abuse", "violence", "weapon"
]

# Emergency keywords
EMERGENCY_KEYWORDS = [
    "chest pain", "heart attack", "stroke", "can't breathe",
    "difficulty breathing", "severe bleeding", "unconscious",
    "severe head injury", "seizure", "allergic reaction"
]


class PromptGuardrail:
    """Guardrail for detecting and handling unsafe prompts"""
    
    @staticmethod
    def detect_injection(text: str) -> Tuple[bool, Optional[str]]:
        """
        Detect prompt injection attempts.
        Returns: (is_injection, reason)
        """
        text_lower = text.lower()
        
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                warning(f"Prompt injection detected: {pattern}")
                return True, f"Potential prompt injection detected"
        
        return False, None
    
    @staticmethod
    def detect_sensitive_topic(text: str) -> Tuple[bool, str]:
        """
        Detect sensitive topics requiring special handling.
        Returns: (is_sensitive, topic)
        """
        text_lower = text.lower()
        
        for topic in SENSITIVE_TOPICS:
            if topic in text_lower:
                warning(f"Sensitive topic detected: {topic}")
                return True, topic
        
        return False, None
    
    @staticmethod
    def detect_emergency(text: str) -> Tuple[bool, str]:
        """
        Detect emergency situations.
        Returns: (is_emergency, keyword)
        """
        text_lower = text.lower()
        
        for keyword in EMERGENCY_KEYWORDS:
            if keyword in text_lower:
                warning(f"Emergency keyword detected: {keyword}")
                return True, keyword
        
        return False, None
    
    @staticmethod
    def validate_input(text: str) -> Tuple[bool, Optional[str], Optional[dict]]:
        """
        Comprehensive input validation.
        Returns: (is_valid, error_message, metadata)
        """
        if not text or not text.strip():
            return False, "Empty input", None
        
        if len(text) > 5000:
            return False, "Input too long (max 5000 characters)", None
        
        # Check for injection
        is_injection, injection_reason = PromptGuardrail.detect_injection(text)
        if is_injection:
            return False, "Input contains prohibited content", {"type": "injection"}
        
        # Check for sensitive topics
        is_sensitive, sensitive_topic = PromptGuardrail.detect_sensitive_topic(text)
        
        # Check for emergency
        is_emergency, emergency_keyword = PromptGuardrail.detect_emergency(text)
        
        metadata = {
            "is_sensitive": is_sensitive,
            "sensitive_topic": sensitive_topic if is_sensitive else None,
            "is_emergency": is_emergency,
            "emergency_keyword": emergency_keyword if is_emergency else None,
        }
        
        return True, None, metadata


class ResponseGuardrail:
    """Guardrail for validating agent responses"""
    
    @staticmethod
    def validate_response(response: str) -> Tuple[bool, Optional[str]]:
        """
        Validate agent response for safety.
        Returns: (is_valid, error_message)
        """
        if not response or not response.strip():
            return False, "Empty response"
        
        # Check for excessive length
        if len(response) > 10000:
            warning("Response too long, truncating")
            return True, None  # Valid but should be truncated
        
        # Check if response refuses to act as medical professional (good)
        refusal_phrases = [
            "i cannot diagnose",
            "i'm not a doctor",
            "consult a healthcare professional",
            "see a doctor"
        ]
        
        response_lower = response.lower()
        
        # For sensitive topics, ensure appropriate disclaimers
        has_appropriate_disclaimer = any(phrase in response_lower for phrase in refusal_phrases)
        
        return True, None
    
    @staticmethod
    def add_emergency_response(response: str) -> str:
        """Add emergency warning to response"""
        emergency_prefix = """
⚠️ **EMERGENCY ALERT** ⚠️

Based on your description, this may be a medical emergency.

**IMMEDIATE ACTION REQUIRED:**
- Call emergency services (911 in US) NOW
- Do not wait for symptoms to worsen
- If alone, call someone to stay with you
- Do not drive yourself to the hospital

**Original Response (for reference only):**

"""
        return emergency_prefix + response
    
    @staticmethod
    def add_sensitive_topic_disclaimer(response: str, topic: str) -> str:
        """Add disclaimer for sensitive topics"""
        if "suicide" in topic or "self-harm" in topic:
            disclaimer = """
⚠️ **Important Resources**

If you're experiencing thoughts of self-harm or suicide, please reach out immediately:
- **National Suicide Prevention Lifeline**: 988 or 1-800-273-8255
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

You are not alone, and help is available 24/7.

---

"""
            return disclaimer + response
        
        return response


class ToolCallLimiter:
    """Limit tool calls to prevent runaway operations"""
    
    def __init__(self, max_calls_per_conversation: int = 10):
        self.max_calls = max_calls_per_conversation
        self.call_counts = {}
    
    def can_call_tool(self, session_id: str) -> Tuple[bool, int]:
        """
        Check if tool call is allowed.
        Returns: (allowed, remaining_calls)
        """
        current_count = self.call_counts.get(session_id, 0)
        
        if current_count >= self.max_calls:
            warning(f"Tool call limit reached for session {session_id}")
            return False, 0
        
        return True, self.max_calls - current_count
    
    def increment_call(self, session_id: str):
        """Increment tool call counter"""
        self.call_counts[session_id] = self.call_counts.get(session_id, 0) + 1
    
    def reset_session(self, session_id: str):
        """Reset counter for a session"""
        if session_id in self.call_counts:
            del self.call_counts[session_id]


# Global tool limiter instance
tool_limiter = ToolCallLimiter(max_calls_per_conversation=15)
