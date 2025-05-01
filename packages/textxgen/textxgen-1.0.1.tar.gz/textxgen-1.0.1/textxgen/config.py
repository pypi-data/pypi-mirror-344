# textxgen/config.py
import random
from typing import List


class Config:
    """
    Configuration class for TextxGen package.
    Stores API key, endpoints, and other configurations.
    """

    # Multiple API keys for OpenRouter
    API_KEYS = [
        "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",  # API_KEY_1
        "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",  # API_KEY_2
        "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",  # API_KEY_3
        "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",  # API_KEY_4
        "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",  # API_KEY_5
        "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",  # API_KEY_6
        "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",  # API_KEY_7
    ]

    # Base URL for OpenRouter API
    BASE_URL = "https://openrouter.ai/api/v1"

    # OpenRouter API URL
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

    # Proxy URL for the Vercel deployment
    PROXY_URL = "https://vercel-proxy-alpha-coral.vercel.app"

    # Package version
    VERSION = "1.0.0"

    # Supported models (actual model IDs)
    SUPPORTED_MODELS = {
        "llama3": "meta-llama/llama-3.1-8b-instruct:free",
        "phi3": "microsoft/phi-3-mini-128k-instruct:free",
        "deepseek": "deepseek/deepseek-chat:free",
        "qwen2_5": "qwen/qwen2.5-vl-3b-instruct:free",
        "deepseek_v3": "deepseek/deepseek-v3-base:free",
        "gemma3_4b": "google/gemma-3-4b-it:free",
        "gemma3_1b": "google/gemma-3-1b-it:free",
        "qwen3": "qwen/qwen3-14b:free",
        "deepseek_r1_t": "tngtech/deepseek-r1t-chimera:free",
        "deepcoder_14b": "agentica-org/deepcoder-14b-preview:free",
        "llama4": "meta-llama/llama-4-maverick:free",
        "qwerky_72b": "featherless/qwerky-72b:free",
        "huggingface_4": "huggingfaceh4/zephyr-7b-beta:free",
        "gpt4_1_nano": "openai/gpt-4.1-nano",
        "gpt4o_mini": "openai/gpt-4o-mini",
    }

    # Default model
    DEFAULT_MODEL = SUPPORTED_MODELS["llama3"]

    @classmethod
    def get_random_api_key(cls) -> str:
        """
        Returns a random API key from the available keys.

        Returns:
            str: A random API key
        """
        return random.choice(cls.API_KEYS)

    @classmethod
    def get_headers(cls, api_key: str = None) -> dict:
        """
        Returns headers for API requests with the specified or random API key.

        Args:
            api_key (str, optional): Specific API key to use. If None, a random key is selected.

        Returns:
            dict: Headers for API requests
        """
        key = api_key or cls.get_random_api_key()
        return {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://vercel-proxy-alpha-coral.vercel.app",
            "X-Title": "TextxGen Proxy",
        }

    @staticmethod
    def get_model_display_names() -> dict:
        """
        Returns a dictionary of model display names (without the `:free` suffix).

        Returns:
            dict: Model display names mapped to their keys.
        """
        return {
            "llama3": "LLaMA 3 (8B Instruct)",
            "phi3": "Phi-3 Mini (128K Instruct)",
            "deepseek": "DeepSeek Chat",
            "qwen2_5": "Qwen 2.5 (3B Parameters)",
            "deepseek_v3": "Deepseek Chat V3",
            "gemma3_4b": "Google Gemma 3 (4B Parameters)",
            "gemma3_1b": "Google Gemma 3 (1B Parameters)",
            "qwen3": "Qwen 3 (14B Parameters)",
            "deepseek_r1_t": "Deepseek R1-T (Chimera)",
            "deepcoder_14b": "Deepcoder (14B Parameters)",
            "llama4": "Llama 4 Maverick (17B Instruct)",
            "qwerky_72b": "Qwerky (72B Parameters)",
            "huggingface_4": "HuggingFace Zephyr (7B Parameters Beta Version)",
            "gpt4_1_nano": "OpenAI GPT 4.1 Nano",
            "gpt4o_mini": "OpenAI GPT 4o Mini",
        }
