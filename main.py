"""
Main entry point for the AI News Agent.
Orchestrates the entire workflow: research, PDF generation, and email delivery.
"""
import sys
from datetime import datetime
from pathlib import Path
from config import Config
from agent import AINewsAgent
from pdf_generator import NewsReportGenerator
from email_sender import EmailSender


def main():
    """Main function to execute the complete news agent workflow."""
    print("=" * 70)
    print("🤖 AI News Agent - Daily Report Generator")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%B %d, %Y %H:%M:%S')}")
    print("=" * 70)
    
    try:
        # Step 1: Validate configuration
        print("\n🔍 Step 1/4: Validating configuration...")
        Config.validate()
        print("✅ Configuration validated successfully!")
        
        # Step 2: Run the AI agent to research news
        print("\n🔍 Step 2/4: Researching AI and automation news...")
        agent = AINewsAgent()
        news_content = agent.research_and_generate_report()
        
        # Optional: Save the raw content to a text file for debugging
        content_file = Path("news_content.txt")
        content_file.write_text(news_content, encoding='utf-8')
        print(f"📝 Raw content saved to: {content_file.absolute()}")
        
        # Step 3: Generate PDF report
        print("\n📄 Step 3/4: Generating PDF report...")
        pdf_generator = NewsReportGenerator()
        pdf_path = pdf_generator.generate_report(news_content)
        print(f"✅ PDF report generated: {Path(pdf_path).absolute()}")
        
        # Step 4: Send email with PDF attachment
        print("\n📧 Step 4/4: Sending email report...")
        email_sender = EmailSender()
        email_success = email_sender.send_report(pdf_path)
        
        if email_success:
            print("\n" + "=" * 70)
            print("🎉 SUCCESS! Daily news report completed and sent!")
            print("=" * 70)
            return 0
        else:
            print("\n" + "=" * 70)
            print("⚠️  Report generated but email sending failed!")
            print(f"📄 PDF saved at: {Path(pdf_path).absolute()}")
            print("=" * 70)
            return 1
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nPlease ensure all required environment variables are set:")
        print("  - GOOGLE_API_KEY")
        print("  - TAVILY_API_KEY")
        print("  - GMAIL_USER")
        print("  - GMAIL_PASSWORD")
        print("  - RECIPIENT_EMAIL")
        return 1
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
