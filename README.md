# 🤖 AI News Agent - Daily Report Generator

An intelligent AI agent built with LangChain 1.0 that automatically researches the latest AI and automation news, generates professional PDF reports, and delivers them via email. Designed to run as a scheduled workflow in Kestra.

## 🌟 Features

- **Automated News Research**: Uses Gemini 1.5 Flash to search and analyze recent AI and automation news
- **Web Search Integration**: Leverages Tavily API for comprehensive web search capabilities
- **Professional PDF Reports**: Generates beautifully formatted PDF reports with ReportLab
- **Email Delivery**: Automatically sends reports via Gmail SMTP
- **Kestra Integration**: Scheduled execution Monday-Friday at 7:00 AM
- **Secure Credential Management**: Uses Kestra KV Store for API keys and credentials

## 📋 Prerequisites

- Python 3.11 or higher
- Google AI API key (for Gemini)
- Tavily API key (for web search)
- Gmail account with App Password enabled
- Kestra instance (for scheduled execution)

## 🔑 API Keys Setup

### 1. Google AI API Key (Gemini)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key

### 2. Tavily API Key

1. Go to [Tavily](https://app.tavily.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### 3. Gmail App Password

1. Go to your [Google Account settings](https://myaccount.google.com/)
2. Navigate to Security → 2-Step Verification
3. Scroll to "App passwords" and create a new one
4. Copy the 16-character password

## 🚀 Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd "LAngchain Kestra Daily News Agent"
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_gmail_app_password_here
RECIPIENT_EMAIL=recipient@example.com
```

### 5. Run Locally

```bash
python main.py
```

## 🎯 Kestra Deployment

### 1. Add Credentials to Kestra KV Store

Access your Kestra instance and add the following keys to the KV Store:

#### Google API Key
```bash
kestra kv put GOOGLE_API_KEY "your_google_api_key_here" --namespace company.team
```

#### Tavily API Key
```bash
kestra kv put TAVILY_API_KEY "your_tavily_api_key_here" --namespace company.team
```

#### Receiver Email
```bash
kestra kv put RECEIVER_EMAIL "recipient@example.com" --namespace company.team
```

#### Gmail OAuth2 Credentials
Store your OAuth2 credentials in a JSON object under `GMAIL_CREDENTIALS`:

```bash
kestra kv put GMAIL_CREDENTIALS '{"client_id": "your_client_id", "client_secret": "your_client_secret", "refresh_token": "your_refresh_token"}' --namespace company.team
```

### 2. Deploy the Workflow

1. The workflow will pull code automatically from GitHub:
   `https://github.com/Guilherme-Silva-Lopes/ai-news-agent-`

2. In Kestra UI:
   - Create Flow using the provided `kestra-workflow.yaml`
   - It runs automatically Mon-Fri at 7:00 AM

## 📁 Project Structure

```
LAngchain Kestra Daily News Agent/
├── agent.py              # Research agent (CLI: --output)
├── pdf_generator.py      # PDF generator (CLI: --input --output)
├── email_sender.py       # OAuth2 Email sender (CLI: --file)
├── tools.py              # Search tool config
├── config.py             # Config & Validation
├── main.py               # Legacy orchestrator
├── requirements.txt      # Dependencies
└── kestra-workflow.yaml  # Modular workflow definition
```

## 🔍 How It Works (Modular)

1. **Clone**: Kestra clones the repository
2. **Setup**: Installs dependencies
3. **Phase 1**: `agent.py` researches and saves to `news_content.txt`
4. **Phase 2**: `pdf_generator.py` reads text and creates `ai_news_report.pdf`
5. **Phase 3**: `email_sender.py` uses OAuth2 to send the PDF


## 🐛 Troubleshooting

### "Missing required environment variables"
- Ensure all credentials are properly set in KV Store or .env file

### "Authentication failed" (Gmail)
- Use an App Password, not your regular Gmail password
- Enable 2-Step Verification first

### "API key invalid" (Google AI)
- Verify the key is correct and active in Google AI Studio

### "Search failed" (Tavily)
- Check your Tavily API key
- Verify you haven't exceeded the free tier limits

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using LangChain 1.0, Gemini 1.5 Flash, and Kestra**
