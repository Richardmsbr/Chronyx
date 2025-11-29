"""
Rate limiting for API calls
"""
import time
from collections import deque
from typing import Dict, Optional


class RateLimitExceeded(Exception):
    """Rate limit exceeded exception"""
    pass


class RateLimiter:
    """Simple token bucket rate limiter"""

    def __init__(
        self,
        max_requests: int = 10,
        time_window: int = 60,
        burst_size: Optional[int] = None
    ):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds
            burst_size: Optional burst size (defaults to max_requests)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.burst_size = burst_size or max_requests
        self.requests: Dict[str, deque] = {}

    def check_rate_limit(self, user_id: str = "default") -> bool:
        """
        Check if request is allowed

        Args:
            user_id: Identifier for the user/client

        Returns:
            True if allowed, False if rate limited

        Raises:
            RateLimitExceeded: If rate limit is exceeded
        """
        current_time = time.time()

        # Initialize if first request
        if user_id not in self.requests:
            self.requests[user_id] = deque()

        # Remove old requests outside time window
        while (
            self.requests[user_id]
            and current_time - self.requests[user_id][0] > self.time_window
        ):
            self.requests[user_id].popleft()

        # Check if limit exceeded
        if len(self.requests[user_id]) >= self.max_requests:
            oldest_request = self.requests[user_id][0]
            wait_time = self.time_window - (current_time - oldest_request)
            raise RateLimitExceeded(
                f"Rate limit exceeded. Try again in {int(wait_time)} seconds"
            )

        # Add current request
        self.requests[user_id].append(current_time)
        return True

    def get_remaining_requests(self, user_id: str = "default") -> int:
        """
        Get remaining requests for user

        Args:
            user_id: Identifier for the user/client

        Returns:
            Number of remaining requests
        """
        if user_id not in self.requests:
            return self.max_requests

        current_time = time.time()

        # Clean old requests
        while (
            self.requests[user_id]
            and current_time - self.requests[user_id][0] > self.time_window
        ):
            self.requests[user_id].popleft()

        return max(0, self.max_requests - len(self.requests[user_id]))

    def reset(self, user_id: Optional[str] = None):
        """
        Reset rate limiter

        Args:
            user_id: Optional user ID to reset. If None, reset all.
        """
        if user_id:
            if user_id in self.requests:
                del self.requests[user_id]
        else:
            self.requests.clear()
