"""
RepoHunter - GitHub API Integration
Search and fetch repository metadata from GitHub.
"""

import requests
from typing import Optional
from .config import config


class GitHubAPI:
    """GitHub API client for repository search."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RepoHunter-CLI"
        })
        
        # Add auth token if available
        if config.has_github_token:
            self.session.headers["Authorization"] = f"token {config.github_token}"
    
    def search_repositories(
        self,
        query: str,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 10
    ) -> dict:
        """
        Search GitHub repositories.
        
        Args:
            query: Search query string
            sort: Sort by (stars, forks, updated)
            order: Order (asc, desc)
            per_page: Number of results
            
        Returns:
            API response as dict
        """
        url = f"{self.BASE_URL}/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Security: Sanitize error message - don't expose internal network details
            error_msg = str(e).lower()
            if "timeout" in error_msg:
                return {"error": "GitHub request timed out. Try again.", "items": []}
            elif "rate" in error_msg or "403" in error_msg:
                return {"error": "GitHub rate limit reached. Wait a moment.", "items": []}
            elif "401" in error_msg or "auth" in error_msg:
                return {"error": "GitHub authentication failed.", "items": []}
            else:
                return {"error": "GitHub connection error. Check your internet.", "items": []}
    
    def get_repository(self, owner: str, repo: str) -> Optional[dict]:
        """
        Get detailed repository information.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository data or None
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None
    
    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """
        Get repository README content.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            README content or None
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # README is base64 encoded
            import base64
            content = base64.b64decode(data.get("content", "")).decode("utf-8")
            return content[:2000]  # Limit for AI context
        except Exception:
            return None


# Global instance
github = GitHubAPI()
