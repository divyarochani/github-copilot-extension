from flask import Flask, request, jsonify
import requests
import os
import jwt
import time
from datetime import datetime

app = Flask(__name__)

# GitHub App configuration
GITHUB_APP_ID = os.getenv('GITHUB_APP_ID')
GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_PRIVATE_KEY_PATH = os.getenv('GITHUB_PRIVATE_KEY_PATH')

# Fallback to personal access token for testing
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_API_BASE = 'https://api.github.com'

class GitHubAPI:
    def __init__(self):
        self.headers = self._get_headers()
    
    def _get_headers(self):
        """Get authentication headers"""
        if GITHUB_TOKEN:
            # Use personal access token for testing
            return {
                'Authorization': f'token {GITHUB_TOKEN}',
                'Accept': 'application/vnd.github.v3+json'
            }
        elif GITHUB_APP_ID and GITHUB_PRIVATE_KEY_PATH:
            # Use GitHub App authentication
            token = self._generate_jwt_token()
            return {
                'Authorization': f'Bearer {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        else:
            return {'Accept': 'application/vnd.github.v3+json'}
    
    def _generate_jwt_token(self):
        """Generate JWT token for GitHub App"""
        try:
            with open(GITHUB_PRIVATE_KEY_PATH, 'r') as key_file:
                private_key = key_file.read()
            
            payload = {
                'iat': int(time.time()),
                'exp': int(time.time()) + 600,  # 10 minutes
                'iss': GITHUB_APP_ID
            }
            
            return jwt.encode(payload, private_key, algorithm='RS256')
        except Exception as e:
            print(f"Error generating JWT: {e}")
            return None
    
    def get_user_info(self, username):
        """Get GitHub user information"""
        url = f"{GITHUB_API_BASE}/users/{username}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_repo_info(self, owner, repo):
        """Get repository information"""
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def search_repositories(self, query, limit=5):
        """Search repositories"""
        url = f"{GITHUB_API_BASE}/search/repositories"
        params = {'q': query, 'per_page': limit}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else None

github_api = GitHubAPI()

@app.route('/copilot/chat', methods=['POST'])
def copilot_chat():
    """Handle Copilot chat requests"""
    try:
        data = request.json
        message = data.get('message', '').lower()
        
        # Simple command parsing
        if 'user' in message and 'info' in message:
            username = extract_username(message)
            if username:
                user_info = github_api.get_user_info(username)
                if user_info:
                    response = format_user_info(user_info)
                else:
                    response = f"User '{username}' not found."
            else:
                response = "Please specify a username. Example: 'user info octocat'"
        
        elif 'repo' in message and 'info' in message:
            repo_parts = extract_repo(message)
            if repo_parts:
                owner, repo = repo_parts
                repo_info = github_api.get_repo_info(owner, repo)
                if repo_info:
                    response = format_repo_info(repo_info)
                else:
                    response = f"Repository '{owner}/{repo}' not found."
            else:
                response = "Please specify a repository. Example: 'repo info microsoft/vscode'"
        
        elif 'search' in message:
            query = extract_search_query(message)
            if query:
                results = github_api.search_repositories(query)
                if results and results.get('items'):
                    response = format_search_results(results['items'])
                else:
                    response = f"No repositories found for '{query}'"
            else:
                response = "Please specify a search query. Example: 'search python web framework'"
        
        else:
            response = get_help_message()
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_username(message):
    """Extract username from message"""
    words = message.split()
    try:
        user_index = words.index('user')
        if user_index + 2 < len(words):
            return words[user_index + 2]
    except ValueError:
        pass
    return None

def extract_repo(message):
    """Extract repository owner/name from message"""
    words = message.split()
    try:
        repo_index = words.index('repo')
        if repo_index + 2 < len(words):
            repo_full = words[repo_index + 2]
            if '/' in repo_full:
                return repo_full.split('/', 1)
    except ValueError:
        pass
    return None

def extract_search_query(message):
    """Extract search query from message"""
    words = message.split()
    try:
        search_index = words.index('search')
        if search_index + 1 < len(words):
            return ' '.join(words[search_index + 1:])
    except ValueError:
        pass
    return None

def format_user_info(user):
    """Format user information response"""
    return f"""**{user['name'] or user['login']}** (@{user['login']})
📍 {user.get('location', 'Not specified')}
📊 {user['public_repos']} public repos
👥 {user['followers']} followers, {user['following']} following
🔗 {user['html_url']}"""

def format_repo_info(repo):
    """Format repository information response"""
    return f"""**{repo['full_name']}**
📝 {repo.get('description', 'No description')}
⭐ {repo['stargazers_count']} stars
🍴 {repo['forks_count']} forks
📅 Updated: {repo['updated_at'][:10]}
🔗 {repo['html_url']}"""

def format_search_results(repos):
    """Format search results response"""
    result = "**Search Results:**\n\n"
    for repo in repos[:5]:
        result += f"• **{repo['full_name']}** ({repo['stargazers_count']} ⭐)\n"
        result += f"  {repo.get('description', 'No description')}\n\n"
    return result

def get_help_message():
    """Return help message with available commands"""
    return """**GitHub Copilot Assistant Commands:**

• `user info <username>` - Get user information
• `repo info <owner/repo>` - Get repository details  
• `search <query>` - Search repositories

**Examples:**
• user info octocat
• repo info microsoft/vscode
• search python web framework"""

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    if not GITHUB_TOKEN and not GITHUB_APP_ID:
        print("Warning: No GitHub authentication configured")
        print("Set either GITHUB_TOKEN or GitHub App credentials")
    app.run(debug=True, host='0.0.0.0', port=5000)