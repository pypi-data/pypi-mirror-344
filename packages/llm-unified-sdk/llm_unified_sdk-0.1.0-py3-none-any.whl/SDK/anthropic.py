from typing import Dict, List, Any, Optional

# Import the internal client (ensure name matches core.py)
from .core import UnifiedChatClient # Use the internal client name if defined in core.py

# --- Re-export Exceptions ---
from .core import SDKError, APIRequestError, ConnectionError, TimeoutError
# ----------------------------

class AnthropicClient:
    """Client specifically for interacting with Anthropic models."""
    _PROVIDER_NAME = "anthropic"

    # --- FIX: Add 'model' parameter to __init__ ---
    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None, timeout: int = 60):
        """
        Initializes the Anthropic client for a specific model.

        Args:
            base_url: Base URL of the unified FastAPI service.
            model: The specific Claude model name this client instance will use.
            api_key: Optional API key to authenticate with the FastAPI service.
            timeout: Request timeout in seconds.
        """
        self.unified_client = UnifiedChatClient(base_url, api_key, timeout)
        if not model:
            raise ValueError("An Anthropic model name must be provided.")
        self.model = model # Store the model name

    # --- FIX: Remove 'model' parameter from chat, use self.model ---
    def chat(self, messages: List[Dict[str, str]], max_tokens: Optional[int] = None, temperature: Optional[float] = None, **kwargs: Any) -> Dict[str, Any]:
        """
        Sends a chat request using the pre-configured Anthropic model.

        Args:
            messages: The list of message dictionaries.
            max_tokens: Optional maximum tokens for the response.
            temperature: Optional sampling temperature.
            **kwargs: Additional parameters. Should NOT include provider, model, or messages.

        Returns:
            The API response dictionary.
        """
        # Filter kwargs
        filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ['provider', 'model', 'messages']}

        # Use the stored model name
        return self.unified_client.chat(
            provider=self._PROVIDER_NAME,
            model=self.model, # Use the stored model
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **filtered_kwargs
        )

__all__ = ["AnthropicClient", "SDKError", "APIRequestError", "ConnectionError", "TimeoutError"]