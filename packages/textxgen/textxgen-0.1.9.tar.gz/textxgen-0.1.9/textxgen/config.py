# textxgen/config.py


class Config:
    """
    Configuration class for TextxGen package.
    Stores API key, endpoints, and other configurations.
    """

    # Predefined API key for OpenRouter
    API_KEY = (
        "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"
    )

    # Base URL for OpenRouter API
    BASE_URL = "https://openrouter.ai/api/v1"

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

    # Headers for API requests
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
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
