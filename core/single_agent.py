"""
Chronyx Community Edition - Single Agent Implementation
"""
from typing import Dict, Optional
import logging
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from .agent_base import BaseAgent
from .validators import InputValidator, ValidationError
from .rate_limiter import RateLimiter, RateLimitExceeded
from config.settings import settings

logger = logging.getLogger(__name__)


class SingleAgent(BaseAgent):
    """Single agent implementation for Community Edition"""
    
    def __init__(
        self,
        name: str,
        description: str,
        system_prompt: str,
        knowledge_base: Optional[Dict] = None,
        max_requests_per_minute: int = 10,
        **kwargs
    ):
        super().__init__(name, description, system_prompt, **kwargs)
        self.knowledge_base = knowledge_base or {}

        # Initialize validators and rate limiter
        self.validator = InputValidator()
        self.rate_limiter = RateLimiter(
            max_requests=max_requests_per_minute,
            time_window=60
        )

        # Initialize AI client
        if settings.openai_api_key:
            client_kwargs = {"api_key": settings.openai_api_key}
            if settings.openai_base_url:
                client_kwargs["base_url"] = settings.openai_base_url
            self.client = AsyncOpenAI(**client_kwargs)
            self.provider = "openai"
        elif settings.anthropic_api_key:
            self.client = AsyncAnthropic(api_key=settings.anthropic_api_key)
            self.provider = "anthropic"
        else:
            raise ValueError("No AI provider API key configured")
    
    async def process_message(
        self,
        message: str,
        context: Optional[Dict] = None,
        user_id: str = "default"
    ) -> str:
        """Process message and generate response"""
        try:
            # Validate input
            message = self.validator.validate_message(message)
            context = self.validator.validate_context(context)

            # Check rate limit
            self.rate_limiter.check_rate_limit(user_id)

            # Sanitize message to prevent prompt injection
            safe_message = self.validator.sanitize_for_prompt(message)

            # Add user message to history
            self.add_to_history("user", safe_message)

            # Build context
            enhanced_prompt = self._build_enhanced_prompt(safe_message, context)

            # Get response from AI
            response = await self._get_ai_response(enhanced_prompt)

            # Add assistant response to history
            self.add_to_history("assistant", response)

            return response

        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            return f"Invalid input: {str(e)}"

        except RateLimitExceeded as e:
            logger.warning(f"Rate limit exceeded for user {user_id}")
            return str(e)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"I apologize, but I encountered an error processing your message. Please try again."
    
    def _build_enhanced_prompt(self, message: str, context: Optional[Dict] = None) -> str:
        """Build enhanced prompt with knowledge base and context"""
        prompt_parts = [self.system_prompt]
        
        # Add knowledge base context
        if self.knowledge_base:
            kb_context = "\n\n=== KNOWLEDGE BASE ===\n"
            for key, value in self.knowledge_base.items():
                kb_context += f"\n{key}: {value}"
            prompt_parts.append(kb_context)
        
        # Add additional context
        if context:
            ctx_str = "\n\n=== CONTEXT ===\n"
            for key, value in context.items():
                ctx_str += f"\n{key}: {value}"
            prompt_parts.append(ctx_str)
        
        # Add conversation history
        history = self.get_context_window(limit=5)
        if history:
            hist_str = "\n\n=== RECENT CONVERSATION ===\n"
            for msg in history[:-1]:  # Exclude current message
                hist_str += f"\n{msg['role'].upper()}: {msg['content']}"
            prompt_parts.append(hist_str)
        
        prompt_parts.append(f"\n\n=== CURRENT MESSAGE ===\nUSER: {message}")
        
        return "\n".join(prompt_parts)
    
    async def _get_ai_response(self, prompt: str) -> str:
        """Get response from AI provider"""
        if self.provider == "openai":
            return await self._get_openai_response(prompt)
        elif self.provider == "anthropic":
            return await self._get_anthropic_response(prompt)
    
    async def _get_openai_response(self, prompt: str) -> str:
        """Get response from OpenAI"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content.strip()
    
    async def _get_anthropic_response(self, prompt: str) -> str:
        """Get response from Anthropic Claude"""
        response = await self.client.messages.create(
            model=self.model if "claude" in self.model else "claude-3-haiku-20240307",
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
