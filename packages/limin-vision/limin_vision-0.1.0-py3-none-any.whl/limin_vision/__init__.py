import base64
from typing import Literal
from limin import ModelConfiguration
from openai import AsyncOpenAI

DEFAULT_MODEL_CONFIGURATION = ModelConfiguration()

Detail = Literal["low", "high", "auto"]


async def process_image_from_url(
    image_url: str,
    model_configuration: ModelConfiguration = DEFAULT_MODEL_CONFIGURATION,
    prompt: str = "What's in this image?",
    detail: Detail = "auto",
):
    """
    Process an image from a URL using a vision model.

    Args:
        image_url: URL of the image to process.
        model_configuration: Configuration for the model to use.
        prompt: Text prompt to send with the image.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        The text response from the model.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    response = await client.chat.completions.create(
        model=model_configuration.model,
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
        messages=[
            {
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
        ],
    )

    return response.choices[0].message.content


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
    model_configuration: ModelConfiguration = DEFAULT_MODEL_CONFIGURATION,
    prompt: str = "What's in this image?",
    detail: Detail = "auto",
):
    """
    Process an image from a local file using a vision model.

    Args:
        image_path: Path to the image file to process.
        model_configuration: Configuration for the model to use.
        prompt: Text prompt to send with the image.
        detail: Level of detail for image processing ('low', 'high', or 'auto').

    Returns:
        The text response from the model.

    Raises:
        ValueError: If log_probs or top_log_probs are set in the model configuration.
    """
    if model_configuration.log_probs or model_configuration.top_log_probs is not None:
        raise ValueError(
            "log_probs and top_log_probs are not supported for image processing"
        )

    base64_image = read_image_b64(image_path)

    client = AsyncOpenAI(
        api_key=model_configuration.api_key,
        base_url=model_configuration.base_url,
    )

    completion = await client.chat.completions.create(
        model=model_configuration.model,
        temperature=model_configuration.temperature,
        max_tokens=model_configuration.max_tokens,
        presence_penalty=model_configuration.presence_penalty,
        frequency_penalty=model_configuration.frequency_penalty,
        top_p=model_configuration.top_p,
        seed=model_configuration.seed,
        messages=[
            {
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
        ],
    )

    return completion.choices[0].message.content
