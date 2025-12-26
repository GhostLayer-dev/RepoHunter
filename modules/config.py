"""
RepoHunter - Configuration Management
Handles API keys and environment configuration.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration manager for RepoHunter."""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.github_token = os.getenv("GITHUB_TOKEN", "")  # Optional
    
    def validate(self) -> tuple[bool, str]:
        """Validate required configuration."""
        if not self.groq_api_key:
            return False, "GROQ_API_KEY not found. Get one free at https://console.groq.com"
        return True, "Configuration OK"
    
    @property
    def has_github_token(self) -> bool:
        """Check if GitHub token is configured."""
        return bool(self.github_token)


# Global config instance
config = Config()
