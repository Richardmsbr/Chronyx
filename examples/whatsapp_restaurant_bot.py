#!/usr/bin/env python3
"""
Example: Restaurant bot on WhatsApp
Quick start script to test WhatsApp integration
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from whatsapp_bot import WhatsAppBot


async def main():
    """Start restaurant bot on WhatsApp"""
    print("🍽️  Starting Restaurant Bot on WhatsApp...")
    print("=" * 50)

    bot = WhatsAppBot(template_type="restaurant")
    await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
