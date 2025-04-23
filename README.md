# 🔍 GitHub Repo Keyword Search Tool

A Python tool to search for specific keywords inside **all public repositories** of a given GitHub **user or organization**.

## 📌 Features

- Input a GitHub profile link (user/org), like `https://github.com/username`
- Automatically fetches all public repositories of that user
- Recursively checks every file in each repo for keyword matches
- Displays the matched file path, GitHub URL, and a short content snippet
- Handles base64 decoding for file contents
- Avoids GitHub API rate limits with optional token support

---

## 🚀 How It Works

1. Takes a GitHub profile URL as input  
2. Extracts username/org name  
3. Uses GitHub REST API to fetch all repositories  
4. For each repo:
   - Gets the file tree recursively
   - Downloads file content
   - Searches for each keyword in each file
5. Displays results with links and snippets

---

## 🛠️ Usage

### 🔧 Requirements
- Python 3.x
- `requests` library (install via `pip install requests`)
- Add your GitHub API Token in `GITHUB_TOKEN = 'GitHub API Token'`. You will find it into `github_keyword_search.py` file

### ▶️ Run the tool

```bash
python github_keyword_search.py
Enter GitHub URL (like https://github.com/username): https://github.com/OWASP
Enter keywords (comma-separated): token, csrf
```
