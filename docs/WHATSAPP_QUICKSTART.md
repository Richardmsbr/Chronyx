# 📱 WhatsApp Quick Start Guide

## 5-Minute Setup

### 1. Install Node.js (if not installed)

```bash
# Check if Node.js is installed
node --version

# If not, install it:
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2. Configure API Key

Make sure your `.env` file has your API key:

```bash
# Edit .env
nano .env

# Add your NVIDIA API key:
OPENAI_API_KEY=nvapi-YOUR_KEY_HERE
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
DEFAULT_MODEL=meta/llama-3.1-8b-instruct
```

### 3. Start the Bot

```bash
# Activate virtual environment
source venv/bin/activate

# Start restaurant bot
python whatsapp_bot.py restaurant

# OR start consulting bot
python whatsapp_bot.py consulting
```

### 4. Connect WhatsApp

1. A QR code will appear in your terminal
2. Open WhatsApp on your phone
3. Go to: **Settings → Linked Devices → Link a Device**
4. Scan the QR code
5. Wait for "WhatsApp is ready!" message

### 5. Test It! 🎉

Send a message to the phone number that scanned the QR code.

**Example for Restaurant Bot:**
```
User: Olá! Vocês estão abertos hoje?
Bot: Olá! 👋 Sim, estamos abertos de terça a domingo...
```

**Example for Consulting Bot:**
```
User: Preciso de consultoria para minha empresa
Bot: Entendo! Para te ajudar melhor, pode me contar...
```

## Quick Commands

```bash
# Start restaurant bot
python whatsapp_bot.py restaurant

# Start consulting bot
python whatsapp_bot.py consulting

# Using example scripts
python examples/whatsapp_restaurant_bot.py
python examples/whatsapp_consulting_bot.py

# Stop bot
Press Ctrl+C
```

## Troubleshooting

**QR code doesn't appear?**
- Check Node.js is installed: `node --version`
- Wait 10-15 seconds for dependencies to install

**Bot doesn't respond?**
- Check `.env` has valid API key
- Check rate limiting (max 10 messages/minute)
- Check logs for errors in terminal

**Connection lost?**
- Restart the bot
- May need to re-scan QR code

## Next Steps

For complete documentation, see:
- [Full WhatsApp Setup Guide](WHATSAPP_SETUP.md)
- [Security Best Practices](../SECURITY.md)

## Tips

💡 **Session persistence:** After first connection, you don't need to scan QR code again on restart

💡 **Multiple bots:** You can run multiple bots with different phone numbers

💡 **Group messages:** Currently ignored - bot only responds to individual chats

💡 **Rate limiting:** Each user limited to 10 messages per minute for safety

## Need Help?

Check the [complete WhatsApp documentation](WHATSAPP_SETUP.md) for:
- Advanced configuration
- Production deployment
- Custom agent templates
- Troubleshooting guide
