"""
RepoHunter - Terminal UI
Professional CLI interface with box-drawing and colors.
"""

import sys
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init(autoreset=True)


class UI:
    """Terminal UI manager for RepoHunter."""
    
    # Colors
    CYAN = Fore.CYAN
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    RED = Fore.RED
    WHITE = Fore.WHITE
    MAGENTA = Fore.MAGENTA
    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT
    
    @staticmethod
    def clear_line():
        """Clear current line."""
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.flush()
    
    @staticmethod
    def header():
        """Display the main RepoHunter header."""
        print()
        print(f"{UI.CYAN}╔══════════════════════════════════════════════════════════════╗{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}                                                              {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}   🐺 {UI.BRIGHT}{UI.WHITE}R E P O H U N T E R{UI.RESET}                                   {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}   {UI.MAGENTA}AI-Powered GitHub Tool Finder for Cybersecurity{UI.RESET}          {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}                                                              {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}╠══════════════════════════════════════════════════════════════╣{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}   {UI.GREEN}▸ Powered by Groq Cloud (100% Free AI){UI.RESET}                    {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}   {UI.GREEN}▸ Real-time GitHub Repository Analysis{UI.RESET}                    {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}   {UI.GREEN}▸ Intelligent Ranking by Practical Value{UI.RESET}                  {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}╠══════════════════════════════════════════════════════════════╣{UI.RESET}")
        print(f"{UI.CYAN}║{UI.RESET}   {UI.WHITE}Created by:{UI.RESET} {UI.BRIGHT}{UI.GREEN}GhostLayer-dev{UI.RESET}              {UI.YELLOW}v1.0.0{UI.RESET}       {UI.CYAN}║{UI.RESET}")
        print(f"{UI.CYAN}╚══════════════════════════════════════════════════════════════╝{UI.RESET}")
        print()
    
    @staticmethod
    def section(title: str, emoji: str = ""):
        """Print a section divider with title."""
        print()
        print(f"{UI.CYAN}─────────────────────────────────────────────────────{UI.RESET}")
        print(f"{emoji} {UI.BRIGHT}{UI.WHITE}{title}{UI.RESET}")
        print(f"{UI.CYAN}─────────────────────────────────────────────────────{UI.RESET}")
    
    @staticmethod
    def query(text: str):
        """Display the parsed query."""
        print(f"\n{UI.GREEN}▶ Query:{UI.RESET}")
        print(f"  {text}")
    
    @staticmethod
    def profile(domain: str, tool_type: str, language: str, skill_tier: str):
        """Display the detected profile."""
        print(f"\n{UI.GREEN}▶ Detected Profile:{UI.RESET}")
        print(f"  - Domain      : {UI.YELLOW}{domain}{UI.RESET}")
        print(f"  - Tool Type   : {UI.YELLOW}{tool_type}{UI.RESET}")
        print(f"  - Language    : {UI.YELLOW}{language}{UI.RESET}")
        print(f"  - Skill Tier  : {UI.YELLOW}{skill_tier}{UI.RESET}")
    
    @staticmethod
    def repository(rank: int, name: str, url: str, language: str, summary: str, why: str, 
                   stars: int = 0, forks: int = 0, updated: str = ""):
        """Display a repository entry with stats."""
        print(f"\n{UI.BRIGHT}[{rank}] {UI.CYAN}{name}{UI.RESET}")
        print(f"    Repo URL   : {UI.WHITE}{url}{UI.RESET}")
        print(f"    Language   : {UI.YELLOW}{language}{UI.RESET}")
        # Stats line
        stats_line = f"    {UI.YELLOW}⭐ {stars:,} stars{UI.RESET}"
        if forks > 0:
            stats_line += f"  {UI.CYAN}⬇ {forks:,} forks{UI.RESET}"
        if updated:
            stats_line += f"  {UI.MAGENTA}📅 {updated}{UI.RESET}"
        print(stats_line)
        print(f"    Summary    :")
        print(f"      {summary}")
        print(f"    {UI.GREEN}Why #{rank}{UI.RESET}     :")
        print(f"      {why}")
    
    @staticmethod
    def install_options():
        """Display install command instructions."""
        print(f"\nTo install a repository:")
        print()
        print(f"  {UI.CYAN}install -repo \"<NUMBER>\"{UI.RESET}")
        print()
        print(f"Example:")
        print(f"  {UI.CYAN}install -repo \"1\"{UI.RESET}")
        print()
        print(f"(This will clone the repository and show setup steps)")
    
    @staticmethod
    def notes(notes_list: list[str]):
        """Display notes section."""
        for note in notes_list:
            print(f"- {note}")
    
    @staticmethod
    def recommendation(text: str):
        """Display expert recommendation."""
        print(text)
    
    @staticmethod
    def install_header(rank: int, name: str):
        """Display install command header."""
        print(f"\n{UI.GREEN}▶ Installing repository [{rank}] {name}{UI.RESET}")
        print()
    
    @staticmethod
    def install_commands(clone_url: str, repo_name: str, setup_steps: list[str]):
        """Display install commands."""
        print(f"  {UI.CYAN}git clone {clone_url}{UI.RESET}")
        print(f"  {UI.CYAN}cd {repo_name}{UI.RESET}")
        for step in setup_steps:
            print(f"  {UI.CYAN}{step}{UI.RESET}")
        print()
        print(f"{UI.GREEN}✔ Installation guide ready.{UI.RESET}")
    
    @staticmethod
    def error(message: str):
        """Display error message."""
        print(f"\n{UI.RED}❌ Error: {message}{UI.RESET}")
    
    @staticmethod
    def warning(message: str):
        """Display warning message."""
        print(f"\n{UI.YELLOW}⚠️  {message}{UI.RESET}")
    
    @staticmethod
    def success(message: str):
        """Display success message."""
        print(f"\n{UI.GREEN}✔ {message}{UI.RESET}")
    
    @staticmethod
    def loading(message: str):
        """Display loading message."""
        print(f"\n{UI.YELLOW}⏳ {message}...{UI.RESET}", end='', flush=True)
    
    @staticmethod
    def input_prompt() -> str:
        """Get user input with styled prompt."""
        print()
        return input(f"{UI.GREEN}🔍 Enter your search query:{UI.RESET} ").strip()
    
    @staticmethod
    def waiting_input():
        """Display waiting for input message."""
        print(f"\n{UI.CYAN}Waiting for input...{UI.RESET}")
