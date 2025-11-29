#!/usr/bin/env python3
"""
WhatsApp Bot for Chronyx Agents
Connects WhatsApp messages to AI agents
"""
import asyncio
import logging
from typing import Dict

from integrations.whatsapp.whatsapp_service import WhatsAppService
from templates.restaurant.restaurant_agent import create_restaurant_agent
from templates.consulting.consulting_agent import create_consulting_agent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WhatsAppBot:
    """WhatsApp bot that connects messages to Chronyx agents"""

    def __init__(self, template_type: str = "restaurant"):
        """
        Initialize WhatsApp bot

        Args:
            template_type: Type of agent template ("restaurant" or "consulting")
        """
        self.template_type = template_type
        self.agent = None
        self.whatsapp = None
        self.user_sessions: Dict[str, Dict] = {}

    async def start(self):
        """Start WhatsApp bot"""
        logger.info(f"Starting WhatsApp bot with {self.template_type} template...")

        # Create agent based on template type
        if self.template_type == "restaurant":
            self.agent = create_restaurant_agent()
        elif self.template_type == "consulting":
            self.agent = create_consulting_agent()
        else:
            raise ValueError(f"Unknown template type: {self.template_type}")

        # Create WhatsApp service
        self.whatsapp = WhatsAppService(
            session_name="chronyx-bot",
            message_handler=self.handle_message
        )

        # Start WhatsApp service
        await self.whatsapp.start()

        logger.info("✅ WhatsApp bot is running!")
        logger.info("Scan the QR code above with your WhatsApp app to connect")

        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping bot...")
            await self.stop()

    async def handle_message(self, message_data: Dict):
        """
        Handle incoming WhatsApp message

        Args:
            message_data: Message data from WhatsApp
                {
                    "from": "5511999999999@c.us",
                    "body": "message text",
                    "timestamp": 1234567890,
                    "isGroup": False
                }
        """
        sender = message_data.get("from")
        text = message_data.get("body", "").strip()
        is_group = message_data.get("isGroup", False)

        # Ignore group messages
        if is_group:
            logger.debug(f"Ignoring group message from {sender}")
            return

        # Ignore empty messages
        if not text:
            logger.debug(f"Ignoring empty message from {sender}")
            return

        logger.info(f"📱 Message from {sender}: {text}")

        try:
            # Get or create user session
            if sender not in self.user_sessions:
                self.user_sessions[sender] = {
                    "message_count": 0,
                    "context": {}
                }

            session = self.user_sessions[sender]
            session["message_count"] += 1

            # Process message with agent
            response = await self.agent.process_message(
                message=text,
                context=session.get("context"),
                user_id=sender
            )

            # Send response
            await self.whatsapp.send_message(sender, response)

            logger.info(f"✅ Response sent to {sender}")

        except Exception as e:
            logger.error(f"Error handling message from {sender}: {e}")

            # Send error message to user
            error_msg = (
                "Desculpe, ocorreu um erro ao processar sua mensagem. "
                "Por favor, tente novamente."
            )
            try:
                await self.whatsapp.send_message(sender, error_msg)
            except Exception as send_error:
                logger.error(f"Failed to send error message: {send_error}")

    async def stop(self):
        """Stop WhatsApp bot"""
        if self.whatsapp:
            await self.whatsapp.stop()
        logger.info("Bot stopped")


async def main():
    """Main entry point"""
    import sys

    # Parse command line arguments
    template_type = "restaurant"  # default

    if len(sys.argv) > 1:
        template_type = sys.argv[1].lower()
        if template_type not in ["restaurant", "consulting"]:
            print(f"Error: Unknown template type '{template_type}'")
            print("Usage: python whatsapp_bot.py [restaurant|consulting]")
            sys.exit(1)

    # Create and start bot
    bot = WhatsAppBot(template_type=template_type)
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
