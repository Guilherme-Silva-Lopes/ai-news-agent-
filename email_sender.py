"""
Email sender module for the AI News Agent using Gmail OAuth2.
"""
import smtplib
import base64
import json
import argparse
import sys
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path
from config import Config

class EmailSender:
    """Handle sending emails with PDF attachments via Gmail using OAuth2."""
    
    def __init__(self):
        """Initialize the email sender with Gmail OAuth2 configuration."""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.user_email = "me" # Special value 'me' acts as the authenticated user
        
    def _get_access_token(self) -> str:
        """
        Refresh the access token using the refresh token.
        """
        params = {
            "client_id": Config.GMAIL_CLIENT_ID,
            "client_secret": Config.GMAIL_CLIENT_SECRET,
            "refresh_token": Config.GMAIL_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }
        
        try:
            response = requests.post("https://oauth2.googleapis.com/token", data=params)
            response.raise_for_status()
            data = response.json()
            return data["access_token"]
        except Exception as e:
            print(f"❌ Failed to refresh access token: {str(e)}")
            raise

    def _generate_oauth2_string(self, username, access_token, base64_encode=True):
        """
        Generate the XOAUTH2 string.
        """
        auth_string = f"user={username}\1auth=Bearer {access_token}\1\1"
        if base64_encode:
            auth_string = base64.b64encode(auth_string.encode("ascii")).decode("ascii")
        return auth_string

    def send_report(self, pdf_path: str, recipient_email: str = None) -> bool:
        """
        Send the PDF report via email.
        
        Args:
            pdf_path (str): Path to the PDF file to send.
            recipient_email (str): Email address of the recipient.
            
        Returns:
            bool: True if email was sent successfully, False otherwise.
        """
        if not recipient_email:
            recipient_email = Config.RECEIVER_EMAIL
            
        # We need the sender email address to form the message correctly.
        # Since we are using OAuth2 with a refresh token, we technically don't strictly need it 
        # for auth (we use token), but SMTP protocol likes a FROM address.
        # We can try to decode the ID token if available, or just fetch user info.
        # For simplicity, we'll fetch the user profile or assume 'me' works for the API but for SMTP we need an address.
        # Actually, let's fetch the email address associated with the token to be proper.
        
        access_token = self._get_access_token()
        
        try:
            # Fetch user info to get the email address from OAuth2 token
            headers = {"Authorization": f"Bearer {access_token}"}
            user_info_response = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers=headers)
            
            print(f"📡 Google API Response Status: {user_info_response.status_code}")
            
            if user_info_response.status_code == 200:
                user_info = user_info_response.json()
                sender_email = user_info.get("email")
                
                if not sender_email:
                    print(f"⚠️ User info response: {user_info}")
                    raise ValueError("Could not retrieve sender email from Google API")
                
                print(f"✅ Retrieved sender email: {sender_email}")
            else:
                print(f"⚠️ Failed to fetch user info: {user_info_response.text}")
                raise ValueError(f"Google API returned status {user_info_response.status_code}")
            
            # Create message
            message = self._create_message(pdf_path, sender_email, recipient_email)
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                
                # Authenticate using XOAUTH2
                auth_string = self._generate_oauth2_string(sender_email, access_token)
                server.docmd("AUTH", "XOAUTH2 " + auth_string)
                
                server.send_message(message)
            
            print(f"✅ Email sent successfully to {recipient_email}")
            return True
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error from Google API: {e}")
            print(f"❌ Response: {e.response.text if e.response else 'No response'}")
            return False
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    def _create_message(self, pdf_path: str, sender_email: str, recipient_email: str) -> MIMEMultipart:
        """Create the email message with PDF attachment."""
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = f"Daily AI News Report - {datetime.now().strftime('%B %d, %Y')}"
        
        # Email body
        body = self._create_email_body()
        message.attach(MIMEText(body, 'html'))
        
        # Attach PDF
        self._attach_pdf(message, pdf_path)
        
        return message
    
    def _create_email_body(self) -> str:
        """Create the HTML body of the email."""
        current_date = datetime.now().strftime('%B %d, %Y')
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb; border-bottom: 3px solid #2563eb; padding-bottom: 10px;">
                        🤖 Daily AI & Automation News Report
                    </h2>
                    <p>Attached is your daily report for <strong>{current_date}</strong>.</p>
                </div>
            </body>
        </html>
        """
        return html
    
    def _attach_pdf(self, message: MIMEMultipart, pdf_path: str):
        """Attach the PDF file to the email message."""
        pdf_filename = Path(pdf_path).name
        with open(pdf_path, 'rb') as attachment:
            part = MIMEBase('application', 'pdf')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {pdf_filename}')
        message.attach(part)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send email with PDF attachment")
    parser.add_argument("--file", required=True, help="Path to the PDF file")
    parser.add_argument("--recipient", help="Recipient email address")
    args = parser.parse_args()
    
    try:
        sender = EmailSender()
        success = sender.send_report(args.file, args.recipient)
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
