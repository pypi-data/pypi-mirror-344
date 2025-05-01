# TextxGen

**TextxGen** is a Python package that provides a seamless interface to interact with **Large Language models** . It supports chat-based conversations and text completions using predefined models. The package is designed to be simple, modular, and easy to use, making it ideal for developers who want to integrate llm models into their applications.

---

## Features

- **Predefined API Key**: No need to provide your own API key—TextxGen uses a predefined key internally.
- **Chat and Completions**: Supports both chat-based conversations and text completions.
- **System Prompts**: Add system-level prompts to guide model interactions.
- **Error Handling**: Robust exception handling for API failures, invalid inputs, and network issues.
- **Modular Design**: Easily extendable to support additional models in the future.

---

## Installation

You can install TextxGen in one of two ways:

### Option 1: Install via `pip`

```bash
pip install textxgen
```

### Option 2: Clone the Repository

1. Clone the repository from GitHub:
   ```bash
   git clone https://github.com/Sohail-Shaikh-07/textxgen.git
   ```
2. Navigate to the project directory:
   ```bash
   cd textxgen
   ```
3. Install the package locally:
   ```bash
   pip install .
   ```

---

## Usage

### 1. Chat Example

Use the `ChatEndpoint` to interact with chat-based models.

```python
from textxgen import ChatEndpoint

def main():
    # Initialize the ChatEndpoint
    chat = ChatEndpoint()

    # Define the conversation messages
    messages = [
        {"role": "user", "content": "What is the capital of France?"},
    ]

    # Add a system prompt (optional)
    system_prompt = "You are a helpful assistant."

    # Send the chat request
    response = chat.chat(
        messages=messages,
        model="llama3",  # Use the LLaMA 3 model
        system_prompt=system_prompt,
        temperature=0.7,  # Adjust creativity
        max_tokens=100,   # Limit response length
    )

    # Format and print the response
    print("=== Chat Response ===")
    print(response["choices"][0]["message"]["content"])

if __name__ == "__main__":
    main()
```

**Output:**

```
=== Chat Response ===
The capital of France is Paris.
```

---

### 2. Completions Example

Use the `CompletionsEndpoint` to generate text completions.

```python
from textxgen import CompletionsEndpoint

def main():
    # Initialize the CompletionsEndpoint
    completions = CompletionsEndpoint()

    # Define the input prompt
    prompt = "Once upon a time"

    # Send the completion request
    response = completions.complete(
        prompt=prompt,
        model="phi3",      # Use the Phi-3 model
        temperature=0.7,   # Adjust creativity
        max_tokens=100,    # Limit response length
    )

    # Format and print the response
    print("=== Completion Response ===")
    print(response["choices"][0]["text"])

if __name__ == "__main__":
    main()
```

**Output:**

```
=== Completion Response ===
Once upon a time, in a land far, far away...
```

---

### 3. Listing Supported Models

Use the `ModelsEndpoint` to list and retrieve supported models.

```python

from textxgen import ModelsEndpoint

def main():
    """
    Example usage of the ModelsEndpoint to list and retrieve supported models.
    """
    # Initialize the ModelsEndpoint
    models = ModelsEndpoint()

    # List all supported models
    print("=== Supported Models ===")
    for model_name, display_name in models.list_display_models().items():
        print(f"{model_name}: {display_name}")


if __name__ == "__main__":
    main()

```

**Output:**

```
=== Supported Models ===
llama3: LLaMA 3 (8B Instruct)
phi3: Phi-3 Mini (128K Instruct)
deepseek: DeepSeek Chat
qwen2_5: Qwen 2.5 (3B Parameters)
deepseek_v3: Deepseek Chat V3
gemma3_4b: Google Gemma 3 (4B Parameters)
gemma3_1b: Google Gemma 3 (1B Parameters)
qwen3: Qwen 3 (14B Parameters)
deepseek_r1_t: Deepseek R1-T (Chimera)
deepcoder_14b: Deepcoder (14B Parameters)
llama4: Llama 4 Maverick (17B Instruct)
qwerky_72b: Qwerky (72B Parameters)
huggingface_4: HuggingFace Zephyr (7B Parameters Beta)
gpt4_1_nano: OpenAI GPT 4.1 Nano
gpt4o_mini: OpenAI GPT 4o Mini

```

### 4. Streaming Example

You can enable streaming for real-time responses by setting `stream=True`.

#### Chat Streaming Example

```python
from textxgen import ChatEndpoint

# Initialize the ChatEndpoint
chat = ChatEndpoint()

# Define the conversation messages
messages = [
    {"role": "user", "content": "What is the capital of France?"},
]

# Add a system prompt (optional)
system_prompt = "You are a helpful assistant."

# Send the chat request with streaming
print("=== Chat Response (Streaming) ===")
response_stream = chat.chat(
    messages=messages,
    model="llama3",
    system_prompt=system_prompt,
    temperature=0.7,
    max_tokens=100,
    stream=True,  # Enable streaming
)

# Process the streaming response
for chunk in response_stream:
    if "choices" in chunk and len(chunk["choices"]) > 0:
        content = chunk["choices"][0].get("delta", {}).get("content", "")
        if content:
            print(content, end="", flush=True)

print("\n")

```

**Output:**

```
The capital of France is Paris.
```

#### Chat Completion Example

```python
from textxgen import CompletionsEndpoint

# Initialize the CompletionsEndpoint
completions = CompletionsEndpoint()

# Define the input prompt
prompt = "Once upon a time"

# Send the completion request with streaming
print("=== Completion Response (Streaming) ===")
response_stream = completions.complete(
    prompt=prompt,
    model="phi3",
    temperature=0.7,
    max_tokens=100,
    stream=True,  # Enable streaming
)

# Process the streaming response
for chunk in response_stream:
    if "choices" in chunk and len(chunk["choices"]) > 0:
        # Extract the generated text from the response
        text = chunk["choices"][0].get("text", "")
        if text:
            print(text, end="", flush=True)

print("\n")

```

**Output:**

```
Once upon a time, in a land far, far away...
```

---

## Supported Models

TextxGen currently supports the following models:

| Model Name                              | Model ID        | Description                                                       |
| --------------------------------------- | --------------- | ----------------------------------------------------------------- |
| LLaMA 3 (8B Instruct)                   | `llama3`        | A powerful 8-billion parameter model for general-purpose tasks.   |
| Phi-3 Mini (128K Instruct)              | `phi3`          | A lightweight yet capable model optimized for efficiency.         |
| DeepSeek Chat                           | `deepseek`      | A conversational model designed for interactive chat.             |
| Qwen 2.5 (3B Parameters)                | `qwen2_5`       | A versatile 3B parameter model with vision-language capabilities. |
| DeepSeek Chat V3                        | `deepseek_v3`   | The latest version of DeepSeek's conversational model.            |
| Google Gemma 3 (4B Parameters)          | `gemma3_4b`     | Google's 4B parameter model optimized for various tasks.          |
| Google Gemma 3 (1B Parameters)          | `gemma3_1b`     | A lightweight 1B parameter version of Google's Gemma model.       |
| Qwen 3 (14B Parameters)                 | `qwen3`         | A powerful 14B parameter model for advanced tasks.                |
| DeepSeek R1-T (Chimera)                 | `deepseek_r1_t` | A specialized model from DeepSeek's R1 series.                    |
| Deepcoder (14B Parameters)              | `deepcoder_14b` | A 14B parameter model focused on coding tasks.                    |
| Llama 4 Maverick (17B Instruct)         | `llama4`        | Meta's latest 17B parameter model for instruction following.      |
| Qwerky (72B Parameters)                 | `qwerky_72b`    | A massive 72B parameter model for complex tasks.                  |
| HuggingFace Zephyr (7B Parameters Beta) | `huggingface_4` | HuggingFace's 7B parameter model in beta testing.                 |
| OpenAI GPT 4.1 Nano                     | `gpt4_1_nano`   | OpenAI's compact version of GPT 4.1.                              |
| OpenAI GPT 4o Mini                      | `gpt4o_mini`    | OpenAI's mini version of GPT 4o.                                  |
|                                         |

---

## Error Handling

TextxGen provides robust error handling for common issues:

- **Invalid Input**: Raised when invalid input is provided (e.g., empty messages or prompts).
- **API Errors**: Raised when the API returns an error (e.g., network issues or invalid requests).
- **Unsupported Models**: Raised when an unsupported model is requested.

**Example:**

```python
from textxgen.exceptions import InvalidInputError

try:
    response = chat.chat(messages=[])
except InvalidInputError as e:
    print("Error:", str(e))
```

---

## Contributing

Contributions are welcome! To contribute to TextxGen:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## License

TextxGen is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Buy Me a Coffee

If you find TextxGen useful and would like to support its development, you can buy me a coffee! Your support helps maintain and improve the project.

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sohails07)

---

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/Sohail-Shaikh-07/textxgen).
