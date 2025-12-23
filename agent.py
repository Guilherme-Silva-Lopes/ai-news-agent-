"""
AI News Agent using LangChain 1.0 create_agent API.
"""
from datetime import datetime
from pathlib import Path
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config
from tools import get_all_tools


class AINewsAgent:
    """AI Agent for researching and summarizing AI and automation news."""
    
    def __init__(self):
        """Initialize the AI News Agent with Gemini model and tools."""
        self.model = self._initialize_model()
        self.tools = get_all_tools()
        self.agent = self._create_agent()
    
    def _initialize_model(self):
        """
        Initialize the Gemini model.
        
        Returns:
            ChatGoogleGenerativeAI: Configured Gemini model.
        """
        model = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        return model
    
    def _create_agent(self):
        """
        Create the LangChain agent using the create_agent API.
        
        Returns:
            Agent: Configured LangChain agent.
        """
        system_prompt = self._get_system_prompt()
        
        agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=system_prompt
        )
        
        return agent
    
    def _get_system_prompt(self) -> str:
        """
        Get the fixed system prompt for the agent.
        
        Returns:
            str: System prompt for the agent.
        """
        current_date = datetime.now().strftime("%B %d, %Y")
        
        prompt = f"""You are an expert AI research assistant specializing in artificial intelligence and automation news.

Today's date is {current_date}.

Your task is to:
1. Search for the most recent news about AI and automation from the LAST 24 HOURS ONLY
2. Focus on: major AI announcements, new AI models, automation technologies, AI regulations, significant research breakthroughs, and industry developments
3. For each news item, you MUST include the source URL from your search results
4. Organize findings into a clear, professional report

For each news item, provide:
- A clear, descriptive headline (without quotes or special formatting)
- A concise summary in 2-4 sentences (write naturally, no excessive quotes)
- Source URL: [Include the full URL from search results]
- Why it's significant

Format your response as follows:

EXECUTIVE SUMMARY
[2-3 sentences highlighting the most important news from today]

---

NEWS ITEM 1: [Headline Here]
[Natural, clean summary without quotes or special characters. Write professionally and clearly.]
Source: [Full URL here]
Significance: [Why this matters]

---

NEWS ITEM 2: [Headline Here]
[Natural summary]
Source: [Full URL here]
Significance: [Why this matters]

Important guidelines:
- Write in clean, natural language WITHOUT excessive quotes or formatting marks
- ALWAYS include the source URL from your search results
- Only report news from the LAST 24 HOURS
- Focus on factual, verified information from reputable sources
- Be concise but comprehensive
- Use clear, professional language suitable for a business report
- No markdown bold/italic unless absolutely necessary

Begin your research and create today's news report."""
        
        return prompt
    
    def _generate_search_queries(self) -> list:
        """
        Generate multiple targeted search queries using current date.
        
        Returns:
            list: List of search query strings.
        """
        current_date = datetime.now()
        month_year = current_date.strftime("%B %Y")  # e.g., "December 2025"
        date_full = current_date.strftime("%B %d, %Y")  # e.g., "December 23, 2025"
        
        queries = [
            f"AI model releases {month_year}",
            f"artificial intelligence news {date_full}",
            f"AI breakthroughs this week {month_year}",
            f"OpenAI Google Anthropic news today",
            f"AI automation industry news {month_year}",
            f"AI regulation updates {month_year}",
            f"latest AI research {month_year}",
        ]
        
        return queries
    
    def research_and_generate_report(self) -> str:
        """
        Execute deep research across multiple search queries to generate comprehensive report.
        
        Returns:
            str: The generated news report content.
        """
        print("🔍 Starting deep AI news research...")
        
        # Get current date for validation
        current_date = datetime.now()
        print(f"📅 Current date: {current_date.strftime('%B %d, %Y')}")
        
        # Generate search queries dynamically
        search_queries = self._generate_search_queries()
        print(f"🎯 Performing {len(search_queries)} targeted searches...")
        
        # Build comprehensive user message with all search queries
        user_message = f"""Today is {current_date.strftime('%B %d, %Y')}.

Perform comprehensive research on AI and automation news from the LAST 24 HOURS ONLY.

Execute these targeted searches to ensure full coverage:
{chr(10).join([f'{i+1}. {q}' for i, q in enumerate(search_queries)])}

CRITICAL REQUIREMENTS:
- Current date is {current_date.strftime('%B %d, %Y')}
- ONLY include news from the last 24 hours
- REJECT any news from {current_date.year - 1} or earlier
- Each news item MUST include the source URL
- Perform ALL searches above for comprehensive coverage
- Deduplicate similar news items
- Focus on verified, factual information

Create a comprehensive daily news report following the format specified in your system prompt."""
        
        try:
            # Execute agent with comprehensive research
            response = self.agent.invoke({
                "messages": [{"role": "user", "content": user_message}]
            })
            
            # Extract content from response - handle various formats including Gemini 2.5 Flash
            content = self._extract_content_from_response(response)
            
            print("✅ Research completed successfully!")
            return content
            
        except Exception as e:
            print(f"❌ Error during research: {str(e)}")
            raise
    
    def _extract_content_from_response(self, response) -> str:
        """
        Extract text content from various response formats.
        Handles Gemini 2.5 Flash format: [{'type': 'text', 'text': '...', 'extras': {...}}]
        """
        # Direct content attribute
        if hasattr(response, 'content'):
            content = response.content
            # If content is a list/dict, process it
            if isinstance(content, (list, dict)):
                return self._extract_text_from_structure(content)
            return str(content)
        
        # Dict with 'output' key
        if isinstance(response, dict) and 'output' in response:
            output = response['output']
            if isinstance(output, (list, dict)):
                return self._extract_text_from_structure(output)
            return str(output)
        
        # Dict with 'messages' key
        if isinstance(response, dict) and 'messages' in response:
            if response['messages']:
                msg_content = response['messages'][-1].content
                if isinstance(msg_content, (list, dict)):
                    return self._extract_text_from_structure(msg_content)
                return str(msg_content)
        
        # List response
        if isinstance(response, list):
            return self._extract_text_from_structure(response)
        
        # Fallback to string
        return str(response)
    
    def _extract_text_from_structure(self, data) -> str:
        """
        Extract text from Gemini 2.5 Flash structure:
        [{'type': 'text', 'text': '...', 'extras': {...}}]
        """
        # Handle list
        if isinstance(data, list):
            text_parts = []
            for item in data:
                if isinstance(item, dict):
                    # Gemini 2.5 Flash format
                    if 'text' in item:
                        text_parts.append(str(item['text']))
                    # Other dict formats
                    elif 'content' in item:
                        text_parts.append(str(item['content']))
                elif hasattr(item, 'content'):
                    text_parts.append(str(item.content))
                else:
                    text_parts.append(str(item))
            
            return '\n'.join(text_parts) if text_parts else str(data)
        
        # Handle dict
        if isinstance(data, dict):
            if 'text' in data:
                return str(data['text'])
            if 'content' in data:
                return str(data['content'])
        
        # Fallback
        return str(data)

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="AI News Agent - Research Phase")
    parser.add_argument("--output", help="Path to save the generated news content")
    args = parser.parse_args()
    
    try:
        # Validate config first
        Config.validate()
        
        agent = AINewsAgent()
        content = agent.research_and_generate_report()
        
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            # Ensure content is always a string before writing
            content_str = str(content) if not isinstance(content, str) else content
            output_path.write_text(content_str, encoding='utf-8')
            print(f"📝 Content saved to: {output_path.absolute()}")
        else:
            print(content)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
