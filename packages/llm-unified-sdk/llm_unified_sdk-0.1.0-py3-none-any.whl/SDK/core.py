import requests
import os
import json
import logging
from typing import Dict, List, Any, Optional, Union

logger = logging.getLogger(__name__)

class SDKError(Exception):
    def __init__(self, message, status_code = None, details = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details

    def __str__(self):
        if self.details:
            return f"{super().__str__()} (Status: {self.status_code}, Details: {self.details})"
        elif self.status_code: 
            return f"{super().__str__()} (Status: {self.status_code})"
        else:
            return super().__str__()

class APIRequestError(SDKError):
    pass

class ConnectionError(SDKError):
    pass

class TimeoutError(SDKError):
    pass

class UnifiedChatClient:

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 60):
        
        if not base_url:
            raise ValueError("base_url cannot be empty.")

        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        self.session.headers.update(headers)

    def chat(self, provider: str, model: str, messages: List[Dict[str, str]], max_tokens: Optional[int] = None, temperature: Optional[float] = None, **kwargs: Any) -> Dict[str, Any]:

        if not provider or not model or not messages:
            raise ValueError("`provider`, `model`, and `messages` are required arguments.")

        endpoint = f"{self.base_url}/v1/chat"

        payload: Dict[str, Any] = {
            "provider": provider,
            "model": model,
            "messages": messages,
            **({ "max_tokens": max_tokens } if max_tokens is not None else {}),
            **({ "temperature": temperature } if temperature is not None else {}),
            **kwargs
        }

        logger.debug(f"Sending request to {endpoint} with payload: {json.dumps(payload)}")

        try: 
            response = self.session.post(
                endpoint,
                json = payload,
                timeout = self.timeout
            )

            response.raise_for_status()

            try:
                response_data = response.json()
                logger.debug(f"Received successful response (Status {response.status_code})")
                return response_data
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON response from {endpoint}, even with status {response.status_code}. Response text: {response.text[:500]}...")
                raise SDKError
        
        except requests.exceptions.Timeout as e:
            logger.warning(f"Request timed out after {self.timeout}s to {endpoint}: {e}")
            raise TimeoutError(f"Request timed out to {endpoint}") from e

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error contacting {endpoint}: {e}")
            raise ConnectionError(f"Could not connect to API endpoint: {endpoint}") from e
        
        except requests.exceptions.HTTPError as e: 
            status_code = e.response.status_code
            error_details = None
            try:
                error_data = e.response.json()
                if isinstance(error_data, dict) and 'detail' in error_data:
                    error_details = error_data['detail']
                else:
                    error_details = e.response.text[:500]
            except json.JSONDecodeError:
                error_details = e.response.text[:500]

            logger.warning(f"API request failed to {endpoint} with status {status_code}. Details:  {error_details}")
            raise APIRequestError(f"API returned error status {status_code}", status_code = status_code, details = error_details) from e

        except requests.exceptions.RequestException as e:
            logger.error(f"An unexpected requests error occured contacting {endpoint}: {e}")
            raise SDKError(f"An unexpected error occurred during the API request: {e}") from e