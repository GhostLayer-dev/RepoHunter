"""
RepoHunter - Groq AI Integration
AI-powered repository analysis and ranking using Groq Cloud.
"""

import json
from groq import Groq
from .config import config


class GroqAI:
    """Groq AI client for intelligent repository analysis."""
    
    MODEL = "llama-3.3-70b-versatile"
    
    def __init__(self):
        self.client = None
        if config.groq_api_key:
            self.client = Groq(api_key=config.groq_api_key)
    
    def _call_ai(self, system_prompt: str, user_prompt: str) -> str:
        """Make a call to Groq AI."""
        if not self.client:
            return '{"error": "Groq API key not configured"}'
        
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            # Security: Sanitize error message - don't expose API keys or internal details
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "key" in error_msg.lower():
                error_msg = "API authentication failed. Check your GROQ_API_KEY."
            elif "rate" in error_msg.lower():
                error_msg = "Rate limit reached. Please wait and try again."
            elif "timeout" in error_msg.lower():
                error_msg = "Request timed out. Check your connection."
            else:
                error_msg = "AI service temporarily unavailable."
            return f'{{"error": "{error_msg}"}}'
    
    def analyze_query(self, user_query: str) -> dict:
        """
        Analyze user query to detect profile and ideal tool characteristics.
        
        Returns:
            dict with domain, tool_type, language, skill_tier, search_terms
        """
        system_prompt = """You are a cybersecurity and development tools expert.
Analyze the user's query and extract:
1. domain: web / osint / red team / blue team / network / mobile / forensics / malware / devops / general
2. tool_type: scanner / framework / cli / library / exploit / automation
3. language: python / go / rust / javascript / c / multi (if no preference)
4. skill_tier: beginner / intermediate / advanced
5. search_terms: optimal GitHub search query (2-5 keywords)
6. query_summary: clear 1-line technical summary of what user wants

Respond ONLY with valid JSON, no markdown:
{"domain": "", "tool_type": "", "language": "", "skill_tier": "", "search_terms": "", "query_summary": ""}"""

        result = self._call_ai(system_prompt, user_query)
        
        try:
            # Try to parse JSON from response
            result = result.strip()
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            return json.loads(result)
        except json.JSONDecodeError:
            # Security: Sanitize user query before using as fallback
            safe_query = ''.join(c for c in user_query if c.isalnum() or c.isspace())[:100]
            return {
                "domain": "general",
                "tool_type": "cli",
                "language": "multi",
                "skill_tier": "intermediate",
                "search_terms": safe_query,
                "query_summary": safe_query
            }
    
    def rank_repositories(self, user_query: str, profile: dict, repos: list) -> dict:
        """
        Rank and analyze repositories based on user needs.
        
        Args:
            user_query: Original user query
            profile: Analyzed profile from analyze_query
            repos: List of repositories from GitHub API
            
        Returns:
            dict with ranked_repos, notes, recommendation
        """
        # Prepare repo data for AI
        repo_data = []
        for i, repo in enumerate(repos[:10]):  # Max 10 repos
            repo_data.append({
                "index": i + 1,
                "name": repo.get("full_name", ""),
                "description": repo.get("description", "")[:200] if repo.get("description") else "",
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language", "Unknown"),
                "updated": repo.get("updated_at", "")[:10],
                "url": repo.get("html_url", "")
            })
        
        system_prompt = """You are RepoHunter, an expert curator of GitHub tools for cybersecurity and development.
Your job is to rank repositories by PRACTICAL VALUE, not hype.

CRITICAL RULES:
- NEVER invent repositories or URLs
- Only use the repos provided in the input
- Rank by: active maintenance, practical use, code quality, community trust
- Filter out abandoned or low-quality projects
- Be honest if no good options exist

Respond ONLY with valid JSON (no markdown):
{
  "ranked_repos": [
    {
      "rank": 1,
      "name": "owner/repo",
      "url": "https://github.com/...",
      "language": "Python",
      "stars": 12500,
      "forks": 2300,
      "updated": "2024-12-20",
      "summary": "What it does in 1-2 clear lines",
      "why": "Why it's the best choice for this use case"
    }
  ],
  "notes": ["requirement 1", "limitation 1"],
  "recommendation": "Expert advice on which to use first and why"
}

Return TOP 5 maximum. If less than 3 good options, return fewer."""

        user_prompt = f"""User Query: {user_query}
Profile: {json.dumps(profile)}
Available Repositories:
{json.dumps(repo_data, indent=2)}

Rank these repositories for the user's specific needs."""

        result = self._call_ai(system_prompt, user_prompt)
        
        try:
            result = result.strip()
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            return json.loads(result)
        except json.JSONDecodeError:
            # Fallback: return basic ranking
            ranked = []
            for repo in repos[:5]:
                ranked.append({
                    "rank": len(ranked) + 1,
                    "name": repo.get("full_name", "Unknown"),
                    "url": repo.get("html_url", ""),
                    "language": repo.get("language", "Unknown"),
                    "summary": repo.get("description", "No description")[:100],
                    "why": f"Has {repo.get('stargazers_count', 0)} stars"
                })
            return {
                "ranked_repos": ranked,
                "notes": ["AI analysis unavailable, showing by star count"],
                "recommendation": "Review each repository manually"
            }
    
    def get_install_steps(self, repo_name: str, language: str, readme: str = None) -> list:
        """
        Generate installation steps for a repository.
        
        Args:
            repo_name: Full repository name (owner/repo)
            language: Primary language
            readme: Optional README content
            
        Returns:
            List of installation command strings
        """
        readme_context = f"\nREADME excerpt:\n{readme[:1000]}" if readme else ""
        
        system_prompt = """You are a developer tools expert.
Generate 2-4 practical installation/setup commands for this repository.
Base your suggestions on the language and any README content provided.

Respond ONLY with a JSON array of command strings:
["command 1", "command 2"]

Keep commands simple and practical. Common patterns:
- Python: pip install -r requirements.txt, python setup.py install
- Go: go build, go install
- Node: npm install, npm run build
- Rust: cargo build --release
- Generic: make, ./configure && make install"""

        user_prompt = f"Repository: {repo_name}\nLanguage: {language}{readme_context}"
        
        result = self._call_ai(system_prompt, user_prompt)
        
        try:
            result = result.strip()
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            return json.loads(result)
        except json.JSONDecodeError:
            # Default fallback based on language
            fallbacks = {
                "Python": ["pip install -r requirements.txt"],
                "Go": ["go build"],
                "JavaScript": ["npm install"],
                "TypeScript": ["npm install", "npm run build"],
                "Rust": ["cargo build --release"],
                "C": ["make"],
                "C++": ["make"]
            }
            return fallbacks.get(language, ["# Check README for setup instructions"])


# Global instance
groq_ai = GroqAI()
