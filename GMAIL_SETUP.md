# Gmail OAuth2 Setup Guide

This guide will help you configure Gmail OAuth2 credentials for the Daily AI News Agent.

## Prerequisites
- Gmail account
- Google Cloud Project

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "AI News Agent" and click "Create"

## Step 2: Enable Gmail API

1. In the Google Cloud Console, navigate to **APIs & Services** → **Library**
2. Search for "Gmail API"
3. Click on it and press **Enable**

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (unless you have a Google Workspace)
3. Fill in the required fields:
   - App name: `AI News Agent`
   - User support email: Your email
   - Developer contact: Your email
4. Click **Save and Continue**
5. On **Scopes** page, click **Add or Remove Scopes**
6. Add these scopes:
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/userinfo.email`
   - `https://www.googleapis.com/auth/userinfo.profile`
7. Click **Save and Continue**
8. Add your email as a test user
9. Click **Save and Continue**

## Step 4: Create OAuth2 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select **Desktop app** as Application type
4. Name it "AI News Agent"
5. Click **Create**
6. Download the JSON file or copy the **Client ID** and **Client Secret**

## Step 5: Get Refresh Token

Run this Python script to obtain a refresh token:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/userinfo.email'
]

CLIENT_ID = "your-client-id-here.apps.googleusercontent.com"
CLIENT_SECRET = "your-client-secret-here"

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    scopes=SCOPES
)

creds = flow.run_local_server(port=0)
print(f"\n✅ Refresh Token: {creds.refresh_token}")
print(f"📋 Save this token securely!")
```

Install dependencies first:
```bash
pip install google-auth-oauthlib
```

Run the script, authorize in the browser, and copy the refresh token.

## Step 6: Configure Kestra Secrets

In Kestra UI, go to **Namespace Variables** and create a secret called `GMAIL_CREDENTIALS`:

```json
{
  "client_id": "your-client-id-here.apps.googleusercontent.com",
  "client_secret": "your-client-secret-here",
  "refresh_token": "your-refresh-token-here"
}
```

## Testing

Run the workflow again. The email should now send successfully!

## Troubleshooting

- **401 Unauthorized**: Check that scopes include `userinfo.email`
- **Invalid grant**: Refresh token may have expired, regenerate it
- **App blocked**: Make sure app is in "Testing" mode and you're added as a test user
