#!/usr/bin/env python3
"""
🐺 RepoHunter - AI GitHub Tool Finder
Powered by Groq Cloud (100% Free AI)

A professional CLI tool for finding and ranking GitHub repositories
for cybersecurity and development use cases.
"""

import sys
import re
import argparse
import subprocess

from modules import __version__
from modules.config import config
from modules.ui import UI
from modules.github_api import github
from modules.groq_ai import groq_ai


class RepoHunter:
    """Main RepoHunter application."""
    
    VERSION = __version__
    
    def __init__(self):
        self.last_results = []  # Store last search results for install command
        self.last_ranked = []   # Store ranked repos
        self.search_history = []  # Store search history (limited to 50)
        self.MAX_HISTORY = 50  # Security: limit history size
    
    def validate_config(self) -> bool:
        """Validate required configuration."""
        valid, message = config.validate()
        if not valid:
            UI.error(message)
            print("\nSetup Instructions:")
            print("  1. Get free API key: https://console.groq.com")
            print("  2. Create .env file with: GROQ_API_KEY=your_key_here")
            print("  3. (Optional) Add GITHUB_TOKEN for higher rate limits")
            return False
        return True
    
    def search(self, query: str):
        """
        Execute a search query and display results.
        
        Args:
            query: User's search query
        """
        # Save to history (with size limit for memory safety)
        if len(self.search_history) >= self.MAX_HISTORY:
            self.search_history.pop(0)  # Remove oldest
        self.search_history.append(query[:500])  # Limit query length
        
        # Step 1: Analyze query with AI
        UI.loading("Analyzing query with AI")
        profile = groq_ai.analyze_query(query)
        UI.clear_line()
        
        # Display query summary
        UI.query(profile.get("query_summary", query))
        
        # Display detected profile
        UI.profile(
            domain=profile.get("domain", "general"),
            tool_type=profile.get("tool_type", "cli"),
            language=profile.get("language", "multi"),
            skill_tier=profile.get("skill_tier", "intermediate")
        )
        
        # Step 2: Search GitHub
        search_terms = profile.get("search_terms", query)
        UI.loading(f"Searching GitHub for '{search_terms}'")
        
        results = github.search_repositories(search_terms, per_page=15)
        UI.clear_line()
        
        if "error" in results:
            UI.error(f"GitHub API error: {results['error']}")
            return
        
        repos = results.get("items", [])
        if not repos:
            UI.warning("No repositories found. Try different keywords.")
            return
        
        self.last_results = repos
        
        # Step 3: Rank with AI
        UI.loading("AI ranking repositories by practical value")
        ranked = groq_ai.rank_repositories(query, profile, repos)
        UI.clear_line()
        
        # Step 4: Display results
        UI.section("Top Matching Repositories", "🔥")
        
        ranked_repos = ranked.get("ranked_repos", [])
        if not ranked_repos:
            UI.warning("Could not rank repositories. Showing raw results.")
            for i, repo in enumerate(repos[:5]):
                UI.repository(
                    rank=i + 1,
                    name=repo.get("name", "Unknown"),
                    url=repo.get("html_url", ""),
                    language=repo.get("language", "Unknown"),
                    summary=repo.get("description", "No description")[:100] if repo.get("description") else "No description",
                    why="Shown by star count",
                    stars=repo.get("stargazers_count", 0),
                    forks=repo.get("forks_count", 0),
                    updated=repo.get("updated_at", "")[:10] if repo.get("updated_at") else ""
                )
        else:
            self.last_ranked = ranked_repos
            for repo in ranked_repos:
                UI.repository(
                    rank=repo.get("rank", 0),
                    name=repo.get("name", "Unknown"),
                    url=repo.get("url", ""),
                    language=repo.get("language", "Unknown"),
                    summary=repo.get("summary", "No description"),
                    why=repo.get("why", ""),
                    stars=repo.get("stars", 0),
                    forks=repo.get("forks", 0),
                    updated=repo.get("updated", "")
                )
        
        # Install options
        UI.section("Install Options", "📦")
        UI.install_options()
        
        # Notes
        notes = ranked.get("notes", [])
        if notes:
            UI.section("Notes", "⚠️")
            UI.notes(notes)
        
        # Expert recommendation
        recommendation = ranked.get("recommendation", "")
        if recommendation:
            UI.section("Expert Recommendation", "✅")
            UI.recommendation(recommendation)
    
    def install(self, repo_number: int):
        """
        Show installation instructions for a repository.
        
        Args:
            repo_number: 1-based index from last search results
        """
        if not self.last_ranked:
            UI.error("No search results. Run a search first.")
            return
        
        if repo_number < 1 or repo_number > len(self.last_ranked):
            UI.error(f"Invalid repository number. Choose 1-{len(self.last_ranked)}")
            return
        
        repo = self.last_ranked[repo_number - 1]
        repo_name = repo.get("name", "")
        repo_url = repo.get("url", "")
        language = repo.get("language", "Unknown")
        
        # Try to get README for better install instructions
        if "/" in repo_name:
            owner, name = repo_name.split("/", 1)
            readme = github.get_readme(owner, name)
        else:
            readme = None
            name = repo_name
        
        # Get AI-generated install steps
        UI.loading("Generating install instructions")
        steps = groq_ai.get_install_steps(repo_name, language, readme)
        UI.clear_line()
        
        # Display
        UI.install_header(repo_number, repo_name)
        UI.install_commands(
            clone_url=f"{repo_url}.git",
            repo_name=name,
            setup_steps=steps
        )
    
    def show_history(self):
        """Display search history."""
        if not self.search_history:
            UI.warning("No search history yet.")
            return
        
        print(f"\n{UI.CYAN}Search History:{UI.RESET}")
        for i, query in enumerate(self.search_history[-10:], 1):  # Last 10
            print(f"  {i}. {query}")
    
    def clear_screen(self):
        """Clear the terminal screen (secure implementation)."""
        # Security: Use subprocess instead of os.system to prevent command injection
        if sys.platform == 'win32':
            subprocess.run(['cmd', '/c', 'cls'], shell=False)
        else:
            subprocess.run(['clear'], shell=False)
        UI.header()
    
    def run(self):
        """Main application loop."""
        # Show header
        UI.header()
        
        # Show version
        print(f"{UI.CYAN}Version {self.VERSION}{UI.RESET}")
        
        # Validate config
        if not self.validate_config():
            return
        
        UI.success("Configuration OK - Ready to hunt!")
        
        # Main loop
        while True:
            try:
                user_input = UI.input_prompt()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\n🐺 Happy hunting! Goodbye.")
                    break
                
                # Check for install command
                install_match = re.match(r'install\s+-repo\s+"?(\d+)"?', user_input, re.IGNORECASE)
                if install_match:
                    repo_num = int(install_match.group(1))
                    self.install(repo_num)
                    continue
                
                # Check for version command
                if user_input.lower() in ["version", "-v", "--version"]:
                    print(f"\n🐺 RepoHunter v{self.VERSION}")
                    continue
                
                # Check for history command
                if user_input.lower() == "history":
                    self.show_history()
                    continue
                
                # Check for clear command
                if user_input.lower() in ["clear", "cls"]:
                    self.clear_screen()
                    continue
                
                # Check for help command
                if user_input.lower() in ["help", "?", "--help", "-h"]:
                    self.show_help()
                    continue
                
                # Regular search
                self.search(user_input)
                
            except KeyboardInterrupt:
                print("\n\n🐺 Interrupted. Goodbye!")
                break
            except Exception as e:
                # Security: Don't expose internal error details
                UI.error("An unexpected error occurred. Please try again.")
    
    def show_help(self):
        """Display help information."""
        print(f"""
{UI.CYAN}Commands:{UI.RESET}
  <query>              Search for tools (e.g., "web vulnerability scanner")
  install -repo "N"    Install repository number N from last search
  history              Show search history
  clear                Clear screen
  version              Show version
  help                 Show this help message
  exit / quit / q      Exit RepoHunter

{UI.CYAN}Examples:{UI.RESET}
  "OSINT tool for social media"
  "Red team framework for pentesting"
  "Network packet analyzer in Go"
  install -repo "1"
""")


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="🐺 RepoHunter - AI GitHub Tool Finder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python repohunter.py                    # Start interactive mode
  python repohunter.py --version          # Show version
  python repohunter.py --help             # Show this help

Powered by Groq Cloud (100% Free AI)
        """
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"🐺 RepoHunter v{__version__}"
    )
    
    args = parser.parse_args()
    
    app = RepoHunter()
    app.run()


if __name__ == "__main__":
    main()

