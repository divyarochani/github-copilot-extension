# GitHub Copilot Extension Backend

Simple Python Flask backend for GitHub Copilot extension that responds to chat commands using GitHub APIs.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your GitHub token to `.env`:
```
GITHUB_TOKEN=your_github_personal_access_token
```

4. Run the application:
```bash
python app.py
```

## Available Commands

- `user info <username>` - Get GitHub user information
- `repo info <owner/repo>` - Get repository details
- `search <query>` - Search repositories

## API Endpoints

- `POST /copilot/chat` - Main chat endpoint
- `GET /health` - Health check

## Example Usage

Send POST request to `/copilot/chat`:
```json
{
  "message": "user info octocat"
}
```

Response:
```json
{
  "response": "**GitHub User** (@octocat)\n📍 San Francisco\n📊 8 public repos...",
  "timestamp": "2024-01-01T12:00:00"
}
```