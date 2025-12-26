# 🐺 RepoHunter - User Guide

## 🔑 First-Time Setup (Required)

Before using RepoHunter, you need a **FREE Groq API key**:

### Step 1: Get Your API Key
1. Go to **[console.groq.com](https://console.groq.com)**
2. Sign up for free (takes 30 seconds)
3. Click **"Create API Key"**
4. Copy your key

### Step 2: Configure RepoHunter
```powershell
cd c:\Users\Usuario\Desktop\RepoHunter

# Copy the template
copy .env.example .env

# Edit .env and paste your API key
notepad .env
```

Replace `your_groq_api_key_here` with your actual key.

### Step 3: Run
```powershell
python repohunter.py
```

---

## 🔍 Commands

### Search for Tools

Just type what you need:
```
web vulnerability scanner
OSINT tool for social media
red team framework for Active Directory
SQL injection scanner
```

### Install a Repository

After getting results:
```
install -repo "1"
```

### All Commands

| Command | What it does |
|---------|--------------|
| `<query>` | Search for tools |
| `install -repo "N"` | Clone repo #N |
| `history` | View search history |
| `clear` | Clear screen |
| `version` | Show version |
| `help` | Show help |
| `exit` | Quit |

---

## 💡 Pro Tips

- **Be specific**: "SQL injection scanner" > "hacking tool"
- **Mention language**: "network scanner in Go"
- **Add context**: "beginner-friendly OSINT tool"

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "GROQ_API_KEY not found" | Did you create `.env` file? See setup above |
| "API key invalid" | Check your key at console.groq.com |
| No results | Try different keywords |
| Rate limit | Wait 1 minute and retry |

---

## 💰 Cost

**100% FREE:**
- ✅ Groq AI - Free tier included
- ✅ GitHub API - No token needed
- ✅ RepoHunter - Open source (MIT)

---

**Happy Hunting! 🐺**

*Created by GhostLayer-dev*
