# limin-vision

A Python library for working with vision models.

## Installation

Install the library using pip:

```bash
pip install limin-vision
```

## Usage

After you've installed the library, you can use it by importing the `limin_vision` module and calling the functions you need.
You will also need to provide an API key for your API either by running `export OPENAI_API_KEY=$YOUR_API_KEY` or by creating an `.env` file in the root directory of your project and adding the following line:

```
OPENAI_API_KEY=$YOUR_API_KEY
```

Here is an example of how to use the library:

```python
import asyncio
from limin_vision import process_image_from_url

async def main():
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    result = await process_image_from_url(url)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

You can pass additional parameters to the `process_image_from_url` function to customize the model configuration and prompt:

```python
await process_image_from_url(
    url,
    prompt="What's in this image?",
    model_configuration=ModelConfiguration(
        model="gpt-4o",
        temperature=1.0
    ),
    detail="high",
)
```

You can find the full example in [`examples/process_from_url.py`](examples/process_from_url.py).

Alternatively, you can process an image from a local file by calling `process_image_from_file` instead of `process_image_from_url`.

```python
from limin_vision import process_image_from_file

async def main():
    result = await process_image_from_file("image.png")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

Just like with `process_image_from_url`, you can pass additional parameters to the `process_image_from_file` function to customize the model configuration and prompt:

```python
await process_image_from_file(
    "image.png",
    prompt="What's in this image?",
    model_configuration=ModelConfiguration(
        model="gpt-4o",
        temperature=1.0
    ),
    detail="high",
)
```

You can find the full example in [`examples/process_from_file.py`](examples/process_from_file.py).

You can also get a structured response from the model by passing a response model to the `process_image_from_url_structured` or `process_image_from_file_structured` functions.

For example, here's how you can process an image from a URL and get a structured response:

```python
import asyncio
from limin_vision import process_image_from_url_structured
from pydantic import BaseModel

class ImageResponse(BaseModel):
    title: str
    description: str

async def main():
    url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    result = await process_image_from_url_structured(url, ImageResponse)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

You can find the full example in [`examples/process_from_url_structured.py`](examples/process_from_url_structured.py).

You can also process an image from a local file by calling `process_image_from_file_structured` instead of `process_image_from_file`.

```python
from limin_vision import process_image_from_file_structured

async def main():
    result = await process_image_from_file_structured("image.png", ImageResponse)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

You can find the full example in [`examples/process_from_file_structured.py`](examples/process_from_file_structured.py).
