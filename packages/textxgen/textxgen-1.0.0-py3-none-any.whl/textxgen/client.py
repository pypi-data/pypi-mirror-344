import requests
from typing import Iterator, Dict, Any, Optional
from .exceptions import APIError, InvalidInputError
import json
import logging
from .config import Config

# Set up logger
logger = logging.getLogger(__name__)


class APIClient:
    """
    Handles API requests to the proxy server.
    """

    def __init__(self, proxy_url: Optional[str] = None):
        """
        Initialize the client.

        Args:
            proxy_url (str, optional): Custom proxy URL. Defaults to None (uses built-in config).
        """
        self.proxy_url = proxy_url or Config.PROXY_URL

        # Validate proxy URL
        if not self.proxy_url:
            raise InvalidInputError(
                "Proxy URL must be provided either through config or constructor"
            )

    def _make_request(
        self,
        endpoint: str,
        method: str = "POST",
        data: dict = None,
        stream: bool = False,
    ) -> Any:
        """
        Makes an API request to the proxy server.

        Args:
            endpoint: API endpoint (e.g., '/chat')
            method: HTTP method (default: POST)
            data: Request payload
            stream: Whether to stream the response

        Returns:
            Parsed JSON response or streaming iterator

        Raises:
            APIError: For request failures
        """
        # Construct the full URL
        url = f"{self.proxy_url.rstrip('/')}/{endpoint.lstrip('/')}"

        headers = {
            "Content-Type": "application/json",
            "X-Proxy-Request": "true",
            "User-Agent": f"TextxGen-PyPI/{Config.VERSION}",
        }

        try:
            logger.debug(f"Making {method} request to proxy: {url}")
            logger.debug(f"Request data: {json.dumps(data, indent=2)}")

            response = requests.request(
                method, url, json=data, stream=stream, headers=headers, timeout=30
            )
            response.raise_for_status()

            if stream:
                return self._handle_streaming_response(response)
            return response.json()

        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP Error: {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise APIError(error_msg, e.response.status_code)

        except requests.exceptions.RequestException as e:
            error_msg = f"Request Error: {str(e)}"
            logger.error(error_msg)
            raise APIError(error_msg, getattr(e.response, "status_code", None))

    def _handle_streaming_response(
        self, response: requests.Response
    ) -> Iterator[Dict[str, Any]]:
        """
        Handles streaming responses from the proxy server.

        Args:
            response: Streaming response object

        Yields:
            Parsed JSON chunks from the stream

        Raises:
            APIError: For parsing failures
        """
        buffer = ""
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                buffer += chunk.decode("utf-8")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.startswith("data: "):
                        json_data = line[len("data: ") :]
                        if json_data.strip() == "[DONE]":
                            return
                        try:
                            yield json.loads(json_data)
                        except json.JSONDecodeError as e:
                            error_msg = f"JSON Decode Error: {e}"
                            logger.error(error_msg)
                            raise APIError(error_msg, 500)

    def chat_completion(
        self,
        messages: list,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False,
    ) -> Any:
        """
        Sends a chat completion request to the proxy server.

        Args:
            messages: List of chat messages
            model: Model identifier (default: Config.DEFAULT_MODEL)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response

        Returns:
            API response or streaming iterator

        Raises:
            InvalidInputError: For invalid input
            APIError: For API failures
        """
        if not messages or not isinstance(messages, list):
            raise InvalidInputError("Messages must be a non-empty list.")

        payload = {
            "model": model or Config.DEFAULT_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        return self._make_request("/chat", data=payload, stream=stream)
