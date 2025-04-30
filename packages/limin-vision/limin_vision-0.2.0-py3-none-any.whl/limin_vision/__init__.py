import base64
from typing import Literal, Type, TypeVar
from limin import ModelConfiguration
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionUserMessageParam

DEFAULT_MODEL_CONFIGURATION = ModelConfiguration()

Detail = Literal["low", "high", "auto"]

T = TypeVar("T")


async def process_image_from_url(
    image_url: str,
    prompt: str = "What's in this image?",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
):
    """
    Process an image from a URL using a vision model.

    Args:
        image_url: URL of the image to process.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        The text response from the model.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_url, "detail": detail}},
        ],
    }

    response = await client.chat.completions.create(
        model=model_configuration.model,
        messages=[user_message],
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    return response.choices[0].message.content


async def process_image_from_url_structured(
    image_url: str,
    response_model: Type[T],
    prompt: str = "What's in this image? Respond with a JSON object.",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
) -> T:
    """
    Process an image from a URL using a vision model and return structured data.

    Args:
        image_url: URL of the image to process.
        response_model: Pydantic model class that defines the structure of the response.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        An instance of the response_model populated with the model's response.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": detail,
                },
            },
        ],
    }

    response = await client.beta.chat.completions.parse(
        model=model_configuration.model,
        messages=[user_message],
        response_format=response_model,
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    # Ensure we always return a value of type T
    if response.choices[0].message.parsed is None:
        raise ValueError("Failed to parse response into the requested model")

    return response.choices[0].message.parsed


def read_image_b64(image_path: str) -> str:
    """
    Read an image file and convert it to base64 encoding.

    Args:
        image_path: Path to the image file.

    Returns:
        Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def process_image_from_file(
    image_path: str,
    prompt: str = "What's in this image?",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
):
    """
    Process an image from a local file using a vision model.

    Args:
        image_path: Path to the image file to process.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        The text response from the model.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    base64_image = read_image_b64(image_path)

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail,
                },
            },
        ],
    }

    completion = await client.chat.completions.create(
        model=model_configuration.model,
        messages=[user_message],
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    return completion.choices[0].message.content


async def process_image_from_file_structured(
    image_path: str,
    response_model: Type[T],
    prompt: str = "What's in this image? Respond with a JSON object.",
    model_configuration: ModelConfiguration | None = None,
    detail: Detail = "auto",
) -> T:
    """
    Process an image from a local file using a vision model and return structured data.

    Args:
        image_path: Path to the image file to process.
        response_model: Pydantic model class that defines the structure of the response.
        prompt: Text prompt to send with the image.
        model_configuration: Configuration for the model to use.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        An instance of the response_model populated with the model's response.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration is None:
        model_configuration = DEFAULT_MODEL_CONFIGURATION

    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    base64_image = read_image_b64(image_path)

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": detail,
                },
            },
        ],
    }

    completion = await client.beta.chat.completions.parse(
        model=model_configuration.model,
        messages=[user_message],
        response_format=response_model,
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
    )

    # Ensure we always return a value of type T
    result = completion.choices[0].message.parsed
    if result is None:
        raise ValueError("Failed to parse response into the requested model")
    return result
