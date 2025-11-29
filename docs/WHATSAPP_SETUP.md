# 📱 WhatsApp Integration Setup

## Overview

Chronyx agents can now respond automatically on WhatsApp using WhatsApp Web integration.

## Prerequisites

### 1. Node.js Installation

WhatsApp integration requires Node.js 18+:

```bash
# Install Node.js (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should be v18.x or higher
npm --version
```

### 2. Python Dependencies

Already included in `requirements.txt`:
- `whatsapp-web.js` (via Node.js subprocess)
- Async support

## Quick Start

### 1. Start WhatsApp Bot

```bash
# Activate virtual environment
source venv/bin/activate

# Start bot with restaurant template (default)
python whatsapp_bot.py restaurant

# Or with consulting template
python whatsapp_bot.py consulting
```

### 2. Scan QR Code

1. When you start the bot, a QR code will appear in the terminal
2. Open WhatsApp on your phone
3. Go to: **Settings → Linked Devices → Link a Device**
4. Scan the QR code displayed in terminal
5. Wait for "WhatsApp is ready!" message

### 3. Test It

Send a WhatsApp message to the phone number that scanned the QR code.

The bot will automatically respond using the configured agent template!

## Configuration

### Choose Agent Template

Edit `whatsapp_bot.py` or pass as argument:

```bash
# Restaurant agent
python whatsapp_bot.py restaurant

# Consulting agent
python whatsapp_bot.py consulting
```

### Session Management

WhatsApp sessions are stored in:
```
integrations/whatsapp/.wwebjs_auth/
```

This allows the bot to stay connected without re-scanning QR code on restart.

To reset authentication:
```bash
rm -rf integrations/whatsapp/.wwebjs_auth/
```

### Rate Limiting

Default: 10 messages per minute per user

To modify, edit in `whatsapp_bot.py`:

```python
self.agent = create_restaurant_agent()
# Agent already has rate limiting configured in core/single_agent.py
```

## How It Works

### Architecture

```
WhatsApp Message
    ↓
whatsapp-web.js (Node.js)
    ↓
WhatsAppService (Python bridge)
    ↓
WhatsAppBot (message router)
    ↓
Chronyx Agent (AI processing)
    ↓
Response sent back to WhatsApp
```

### Message Flow

1. **User sends WhatsApp message** → Received by whatsapp-web.js
2. **Bridge forwards to Python** → JSON event via stdout
3. **WhatsAppService parses event** → Calls message_handler
4. **WhatsAppBot routes to agent** → Process with AI
5. **Agent generates response** → With validation & rate limiting
6. **Response sent via bridge** → JSON command to Node.js
7. **whatsapp-web.js sends message** → Back to user on WhatsApp

## Example Usage

### Restaurant Bot

User: "Olá, vocês estão abertos?"

Bot: "Olá! 👋 Sim, estamos abertos de terça a domingo..."

### Consulting Bot

User: "Preciso melhorar a produtividade da minha empresa"

Bot: "Entendo sua necessidade de melhorar a produtividade. Para te ajudar melhor, gostaria de saber..."

## Security Features

✅ **Input Validation** - All messages validated before processing
✅ **Rate Limiting** - 10 messages/minute per user
✅ **Sanitization** - Protection against prompt injection
✅ **No API Keys in Code** - All secrets in environment variables
✅ **Session Isolation** - Each user has independent session

## Troubleshooting

### QR Code Not Appearing

```bash
# Check Node.js installation
node --version

# Check if dependencies are installed
ls integrations/whatsapp/node_modules/
```

If missing, the bot will auto-install on first run.

### Bot Not Responding

1. Check if bot is running: Look for "WhatsApp is ready!" message
2. Check logs for errors
3. Verify rate limiting not exceeded
4. Check API key is configured in `.env`

### Connection Lost

If WhatsApp disconnects:
1. Bot will log "Disconnected: [reason]"
2. Restart the bot
3. May need to re-scan QR code if session expired

### API Rate Limits

If you see "Rate limit exceeded":
- Wait 60 seconds
- User has sent >10 messages in 1 minute
- This is a security feature

## Advanced Configuration

### Custom Agent Template

Create your own agent template in `templates/`:

```python
# templates/my_template/my_agent.py
def create_my_agent():
    return SingleAgent(
        name="MyBot",
        description="Custom bot",
        system_prompt="Your custom prompt here...",
        knowledge_base={"info": "data"}
    )
```

Then use it:

```python
# In whatsapp_bot.py, add your template
elif self.template_type == "my_template":
    from templates.my_template.my_agent import create_my_agent
    self.agent = create_my_agent()
```

### Multiple Phone Numbers

Run multiple bot instances:

```bash
# Terminal 1 - Restaurant bot
python whatsapp_bot.py restaurant

# Terminal 2 - Consulting bot (different session)
python whatsapp_bot.py consulting
```

Each needs to scan a different QR code with different phones.

### Production Deployment

For production use:

1. Use process manager (PM2, systemd)
2. Set up proper logging
3. Monitor API usage
4. Regular session backups
5. Implement webhook notifications

Example with PM2:

```bash
# Install PM2
npm install -g pm2

# Start bot with PM2
pm2 start whatsapp_bot.py --interpreter python3 --name chronyx-bot

# View logs
pm2 logs chronyx-bot

# Auto-restart on reboot
pm2 startup
pm2 save
```

## Limitations

- ❌ **Not for spam** - Respect WhatsApp terms of service
- ❌ **Not for bulk messaging** - This is for conversational bots
- ❌ **Group messages ignored** - Bot only responds to individual chats
- ⚠️ **WhatsApp may ban** - If detecting automated behavior

## Resources

- [whatsapp-web.js docs](https://wwebjs.dev/)
- [WhatsApp Business Policy](https://www.whatsapp.com/legal/business-policy)
- [Chronyx Documentation](../README.md)

## Support

Issues? Check:
1. Logs in terminal output
2. SECURITY.md for best practices
3. Create issue on GitHub
