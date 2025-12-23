"""
Configuration management for the AI News Agent.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Configuration class for managing environment variables and settings."""
    

    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Discord Webhook Configuration
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    
    # Agent Configuration
    MODEL_NAME = "models/gemini-2.5-flash"
    MAX_SEARCH_RESULTS = 10
    
    # Report Configuration
    REPORT_TITLE = "Daily AI & Automation News Report"
    REPORT_FILENAME = "ai_news_report.pdf"
    
    # Validation
    @classmethod
    def validate(cls):
        """
        Validate that all required environment variables are set.
        """
        required_vars = {
            "GOOGLE_API_KEY": cls.GOOGLE_API_KEY,
            "TAVILY_API_KEY": cls.TAVILY_API_KEY,
            "DISCORD_WEBHOOK_URL": cls.DISCORD_WEBHOOK_URL,
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        return True
