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
    
    def research_and_generate_report(self) -> str:
        """
        Execute the agent to research and generate a news report.
        
        Returns:
            str: The generated news report content.
        """
        print("🔍 Starting AI news research...")
        
        # Fixed user message for daily news research
        user_message = (
            "Research today's most important AI and automation news and create a "
            "comprehensive daily report following the format specified in your instructions."
        )
        
        try:
            # Invoke the agent
            result = self.agent.invoke({
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            })
            
            # Extract the content from the result
            if isinstance(result, dict) and "messages" in result:
                # Get the last message (agent's response)
                last_message = result["messages"][-1]
                content = last_message.content
                
                # Handle case where content is a list
                if isinstance(content, list):
                    # Join list items or extract text from content blocks
                    content = "\n".join(
                        item.get("text", str(item)) if isinstance(item, dict) else str(item)
                        for item in content
                    )
            else:
                content = str(result)
            
            print("✅ News research completed successfully!")
            return content
            
        except Exception as e:
            print(f"❌ Error during news research: {str(e)}")
            raise

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
            output_path.write_text(content, encoding='utf-8')
            print(f"📝 Content saved to: {output_path.absolute()}")
        else:
            print(content)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
