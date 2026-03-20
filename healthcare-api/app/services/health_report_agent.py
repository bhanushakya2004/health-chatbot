import os
from typing import List, Dict, Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from app.config.database import get_chats_collection, get_documents_collection, get_reports_collection

class HealthReportAgent:
    """Agent for generating comprehensive health summaries from user data"""
    
    @staticmethod
    def get_agent():
        """Initialize the health report generation agent"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not set")
        
        agent = Agent(
            name="Health Report Analyzer",
            model=OpenRouter(id="google/gemini-2.0-flash-001", api_key=api_key),
            instructions=[
                "You are a medical data analyst specialized in creating comprehensive health summaries.",
                "Analyze patient chat history, medical documents, and reports to extract key health information.",
                "Identify medical conditions, symptoms, medications, and health concerns.",
                "Create concise, structured health summaries that can be used as context for consultations.",
                "Extract and categorize: chronic conditions, current symptoms, medications, allergies, lifestyle factors.",
                "Be factual and only include information explicitly mentioned in the data.",
                "Format output as clear, bulleted summaries for easy reference."
            ],
            markdown=True,
        )
        return agent
    
    @staticmethod
    def fetch_user_chats(user_id: str, limit: int = 50) -> List[Dict]:
        """Fetch recent chat messages for user"""
        chats_collection = get_chats_collection()
        chats = list(chats_collection.find(
            {"user_id": user_id}
        ).sort("updated_at", -1).limit(limit))
        
        all_messages = []
        for chat in chats:
            for msg in chat.get("messages", []):
                all_messages.append({
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"]
                })
        
        return all_messages
    
    @staticmethod
    def fetch_user_documents(user_id: str) -> List[Dict]:
        """Fetch user's medical documents with extracted text"""
        documents_collection = get_documents_collection()
        docs = list(documents_collection.find(
            {"user_id": user_id, "processed": True}
        ))
        
        return [{
            "filename": doc["filename"],
            "description": doc.get("description", ""),
            "extracted_text": doc.get("extracted_text", ""),
            "uploaded_at": doc["uploaded_at"]
        } for doc in docs]
    
    @staticmethod
    def fetch_user_reports(user_id: str) -> List[Dict]:
        """Fetch user's medical reports"""
        reports_collection = get_reports_collection()
        reports = list(reports_collection.find({"user_id": user_id}))
        
        return [{
            "report_type": report.get("report_type", ""),
            "findings": report.get("findings", ""),
            "diagnosis": report.get("diagnosis", ""),
            "created_at": report.get("created_at", "")
        } for report in reports]
    
    @staticmethod
    def generate_health_summary(user_id: str) -> Dict[str, any]:
        """
        Generate comprehensive health summary for user
        
        Returns:
            Dictionary with health_summary and extracted medical_conditions
        """
        agent = HealthReportAgent.get_agent()
        
        # Gather all user data
        chats = HealthReportAgent.fetch_user_chats(user_id)
        documents = HealthReportAgent.fetch_user_documents(user_id)
        reports = HealthReportAgent.fetch_user_reports(user_id)
        
        # Build analysis prompt
        prompt = f"""Analyze the following patient data and create a comprehensive health summary:

## Chat History ({len(chats)} messages):
"""
        for msg in chats[:30]:  # Limit to recent 30 messages
            prompt += f"- [{msg['role']}]: {msg['content'][:200]}...\n"
        
        prompt += f"\n## Medical Documents ({len(documents)} files):\n"
        for doc in documents:
            prompt += f"- {doc['filename']}: {doc['extracted_text'][:500]}...\n"
        
        prompt += f"\n## Medical Reports ({len(reports)} reports):\n"
        for report in reports:
            prompt += f"- Type: {report['report_type']}, Findings: {report['findings'][:300]}...\n"
        
        prompt += """

Based on this data, provide:
1. **Health Summary**: A concise 3-5 sentence overview of the patient's health status
2. **Medical Conditions**: List of identified chronic or current conditions
3. **Current Symptoms**: Any ongoing symptoms mentioned
4. **Medications**: List of medications mentioned
5. **Key Health Concerns**: Important issues to be aware of

Format as structured markdown."""
        
        # Generate summary
        response = agent.run(prompt)
        summary_text = response.content if hasattr(response, 'content') else str(response)
        
        # Extract conditions (simple extraction)
        conditions = []
        if "diabetes" in summary_text.lower():
            conditions.append("Diabetes")
        if "hypertension" in summary_text.lower():
            conditions.append("Hypertension")
        if "asthma" in summary_text.lower():
            conditions.append("Asthma")
        if "arthritis" in summary_text.lower():
            conditions.append("Arthritis")
        
        return {
            "health_summary": summary_text,
            "medical_conditions": conditions
        }
