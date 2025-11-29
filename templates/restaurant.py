"""
Chronyx Community Edition - Restaurant Template
Simple template for restaurant reservations and menu inquiries
"""
from core.single_agent import SingleAgent


class RestaurantTemplate:
    """Restaurant business template"""
    
    @staticmethod
    def create_agent(restaurant_name: str = "Sabor Premium", **config):
        """Create a restaurant agent"""
        
        system_prompt = f"""You are a friendly and professional virtual assistant for {restaurant_name}, 
a premium restaurant. Your role is to help customers with:

1. Menu inquiries - Answer questions about dishes, ingredients, prices
2. Reservation requests - Collect name, date, time, number of guests
3. Operating hours - Provide information about when we're open
4. Special requests - Note dietary restrictions, allergies, celebrations

PERSONALITY:
- Warm and welcoming
- Professional but not stiff
- Enthusiastic about our food
- Helpful and patient

IMPORTANT RULES:
- Always greet customers warmly
- If they want to make a reservation, collect: name, date, time, number of guests
- For menu questions, be descriptive and appetizing
- If you don't know something, say you'll check with the manager
- End conversations by thanking them and inviting them to visit

Remember: You're representing a premium dining experience!"""

        knowledge_base = {
            "restaurant_name": restaurant_name,
            "cuisine": "Contemporary Brazilian with international influences",
            "operating_hours": "Tuesday to Sunday, 12:00 PM - 11:00 PM (Closed Mondays)",
            "location": "Downtown, Main Street 123",
            "phone": "+55 11 1234-5678",
            "email": "reservations@saborpremium.com",
            "average_price": "R$ 120-180 per person",
            "specialties": "Grilled meats, Fresh seafood, Homemade pasta, Premium wines",
            "capacity": "80 guests",
            "accepts": "Reservations recommended, Walk-ins welcome (subject to availability)",
            "payment": "Cash, Credit cards, Debit cards, Pix",
            "features": "Air-conditioned, Live music on weekends, Private room available, Parking"
        }
        
        return SingleAgent(
            name="Restaurant Assistant",
            description=f"Virtual assistant for {restaurant_name}",
            system_prompt=system_prompt,
            knowledge_base=knowledge_base,
            **config
        )


# Example usage and demo data
DEMO_CONVERSATIONS = [
    {
        "customer": "Hi, are you open on Mondays?",
        "expected": "We're closed on Mondays, but we're open Tuesday to Sunday from 12:00 PM to 11:00 PM!"
    },
    {
        "customer": "I'd like to make a reservation for 4 people this Saturday at 8 PM",
        "expected": "Wonderful! I'd be happy to help with that reservation. May I have your name please?"
    },
    {
        "customer": "What's your specialty?",
        "expected": "Our specialties include grilled meats, fresh seafood, homemade pasta, and premium wines!"
    }
]
