"""
Chronyx Community Edition - Basic Usage Example
"""
import asyncio
from templates.restaurant import RestaurantTemplate
from templates.consulting import ConsultingTemplate


async def restaurant_example():
    """Example: Restaurant agent"""
    print("\n" + "="*60)
    print("🍽️  RESTAURANT AGENT EXAMPLE")
    print("="*60 + "\n")
    
    # Create agent
    agent = RestaurantTemplate.create_agent(restaurant_name="Sabor Premium")
    
    # Simulate conversation
    messages = [
        "Hi, are you open on Mondays?",
        "What time do you close on weekends?",
        "I'd like to make a reservation for 4 people this Saturday at 8 PM",
        "My name is John Smith"
    ]
    
    for msg in messages:
        print(f"👤 Customer: {msg}")
        response = await agent.process_message(msg)
        print(f"🤖 Agent: {response}\n")


async def consulting_example():
    """Example: Consulting agent"""
    print("\n" + "="*60)
    print("💼 CONSULTING AGENT EXAMPLE")
    print("="*60 + "\n")
    
    # Create agent
    agent = ConsultingTemplate.create_agent(company_name="Business Pro Consulting")
    
    # Simulate conversation
    messages = [
        "We're struggling with operational efficiency in our manufacturing plant",
        "We have about 200 employees and revenue around $50M",
        "We'd like to solve this in the next 3-6 months",
        "Yes, I'd like to schedule a discovery call"
    ]
    
    for msg in messages:
        print(f"👤 Lead: {msg}")
        response = await agent.process_message(msg)
        print(f"🤖 Agent: {response}\n")


async def main():
    """Run examples"""
    print("\n🌀 CHRONYX COMMUNITY EDITION - EXAMPLES\n")
    
    # Run restaurant example
    await restaurant_example()
    
    # Run consulting example
    await consulting_example()
    
    print("="*60)
    print("✅ Examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
