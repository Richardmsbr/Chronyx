"""
Chronyx Community Edition - Email Service
Basic email sending functionality
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Basic email service for Community Edition"""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
        self.smtp_from = settings.smtp_from or settings.smtp_user
        
    def is_configured(self) -> bool:
        """Check if email is configured"""
        return all([
            self.smtp_host,
            self.smtp_user,
            self.smtp_password
        ])
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """Send an email"""
        if not self.is_configured():
            logger.warning("Email not configured - skipping send")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_from
            msg['To'] = to
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if bcc:
                msg['Bcc'] = ', '.join(bcc)
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            if html:
                msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                
                recipients = [to]
                if cc:
                    recipients.extend(cc)
                if bcc:
                    recipients.extend(bcc)
                
                server.send_message(msg, self.smtp_from, recipients)
            
            logger.info(f"Email sent successfully to {to}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    async def send_notification(
        self,
        to: str,
        title: str,
        message: str,
        action_url: Optional[str] = None
    ) -> bool:
        """Send a notification email with basic template"""
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">{title}</h2>
                    <p>{message}</p>
                    {f'<p><a href="{action_url}" style="display: inline-block; padding: 10px 20px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 5px;">Take Action</a></p>' if action_url else ''}
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                    <p style="font-size: 12px; color: #666;">
                        This is an automated message from Chronyx Community Edition.
                    </p>
                </div>
            </body>
        </html>
        """
        
        text_body = f"{title}\n\n{message}"
        if action_url:
            text_body += f"\n\nAction URL: {action_url}"
        
        return await self.send_email(
            to=to,
            subject=title,
            body=text_body,
            html=html_body
        )
