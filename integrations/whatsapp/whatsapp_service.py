"""
WhatsApp Service - Integration with WhatsApp Web
Uses whatsapp-web.js via subprocess bridge
"""
import asyncio
import json
import logging
from typing import Optional, Dict, Callable
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)


class WhatsAppService:
    """WhatsApp integration service"""

    def __init__(
        self,
        session_name: str = "chronyx-whatsapp",
        message_handler: Optional[Callable] = None
    ):
        """
        Initialize WhatsApp service

        Args:
            session_name: Session name for WhatsApp auth
            message_handler: Async callback for processing messages
        """
        self.session_name = session_name
        self.message_handler = message_handler
        self.is_ready = False
        self.qr_code = None
        self.client_info = None
        self.process = None

    async def start(self):
        """Start WhatsApp client"""
        logger.info("Starting WhatsApp service...")

        # Check if Node.js is installed
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True
            )
            logger.info(f"Node.js version: {result.stdout.strip()}")
        except FileNotFoundError:
            raise RuntimeError(
                "Node.js is not installed. Please install Node.js first:\n"
                "  curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -\n"
                "  sudo apt-get install -y nodejs"
            )

        # Check if whatsapp-web.js is installed
        node_modules = Path("integrations/whatsapp/node_modules")
        if not node_modules.exists():
            logger.info("Installing whatsapp-web.js dependencies...")
            await self._install_dependencies()

        # Start the WhatsApp bridge
        await self._start_bridge()

    async def _install_dependencies(self):
        """Install Node.js dependencies"""
        package_json = Path("integrations/whatsapp/package.json")

        if not package_json.exists():
            # Create package.json
            package_data = {
                "name": "chronyx-whatsapp",
                "version": "1.0.0",
                "description": "WhatsApp integration for Chronyx",
                "dependencies": {
                    "whatsapp-web.js": "^1.23.0",
                    "qrcode-terminal": "^0.12.0"
                }
            }

            with open(package_json, "w") as f:
                json.dump(package_data, f, indent=2)

        # Run npm install
        process = await asyncio.create_subprocess_exec(
            "npm", "install",
            cwd="integrations/whatsapp",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"Failed to install dependencies: {stderr.decode()}")

        logger.info("Dependencies installed successfully")

    async def _start_bridge(self):
        """Start Node.js bridge process"""
        bridge_script = Path("integrations/whatsapp/bridge.js")

        if not bridge_script.exists():
            # Create bridge script
            self._create_bridge_script()

        # Start Node.js process
        self.process = await asyncio.create_subprocess_exec(
            "node", str(bridge_script),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="integrations/whatsapp"
        )

        # Start reading output
        asyncio.create_task(self._read_output())

        logger.info("WhatsApp bridge started")

    def _create_bridge_script(self):
        """Create Node.js bridge script"""
        script_content = """
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
    authStrategy: new LocalAuth({
        clientId: 'chronyx-session'
    }),
    puppeteer: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Send events to Python via stdout
function sendEvent(type, data) {
    console.log(JSON.stringify({ type, data }));
}

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    sendEvent('qr', { qr });
});

client.on('ready', () => {
    sendEvent('ready', { message: 'WhatsApp is ready!' });
});

client.on('authenticated', () => {
    sendEvent('authenticated', { message: 'Authenticated successfully' });
});

client.on('auth_failure', (msg) => {
    sendEvent('auth_failure', { error: msg });
});

client.on('disconnected', (reason) => {
    sendEvent('disconnected', { reason });
});

client.on('message', async (message) => {
    sendEvent('message', {
        from: message.from,
        body: message.body,
        timestamp: message.timestamp,
        isGroup: message.from.includes('@g.us')
    });
});

// Handle commands from Python via stdin
process.stdin.on('data', async (data) => {
    try {
        const command = JSON.parse(data.toString());

        if (command.type === 'send_message') {
            await client.sendMessage(command.to, command.message);
            sendEvent('message_sent', { to: command.to, success: true });
        }
    } catch (error) {
        sendEvent('error', { error: error.message });
    }
});

client.initialize();

process.on('SIGTERM', () => {
    client.destroy();
    process.exit(0);
});
"""

        with open("integrations/whatsapp/bridge.js", "w") as f:
            f.write(script_content)

        logger.info("Bridge script created")

    async def _read_output(self):
        """Read output from Node.js process"""
        if not self.process or not self.process.stdout:
            return

        while True:
            try:
                line = await self.process.stdout.readline()
                if not line:
                    break

                data = line.decode().strip()
                if not data:
                    continue

                # Try to parse as JSON event
                try:
                    event = json.loads(data)
                    await self._handle_event(event)
                except json.JSONDecodeError:
                    # Not JSON, just log it
                    logger.info(f"WhatsApp: {data}")

            except Exception as e:
                logger.error(f"Error reading output: {e}")
                break

    async def _handle_event(self, event: Dict):
        """Handle events from WhatsApp"""
        event_type = event.get("type")
        data = event.get("data", {})

        if event_type == "qr":
            self.qr_code = data.get("qr")
            logger.info("QR Code received - scan with WhatsApp app")

        elif event_type == "ready":
            self.is_ready = True
            logger.info("✅ WhatsApp is ready!")

        elif event_type == "authenticated":
            logger.info("✅ Authenticated successfully")

        elif event_type == "message":
            # Handle incoming message
            if self.message_handler:
                await self.message_handler(data)

        elif event_type == "error":
            logger.error(f"WhatsApp error: {data.get('error')}")

        elif event_type == "disconnected":
            logger.warning(f"Disconnected: {data.get('reason')}")
            self.is_ready = False

    async def send_message(self, to: str, message: str):
        """
        Send message via WhatsApp

        Args:
            to: Phone number (format: 5511999999999@c.us)
            message: Message text
        """
        if not self.is_ready:
            raise RuntimeError("WhatsApp is not ready")

        if not self.process or not self.process.stdin:
            raise RuntimeError("WhatsApp bridge is not running")

        command = {
            "type": "send_message",
            "to": to,
            "message": message
        }

        self.process.stdin.write(
            (json.dumps(command) + "\n").encode()
        )
        await self.process.stdin.drain()

    async def stop(self):
        """Stop WhatsApp client"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            logger.info("WhatsApp service stopped")

    def format_phone_number(self, number: str) -> str:
        """
        Format phone number for WhatsApp

        Args:
            number: Phone number (can include country code)

        Returns:
            Formatted number (e.g., 5511999999999@c.us)
        """
        # Remove all non-digit characters
        clean_number = "".join(filter(str.isdigit, number))

        # Add Brazil country code if not present
        if not clean_number.startswith("55"):
            clean_number = "55" + clean_number

        return f"{clean_number}@c.us"
