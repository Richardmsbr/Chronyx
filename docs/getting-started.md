# Getting Started with Chronyx Community Edition

## Prerequisites

Before you begin, make sure you have:

- **Python 3.11 or higher** installed
- An **OpenAI API key** or **Anthropic API key**
- Basic knowledge of Python (helpful but not required)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/chronyx-community.git
cd chronyx-community
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

Add your API key:

```env
OPENAI_API_KEY=sk-your-key-here
```

## Quick Start

### Interactive CLI

The easiest way to get started is with the interactive CLI:

```bash
python cli.py
```

This will:
1. Show you available templates
2. Let you choose one
3. Start an interactive chat session

### Programmatic Usage

You can also use Chronyx in your own Python code:

```python
import asyncio
from templates.restaurant import RestaurantTemplate

async def main():
    # Create agent
    agent = RestaurantTemplate.create_agent(
        restaurant_name="My Restaurant"
    )
    
    # Process message
    response = await agent.process_message(
        "Hi, I'd like to make a reservation"
    )
    
    print(response)

asyncio.run(main())
```

## Using Docker

### Build and Run

```bash
# Build the image
docker-compose build

# Run interactively
docker-compose run chronyx python cli.py
```

### Run in Background

```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

## Next Steps

- [Learn about Templates](templates.md)
- [Configure Email](email-setup.md)
- [API Reference](api-reference.md)
- [Upgrade to Professional](https://chronyx.gumroad.com/pro)

## Troubleshooting

### "No API key configured"

Make sure you've set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in your `.env` file.

### "Module not found"

Make sure you've activated your virtual environment and installed dependencies:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Docker issues

Make sure Docker is running:

```bash
docker --version
docker-compose --version
```

## Need Help?

- [GitHub Issues](https://github.com/yourusername/chronyx-community/issues)
- [GitHub Discussions](https://github.com/yourusername/chronyx-community/discussions)
- Email: support@chronyx.ai
