#!/usr/bin/env python3
"""
Chronyx Community Edition - CLI Interface
Interactive command-line interface for testing agents
"""
import asyncio
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich import print as rprint

from templates.restaurant import RestaurantTemplate
from templates.consulting import ConsultingTemplate
from config.settings import settings

console = Console()


class ChronyxCLI:
    """Interactive CLI for Chronyx Community"""
    
    def __init__(self):
        self.agent = None
        self.template_type = None
        
    def show_banner(self):
        """Display welcome banner"""
        banner = """
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║     🌀  CHRONYX COMMUNITY EDITION  🌀                ║
║                                                       ║
║     AI Agent Platform for Business Automation        ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
        console.print("\n💡 Test your AI agents interactively!\n", style="yellow")
        
    def show_templates(self):
        """Show available templates"""
        console.print("\n📋 Available Templates:\n", style="bold")
        console.print("  1. 🍽️  Restaurant - Reservations & Menu Inquiries")
        console.print("  2. 💼 Consulting - Lead Qualification & Scheduling")
        console.print("\n")
        
    async def select_template(self):
        """Let user select a template"""
        self.show_templates()
        
        choice = Prompt.ask(
            "Select a template",
            choices=["1", "2"],
            default="1"
        )
        
        console.print()
        
        if choice == "1":
            self.template_type = "restaurant"
            restaurant_name = Prompt.ask(
                "Restaurant name",
                default="Sabor Premium"
            )
            console.print(f"\n🍽️  Creating restaurant agent for '{restaurant_name}'...\n")
            self.agent = RestaurantTemplate.create_agent(restaurant_name=restaurant_name)
            
        elif choice == "2":
            self.template_type = "consulting"
            company_name = Prompt.ask(
                "Company name",
                default="Business Pro Consulting"
            )
            console.print(f"\n💼 Creating consulting agent for '{company_name}'...\n")
            self.agent = ConsultingTemplate.create_agent(company_name=company_name)
    
    async def chat_loop(self):
        """Main chat loop"""
        console.print(Panel(
            "[bold green]Agent is ready![/bold green]\n\n"
            "💬 Start chatting below\n"
            "📝 Type 'help' for commands\n"
            "👋 Type 'quit' or 'exit' to end\n",
            title="✅ Ready",
            border_style="green"
        ))
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    console.print("\n👋 Thanks for using Chronyx! Goodbye!\n", style="yellow")
                    break
                    
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                    
                elif user_input.lower() == 'clear':
                    self.agent.clear_history()
                    console.print("\n✅ Conversation history cleared!\n", style="green")
                    continue
                    
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                # Process message
                console.print("\n[dim]Agent is thinking...[/dim]")
                response = await self.agent.process_message(user_input)
                
                # Display response
                console.print(f"\n[bold green]🤖 Agent[/bold green]\n")
                console.print(Panel(response, border_style="green"))
                
            except KeyboardInterrupt:
                console.print("\n\n👋 Interrupted. Goodbye!\n", style="yellow")
                break
            except Exception as e:
                console.print(f"\n❌ Error: {e}\n", style="red")
    
    def show_help(self):
        """Show help message"""
        help_text = """
        **Available Commands:**
        
        • `help` - Show this help message
        • `clear` - Clear conversation history
        • `history` - Show conversation history
        • `quit` or `exit` - Exit the program
        
        **Tips:**
        
        • Just type naturally to chat with the agent
        • The agent remembers your conversation
        • Use 'clear' to start fresh
        """
        console.print(Panel(Markdown(help_text), title="Help", border_style="blue"))
    
    def show_history(self):
        """Show conversation history"""
        history = self.agent.get_history()
        
        if not history:
            console.print("\n📭 No conversation history yet.\n", style="yellow")
            return
        
        console.print(f"\n📜 Conversation History ({len(history)} messages):\n", style="bold")
        
        for i, msg in enumerate(history, 1):
            role = "You" if msg["role"] == "user" else "Agent"
            style = "cyan" if msg["role"] == "user" else "green"
            console.print(f"  {i}. [{style}]{role}[/{style}]: {msg['content'][:100]}...")
        
        console.print()
    
    async def run(self):
        """Run the CLI"""
        self.show_banner()
        
        # Check API key
        if not settings.openai_api_key and not settings.anthropic_api_key:
            console.print("❌ [bold red]ERROR:[/bold red] No AI provider API key configured!\n", style="red")
            console.print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in your .env file.\n")
            console.print("Example: OPENAI_API_KEY=sk-...\n")
            return
        
        # Select template
        await self.select_template()
        
        # Start chat
        await self.chat_loop()


async def main():
    """Main entry point"""
    cli = ChronyxCLI()
    await cli.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n\n👋 Goodbye!\n", style="yellow")
        sys.exit(0)
