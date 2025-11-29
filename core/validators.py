"""
Input validation for Chronyx agents
"""
from typing import Dict, Optional
import re


class ValidationError(Exception):
    """Custom validation error"""
    pass


class InputValidator:
    """Validate user inputs"""

    # Configuration
    MAX_MESSAGE_LENGTH = 2000
    MIN_MESSAGE_LENGTH = 1
    MAX_CONTEXT_SIZE = 10000

    @staticmethod
    def validate_message(message: str) -> str:
        """
        Validate and sanitize user message

        Args:
            message: User input message

        Returns:
            Sanitized message

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(message, str):
            raise ValidationError("Message must be a string")

        # Strip whitespace
        message = message.strip()

        # Check length
        if len(message) < InputValidator.MIN_MESSAGE_LENGTH:
            raise ValidationError("Message cannot be empty")

        if len(message) > InputValidator.MAX_MESSAGE_LENGTH:
            raise ValidationError(
                f"Message too long. Maximum {InputValidator.MAX_MESSAGE_LENGTH} characters"
            )

        # Basic sanitization - remove control characters
        message = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', message)

        return message

    @staticmethod
    def validate_context(context: Optional[Dict]) -> Optional[Dict]:
        """
        Validate context dictionary

        Args:
            context: Context data

        Returns:
            Validated context

        Raises:
            ValidationError: If validation fails
        """
        if context is None:
            return None

        if not isinstance(context, dict):
            raise ValidationError("Context must be a dictionary")

        # Check total size
        import json
        context_str = json.dumps(context)
        if len(context_str) > InputValidator.MAX_CONTEXT_SIZE:
            raise ValidationError(
                f"Context too large. Maximum {InputValidator.MAX_CONTEXT_SIZE} characters"
            )

        return context

    @staticmethod
    def sanitize_for_prompt(text: str) -> str:
        """
        Sanitize text for use in prompts (prevent prompt injection)

        Args:
            text: Text to sanitize

        Returns:
            Sanitized text
        """
        # Remove potential prompt injection attempts
        dangerous_patterns = [
            r'<\|im_start\|>',
            r'<\|im_end\|>',
            r'###\s*System:',
            r'###\s*Assistant:',
            r'###\s*User:',
        ]

        for pattern in dangerous_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        return text
