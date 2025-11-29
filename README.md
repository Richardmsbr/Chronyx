# Chronyx Community Edition

> Open-source AI agent framework for intelligent customer service automation

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Overview

**Chronyx** is an AI-powered agent framework designed to automate customer service through intelligent, context-aware conversations. This Community Edition is fully open source under the MIT License.

### Key Features

- **Single AI Agent Framework** - Build intelligent conversational agents
- **Multi-Provider Support** - OpenAI (GPT-4), Anthropic (Claude), custom endpoints
- **WhatsApp Integration** - Connect agents to WhatsApp Web
- **Email Integration** - Automated email notifications
- **Industry Templates** - Restaurant & Consulting ready-to-use
- **Rate Limiting** - Built-in request throttling
- **Input Validation** - Security-first design with sanitization
- **Docker Ready** - One-command deployment

---

## Architecture

```
chronyx/
├── core/                    # Core framework
│   ├── agent_base.py       # Abstract base agent class
│   ├── single_agent.py     # Single agent implementation
│   ├── rate_limiter.py     # Request rate limiting
│   └── validators.py       # Input validation & sanitization
├── config/
│   └── settings.py         # Pydantic settings configuration
├── integrations/
│   ├── whatsapp/           # WhatsApp Web integration
│   └── email/              # Email service integration
├── templates/
│   ├── restaurant.py       # Restaurant business template
│   └── consulting.py       # Consulting business template
├── examples/               # Usage examples
├── tests/                  # Test suite
├── cli.py                  # Interactive CLI
└── whatsapp_bot.py         # WhatsApp bot entry point
```

---

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Runtime | Python | 3.11+ |
| AI/LLM | OpenAI, Anthropic, LangChain | Latest |
| API Framework | FastAPI | 0.112+ |
| Validation | Pydantic | 2.8+ |
| Database | SQLAlchemy + SQLite/PostgreSQL | 2.0+ |
| Async | asyncio, httpx, aiohttp | Native |
| CLI | Typer, Rich | Latest |

---

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key or Anthropic API key
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/Richardmsbr/Chronyx.git
cd Chronyx

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Run with Docker

```bash
# Build and run
docker-compose up

# Interactive mode
docker-compose run chronyx python cli.py
```

### Run Locally

```bash
# Interactive CLI
python cli.py

# With custom settings
OPENAI_API_KEY=your_key python cli.py
```

---

## Usage Examples

### Restaurant Template

```python
from templates.restaurant import RestaurantTemplate

# Create restaurant agent
agent = RestaurantTemplate.create_agent(
    restaurant_name="Sabor Premium"
)

# Process customer message
response = await agent.process_message(
    "Hi, I'd like to make a reservation for 4 people on Saturday at 8 PM"
)
print(response)
```

### Consulting Template

```python
from templates.consulting import ConsultingTemplate

# Create consulting agent
agent = ConsultingTemplate.create_agent(
    company_name="Business Pro Consulting"
)

# Qualify a lead
response = await agent.process_message(
    "We're struggling with operational efficiency"
)
print(response)
```

### Custom Agent

```python
from core.single_agent import SingleAgent

agent = SingleAgent(
    name="Support Agent",
    description="Customer support specialist",
    system_prompt="""You are a helpful customer support agent.
    Be professional, concise, and solution-oriented.""",
    model="gpt-4-turbo",
    temperature=0.7,
    max_tokens=500
)

response = await agent.process_message("I need help with my order")
```

---

## Configuration

### Environment Variables

```env
# AI Provider (at least one required)
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional, for proxies
ANTHROPIC_API_KEY=sk-ant-...

# Model Settings
DEFAULT_MODEL=gpt-4-turbo
MAX_TOKENS=500
TEMPERATURE=0.7

# Database
DATABASE_URL=sqlite:///./chronyx.db

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your@email.com

# Application
DEBUG=false
LOG_LEVEL=INFO
```

---

## API Reference

### BaseAgent

```python
class BaseAgent(ABC):
    """Abstract base class for all agents"""

    async def process_message(message: str, context: Optional[Dict]) -> str
    def add_to_history(role: str, content: str) -> None
    def get_history(limit: Optional[int]) -> List[Dict]
    def clear_history() -> None
    def get_context_window(limit: int) -> List[Dict[str, str]]
```

### SingleAgent

```python
class SingleAgent(BaseAgent):
    """Production-ready single agent implementation"""

    def __init__(
        name: str,
        description: str,
        system_prompt: str,
        knowledge_base: Optional[Dict] = None,
        max_requests_per_minute: int = 10,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 500
    )
```

### InputValidator

```python
class InputValidator:
    """Input validation and sanitization"""

    def validate_message(message: str) -> str
    def validate_context(context: Optional[Dict]) -> Optional[Dict]
    def sanitize_for_prompt(text: str) -> str
```

### RateLimiter

```python
class RateLimiter:
    """Request rate limiting per user"""

    def __init__(max_requests: int, time_window: int)
    def check_rate_limit(user_id: str) -> bool
    def reset(user_id: str) -> None
```

---

## Security

### Built-in Protections

- **Input Validation** - All inputs are validated and sanitized
- **Prompt Injection Prevention** - User inputs are escaped before LLM processing
- **Rate Limiting** - Configurable per-user request limits
- **API Key Security** - Keys loaded from environment, never logged

### Best Practices

1. Never commit `.env` files
2. Use environment variables for all secrets
3. Enable rate limiting in production
4. Review and customize system prompts for your use case
5. Monitor logs for suspicious activity

---

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=core --cov-report=html

# Specific test file
pytest tests/test_agent.py -v
```

---

## Deployment

### Docker

```bash
docker build -t chronyx .
docker run -d --env-file .env chronyx
```

### Docker Compose

```bash
docker-compose up -d
```

### Manual

```bash
# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Professional Edition

For production deployments requiring advanced features:

| Feature | Community | Professional |
|---------|-----------|--------------|
| Agent Framework | Single | Multi-agent orchestration |
| Templates | 2 | 5+ industry-specific |
| WhatsApp | Basic | Full integration |
| Dashboard | - | Real-time analytics |
| RAG System | - | Document-based knowledge |
| Calendar Integration | - | Google/Outlook |
| CRM Integration | - | HubSpot, Salesforce |
| Kubernetes | - | Production configs |
| Support | Community | Priority |

Contact: richardmsbr@gmail.com

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone and setup
git clone https://github.com/Richardmsbr/Chronyx.git
cd Chronyx
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest

# Type checking
mypy core/
```

---

## Documentation

- [Getting Started](docs/getting-started.md)
- [WhatsApp Setup](docs/WHATSAPP_SETUP.md)
- [Templates Guide](docs/templates.md)
- [Email Configuration](docs/email-setup.md)
- [API Reference](docs/api-reference.md)
- [Security Guide](SECURITY.md)

---

## License

MIT License - Free for personal and commercial use.

See [LICENSE](LICENSE) for details.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/Richardmsbr/Chronyx/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Richardmsbr/Chronyx/discussions)
- **Email**: richardmsbr@gmail.com

---

**Built by [Richard S.](https://github.com/Richardmsbr)**

*Chronyx - Intelligent Customer Service Automation*
