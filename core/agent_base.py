"""
Chronyx Community Edition - Base Agent Class
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all Chronyx agents"""
    
    def __init__(
        self,
        name: str,
        description: str,
        system_prompt: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 500
    ):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history: List[Dict[str, str]] = []
        
    @abstractmethod
    async def process_message(self, message: str, context: Optional[Dict] = None) -> str:
        """Process incoming message and return response"""
        pass
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get conversation history"""
        if limit:
            return self.conversation_history[-limit:]
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_context_window(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent conversation context for LLM"""
        recent = self.conversation_history[-limit:] if len(self.conversation_history) > limit else self.conversation_history
        return [{"role": msg["role"], "content": msg["content"]} for msg in recent]
