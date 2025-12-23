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
kestra kv put GOOGLE_API_KEY "your_google_api_key_here" --namespace ai.news
```

#### Tavily API Key
```bash
kestra kv put TAVILY_API_KEY "your_tavily_api_key_here" --namespace ai.news
```

#### Gmail Credentials
```bash
kestra kv put GMAIL_CREDENTIALS '{"user": "your_email@gmail.com", "password": "your_app_password", "recipient": "recipient@example.com"}' --namespace ai.news
```

**Alternative: Using Kestra UI**

1. Navigate to KV Store in Kestra UI
2. Add each credential:
   - Key: `GOOGLE_API_KEY`, Value: `your_google_api_key_here`
   - Key: `TAVILY_API_KEY`, Value: `your_tavily_api_key_here`
   - Key: `GMAIL_CREDENTIALS`, Value (as JSON):
     ```json
     {
       "user": "your_email@gmail.com",
       "password": "your_app_password",
       "recipient": "recipient@example.com"
     }
     ```

### 2. Deploy the Workflow

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Add AI News Agent"
   git push origin main
   ```

2. In Kestra UI:
   - Navigate to Flows
   - Click "Create Flow"
   - Copy the contents of `kestra-workflow.yaml`
   - Paste and save

3. The workflow will automatically run Monday-Friday at 7:00 AM (Brazil time)

### 3. Manual Execution

To test immediately, click "Execute" on the flow in Kestra UI.

## 📁 Project Structure

```
LAngchain Kestra Daily News Agent/
├── agent.py              # Main AI agent using LangChain 1.0
├── tools.py              # Web search tool configuration
├── pdf_generator.py      # PDF report generation
├── email_sender.py       # Email delivery module
├── config.py             # Configuration management
├── main.py               # Entry point orchestrator
├── requirements.txt      # Python dependencies
├── kestra-workflow.yaml  # Kestra workflow definition
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🛠️ Configuration

### Schedule Customization

Edit `kestra-workflow.yaml` to change the schedule:

```yaml
triggers:
  - id: daily-schedule
    cron: "0 7 * * 1-5"  # Minute Hour Day Month DayOfWeek
    timezone: America/Sao_Paulo
```

### Model Selection

Change the Gemini model in `config.py`:

```python
MODEL_NAME = "gemini-1.5-flash"  # or "gemini-1.5-pro"
```

### Search Results Limit

Adjust in `config.py`:

```python
MAX_SEARCH_RESULTS = 10  # Number of search results to fetch
```

## 📧 Email Format

The agent sends HTML-formatted emails with:
- Professional styling
- Daily date header
- PDF attachment with comprehensive news report

## 🔍 How It Works

1. **Research Phase**: Agent searches for recent AI/automation news using Tavily
2. **Analysis Phase**: Gemini processes and structures the findings
3. **Generation Phase**: Creates a professional PDF report
4. **Delivery Phase**: Sends the report via Gmail

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
