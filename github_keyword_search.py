from urllib.parse import urlparse
import requests
import base64

def pp(data):
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(data)
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

# Optional token to avoid rate limit
GITHUB_TOKEN = 'GitHub API Token'
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}

def get_repos(username):
    repos = []
    url = f'https://api.github.com/users/{username}/repos?per_page=100'
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        for repo in res.json():
            repos.append(repo['name'])
    return repos

def get_files_path(username, repo):
    # get default branch
    repo_url = f'https://api.github.com/repos/{username}/{repo}'
    res = requests.get(repo_url, headers=HEADERS)
    if res.status_code != 200:
        return []
    default_branch = res.json().get("default_branch", "main") # If the default_branch key doesn't exist, it returns 'main' as the default.

    # get the files path
    repo_tree_url = f'https://api.github.com/repos/{username}/{repo}/git/trees/{default_branch}?recursive=1' # recursive=1 enable recursive mode
    res = requests.get(repo_tree_url, headers=HEADERS)
    if res.status_code != 200:
        return []
    files_path = []
    for item in res.json().get("tree", []):
        if(item["type"] == "blob"): #blob refer to file and tree refer to folder
            files_path.append(item["path"])
    return files_path
    
def get_file_content(username, repo, file):
    file_url = f'https://api.github.com/repos/{username}/{repo}/contents/{file}'
    res = requests.get(file_url, headers=HEADERS)
    if res.status_code != 200: 
        return ''
    
    file_content_data = res.json()
    if file_content_data.get('encoding') == 'base64':
        try:
            return base64.b64decode(file_content_data["content"]).decode('utf-8', errors='ignore')
        except:
            return ''
    return ''


# MAIN
github_link = input("Enter GitHub URL (ex: https://github.com/user): ")
input_keywords = input("Enter keywords (ex: user,password): ").strip().split(',')
keywords = []
for kw in input_keywords:
    keywords.append(kw)

username = urlparse(github_link).path.strip('/')
repos = get_repos(username)

if not repos:
    print("❌ No public repositories found or invalid username.")

print(f"🔍 Searching {len(repos)} repositories for keywords: {keywords}")

for repo in repos:
    print(f"\n📦 Searching in repository: {repo}")
    repo_files_path = get_files_path(username, repo)

    for file in repo_files_path:
        file_content = get_file_content(username, repo, file)
        # pp(file_content)

        for keyword in keywords:
            if keyword.lower() in file_content.lower():
                print(f"\n✅ Found '{keyword}' in {username}/{repo}/{file}")
                print(f"🔗 URL: https://github.com/{username}/{repo}/blob/main/{file}")
