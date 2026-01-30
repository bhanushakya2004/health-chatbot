import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from app.utils.tools import get_patient_info, get_patient_reports, get_latest_report

load_dotenv()

class HealthcareAgentService:
    _agent = None
    
    @classmethod
    def get_agent(cls):
        """Get or create healthcare agent instance"""
        if cls._agent is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not set. Please set the GOOGLE_API_KEY environment variable.")
            
            cls._agent = Agent(
                name="Health Consultant",
                model=Gemini(id="gemini-2.5-flash", api_key=api_key),
                tools=[get_patient_info, get_patient_reports, get_latest_report],
                instructions=[
                    "You are a professional health consultant.",
                    "Fetch patient data and reports using the provided tools.",
                    "Provide health advice based on the patient's medical history.",
                    "Always recommend consulting a doctor for serious concerns.",
                ],
                markdown=True,
            )
        return cls._agent
    
    @classmethod
    def get_response(cls, query: str) -> str:
        """Get response from healthcare agent"""
        agent = cls.get_agent()
        response = agent.run(query)
        return response.content if hasattr(response, 'content') else str(response)
