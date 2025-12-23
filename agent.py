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
1. Search for the most recent and relevant news about AI and automation from the last 24-48 hours
2. Focus on: major AI announcements, new AI models, automation technologies, AI regulations, significant research breakthroughs, and industry developments
3. Organize the findings into a clear, professional report
4. For each news item, include:
   - A clear, descriptive headline
   - A concise summary (2-4 sentences)
   - The source or publication
   - Why it's significant

Format your response as a well-structured report with:
- An executive summary at the top (2-3 sentences highlighting the most important news)
- Main news items organized by importance or category
- Clear section headings
- Professional, informative tone

Important guidelines:
- Focus on factual, verified information from reputable sources
- Prioritize recent developments (last 24-48 hours)
- Highlight trends or patterns if you notice them
- Be concise but comprehensive
- Use clear, professional language suitable for a business report

Begin your research and create a comprehensive daily news report."""
        
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
                content = result["messages"][-1].content
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
