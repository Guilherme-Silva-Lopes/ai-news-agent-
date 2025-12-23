"""
Discord webhook sender for the AI News Agent.
Sends daily news reports as Discord messages with PDF attachments.
"""
import os
import sys
import argparse
import requests


class DiscordSender:
    """
    Handles sending news reports via Discord webhook.
    """
    
    def __init__(self, webhook_url: str):
        """
        Initialize the Discord sender.
        
        Args:
            webhook_url: Discord webhook URL from KV Store
        """
        self.webhook_url = webhook_url
    
    def send_report(self, pdf_path: str) -> bool:
        """
        Send the news report to Discord with PDF attachment.
        
        Args:
            pdf_path: Path to the PDF file to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if PDF exists
            if not os.path.exists(pdf_path):
                print(f"❌ PDF file not found: {pdf_path}")
                return False
            
            # Prepare the message
            message_content = "📰 **Daily AI News Report**\n\nHere's your daily AI news digest!"
            
            # Prepare the multipart form data
            with open(pdf_path, 'rb') as pdf_file:
                files = {
                    'file': (os.path.basename(pdf_path), pdf_file, 'application/pdf')
                }
                data = {
                    'content': message_content
                }
                
                # Send to Discord webhook
                print(f"📨 Sending report to Discord...")
                response = requests.post(
                    self.webhook_url,
                    data=data,
                    files=files
                )
                
                response.raise_for_status()
            
            print(f"✅ Report sent successfully to Discord!")
            return True
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error from Discord: {e}")
            print(f"❌ Response: {e.response.text if e.response else 'No response'}")
            return False
        except Exception as e:
            print(f"❌ Failed to send report: {e}")
            return False


def main():
    """
    Main function to send the report via Discord webhook.
    """
    parser = argparse.ArgumentParser(description="Send AI News Report via Discord Webhook")
    parser.add_argument("--file", required=True, help="Path to the PDF file to send")
    args = parser.parse_args()
    
    # Get the Discord webhook URL from environment
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("❌ Error: DISCORD_WEBHOOK_URL environment variable is not set")
        sys.exit(1)
    
    # Create sender and send report
    sender = DiscordSender(webhook_url)
    success = sender.send_report(args.file)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
