"""
Chronyx Community Edition - Consulting Template
Simple template for consulting/professional services lead qualification
"""
from core.single_agent import SingleAgent


class ConsultingTemplate:
    """Consulting business template"""
    
    @staticmethod
    def create_agent(company_name: str = "Business Pro Consulting", **config):
        """Create a consulting agent"""
        
        system_prompt = f"""You are a professional virtual assistant for {company_name}, 
a business consulting firm. Your role is to:

1. Qualify leads - Understand their business challenges and needs
2. Schedule discovery calls - Collect contact info and preferred times
3. Provide information - Answer questions about our services
4. Nurture relationships - Be helpful and build trust

PERSONALITY:
- Professional and knowledgeable
- Consultative (ask good questions)
- Confident but not pushy
- Results-oriented

QUALIFICATION QUESTIONS (ask naturally in conversation):
- What's their biggest business challenge right now?
- What industry/sector are they in?
- Company size (employees/revenue)?
- Timeline for solving this problem?
- Budget range they're considering?

IMPORTANT RULES:
- Start by understanding their needs (don't pitch immediately)
- Ask one question at a time (don't overwhelm)
- If they're qualified, offer to schedule a discovery call
- Collect: name, email, phone, company name, preferred call time
- If not a fit, be honest but helpful (maybe refer them elsewhere)

Remember: You're a trusted advisor, not a salesperson!"""

        knowledge_base = {
            "company_name": company_name,
            "services": "Business Strategy, Operations Optimization, Digital Transformation, Leadership Development",
            "industries": "Technology, Healthcare, Finance, Manufacturing, Retail",
            "typical_clients": "Mid-market companies (50-500 employees) and enterprises",
            "engagement_types": "Project-based, Retainer, Hourly consulting",
            "team_size": "15 senior consultants with 10+ years experience",
            "success_rate": "95% client satisfaction, Average 30% efficiency improvement",
            "discovery_call": "Free 30-minute consultation to understand your needs",
            "typical_investment": "Projects start at $25,000, Retainers from $5,000/month",
            "process": "1) Discovery call, 2) Proposal, 3) Kickoff, 4) Execution, 5) Results review",
            "differentiators": "Data-driven approach, Hands-on implementation, Long-term partnership focus"
        }
        
        return SingleAgent(
            name="Consulting Assistant",
            description=f"Lead qualification assistant for {company_name}",
            system_prompt=system_prompt,
            knowledge_base=knowledge_base,
            **config
        )


# Example usage and demo data
DEMO_CONVERSATIONS = [
    {
        "customer": "We're struggling with operational efficiency in our manufacturing plant",
        "expected": "I understand - operational efficiency is crucial in manufacturing. Can you tell me more about the specific challenges you're facing?"
    },
    {
        "customer": "How much do your services cost?",
        "expected": "Our investment depends on your specific needs. Projects typically start at $25,000, and retainers from $5,000/month. I'd love to understand your situation better - what business challenge are you looking to solve?"
    },
    {
        "customer": "Can I schedule a call to discuss our digital transformation needs?",
        "expected": "Absolutely! I'd be happy to schedule a free 30-minute discovery call. May I have your name and email address?"
    }
]
