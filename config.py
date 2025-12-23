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
    
    # Gmail OAuth2 Configuration
    # These will be populated from the GMAIL_CREDENTIALS JSON in Kestra
    GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
    GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
    GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")
    
    # Email Addresses
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
    
    # Agent Configuration
    MODEL_NAME = "gemini-3-flash-preview"
    MAX_SEARCH_RESULTS = 10
    
    # Report Configuration
    REPORT_TITLE = "Daily AI & Automation News Report"
    REPORT_FILENAME = "ai_news_report.pdf"
    
    # Validation
    @classmethod
    def validate(cls):
        """
        Validate that all required environment variables are set.
        Checks for either basic auth (user/pass) or OAuth2 credentials.
        """
        required_common = {
            "GOOGLE_API_KEY": cls.GOOGLE_API_KEY,
            "TAVILY_API_KEY": cls.TAVILY_API_KEY,
            "RECEIVER_EMAIL": cls.RECEIVER_EMAIL,
        }
        
        # Check common vars
        missing_vars = [var for var, value in required_common.items() if not value]
        
        # Check OAuth2 vars
        required_oauth = {
            "GMAIL_CLIENT_ID": cls.GMAIL_CLIENT_ID,
            "GMAIL_CLIENT_SECRET": cls.GMAIL_CLIENT_SECRET,
            "GMAIL_REFRESH_TOKEN": cls.GMAIL_REFRESH_TOKEN,
        }
        
        missing_oauth = [var for var, value in required_oauth.items() if not value]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
            
        if missing_oauth:
             raise ValueError(
                f"Missing required OAuth2 environment variables: {', '.join(missing_oauth)}"
            )
        
        return True
