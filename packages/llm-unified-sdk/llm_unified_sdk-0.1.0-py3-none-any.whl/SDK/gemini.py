from typing import Dict, List, Any, Optional

# Import the internal client from the core module within the same package
# Make sure this matches the actual class name in core.py (e.g., _UnifiedChatClient or UnifiedChatClient)
from .core import UnifiedChatClient # Assuming core.py defines UnifiedChatClient

# --- Import AND Re-export Exceptions ---
from .core import SDKError, APIRequestError, ConnectionError, TimeoutError
# ---------------------------------------

class GeminiClient:
    """Client specifically for interacting with Google Gemini models."""
    _PROVIDER_NAME = "google"

    # --- FIX: Add 'model' parameter to __init__ ---
    def __init__(self, base_url: str, model: str, api_key: Optional[str] = None, timeout: int = 60):
        """
        Initializes the Gemini client for a specific model.

        Args:
            base_url: Base URL of the unified FastAPI service.
            model: The specific Gemini model name this client instance will use.
            api_key: Optional API key to authenticate with the FastAPI service.
            timeout: Request timeout in seconds.
        """
        self._unified_client = UnifiedChatClient(base_url, api_key, timeout)
        if not model:
            raise ValueError("A model name must be provided for GeminiClient.")
        self.model = model # Store the model name

    # --- FIX: Remove 'model' parameter from chat, use self.model ---
    def chat(self, messages: List[Dict[str, str]], max_tokens: Optional[int] = None, temperature: Optional[float] = None, **kwargs: Any) -> Dict[str, Any]:
        """
        Sends a chat request using the pre-configured Gemini model.

        Args:
            messages: The list of message dictionaries.
            max_tokens: Optional maximum tokens for the response.
            temperature: Optional sampling temperature.
            **kwargs: Additional parameters for the API call.

        Returns:
            The API response dictionary.
        """
        # Use the stored model name
        return self._unified_client.chat(
            provider=self._PROVIDER_NAME,
            model=self.model, # Use the stored model
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )

__all__ = ["GeminiClient", "SDKError", "APIRequestError", "ConnectionError", "TimeoutError"]