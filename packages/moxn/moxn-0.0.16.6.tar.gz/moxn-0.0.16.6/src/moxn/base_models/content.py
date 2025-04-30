from typing import Literal, overload, Any, cast

from anthropic.types import ImageBlockParam, MessageParam, TextBlockParam
from openai.types.chat import (
    ChatCompletionContentPartImageParam,
    ChatCompletionMessageParam,
)
from openai.types.chat.chat_completion_content_part_image_param import ImageURL
from openai.types.chat.chat_completion_content_part_text_param import (
    ChatCompletionContentPartTextParam,
)
from pydantic import BaseModel, Field
from moxn_models.content import Author, MessageRole, Provider  # tpe: ignore
from moxn_models.utils import infer_image_mime

_ = MessageRole
__ = Author

IMAGE_MEDIA_TYPES = Literal[
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
]

IMAGE_MEDIA_TYPES_VALUES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


class BaseContent(BaseModel):
    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.ANTHROPIC]
    ) -> TextBlockParam | ImageBlockParam: ...

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.OPENAI]
    ) -> ChatCompletionContentPartTextParam | ChatCompletionContentPartImageParam: ...

    def to_provider_content_block(self, provider: Provider):
        raise NotImplementedError


class TextContent(BaseContent):
    text: str

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.ANTHROPIC]
    ) -> TextBlockParam: ...

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.OPENAI]
    ) -> ChatCompletionContentPartTextParam: ...

    def to_provider_content_block(
        self, provider: Provider
    ) -> TextBlockParam | ChatCompletionContentPartTextParam:
        if provider == Provider.ANTHROPIC:
            return TextBlockParam(type="text", text=self.text)
        elif provider == Provider.OPENAI:
            return ChatCompletionContentPartTextParam(type="text", text=self.text)


class ImageContentUrl(BaseContent):
    image_url: str

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.ANTHROPIC]
    ) -> ImageBlockParam: ...

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.OPENAI]
    ) -> ChatCompletionContentPartImageParam: ...

    def to_provider_content_block(
        self, provider: Provider
    ) -> ChatCompletionContentPartImageParam | ImageBlockParam:
        if provider == Provider.ANTHROPIC:
            return ImageBlockParam(
                source={"type": "url", "url": self.image_url},
                type="image",
            )
        elif provider == Provider.OPENAI:
            return ChatCompletionContentPartImageParam(
                image_url=ImageURL(url=self.image_url, detail="auto"),
                type="image_url",
            )


class ImageContentBase64(BaseContent):
    type: Literal["image_base64"]
    media_type: IMAGE_MEDIA_TYPES
    data: str

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.ANTHROPIC]
    ) -> ImageBlockParam: ...

    @overload
    def to_provider_content_block(
        self, provider: Literal[Provider.OPENAI]
    ) -> ChatCompletionContentPartImageParam: ...

    def to_provider_content_block(
        self, provider: Provider
    ) -> ChatCompletionContentPartImageParam | ImageBlockParam:
        if provider == Provider.ANTHROPIC:
            return ImageBlockParam(
                source={
                    "type": "base64",
                    "media_type": self.media_type,
                    "data": self.data,
                },
                type="image",
            )
        elif provider == Provider.OPENAI:
            return ChatCompletionContentPartImageParam(
                image_url=ImageURL(
                    url=f"data:{self.media_type};base64,{self.data}", detail="auto"
                ),
                type="image_url",
            )


class ProviderMessagesParam(BaseModel):
    """Base class for provider-specific message parameters"""

    pass


class OpenAIMessagesParam(ProviderMessagesParam):
    messages: list[ChatCompletionMessageParam]


class AnthropicMessagesParam(ProviderMessagesParam):
    system: str | list[TextBlockParam] | None = None
    messages: list[MessageParam]


class ImageFormat(BaseModel):
    """Base class for image format information"""

    media_type: IMAGE_MEDIA_TYPES

    @classmethod
    def infer_media_type(
        cls, content: str, media_type: IMAGE_MEDIA_TYPES | None = None
    ) -> "ImageFormat":
        """Infer the media type of an image"""
        if media_type is None:
            inferred_mime = infer_image_mime(content)
            if inferred_mime is None or inferred_mime not in IMAGE_MEDIA_TYPES_VALUES:
                raise ValueError("Unsupported image format")
            _media_type = cast(IMAGE_MEDIA_TYPES, inferred_mime)
        else:
            _media_type = media_type
        return cls(media_type=_media_type)


class ImageBase64(ImageFormat):
    """Base64 encoded image data"""

    type: Literal["image_base64"] = "image_base64"
    data: str

    @classmethod
    def infer_media_type(
        cls, content: str, media_type: IMAGE_MEDIA_TYPES | None = None
    ) -> "ImageBase64":
        """Infer the media type of an image"""
        if media_type is None:
            inferred_mime = infer_image_mime(content)
            if inferred_mime is None or inferred_mime not in IMAGE_MEDIA_TYPES_VALUES:
                raise ValueError("Unsupported image format")
            _media_type = cast(IMAGE_MEDIA_TYPES, inferred_mime)
        else:
            _media_type = media_type
        return cls(media_type=_media_type, data=content)


class ImageUrl(ImageFormat):
    """URL reference to an image"""

    type: Literal["image_url"] = "image_url"
    url: str
    # Optional authentication or access metadata
    auth_metadata: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def infer_media_type(
        cls, content: str, media_type: IMAGE_MEDIA_TYPES | None = None
    ) -> "ImageUrl":
        """Infer the media type of an image"""
        if media_type is None:
            inferred_mime = infer_image_mime(content)
            if inferred_mime is None or inferred_mime not in IMAGE_MEDIA_TYPES_VALUES:
                raise ValueError("Unsupported image format")
            _media_type = cast(IMAGE_MEDIA_TYPES, inferred_mime)
        else:
            _media_type = media_type
        return cls(media_type=_media_type, url=content)


def get_image_representation(block_data: dict[str, Any]) -> ImageBase64 | ImageUrl:
    """
    Extract standardized image representation from a block

    Args:
        block_data: The block data containing image information

    Returns:
        Standardized ImageBase64 or ImageUrl representation based on the format
    """
    image_data = block_data.get("metadata", {}).get("imageData", {})

    # Get the format explicitly
    image_format = image_data.get("format", "")

    has_url = bool(image_data.get("url"))
    has_base64 = bool(image_data.get("base64"))

    # Extract media type
    media_type = image_data.get("providerOptions", {}).get("mime")
    if not media_type:
        media_type = block_data.get("metadata", {}).get("mime")

    if not media_type:
        raise ValueError("Missing media type for image")

    # Validate media type
    if media_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
        raise ValueError(f"Unsupported image format: {media_type}")

    # Choose representation based on the format
    if image_format == "image-url" and has_url:
        return ImageUrl(url=image_data["url"], media_type=media_type)
    elif image_format == "image-base64" and has_base64:
        # Strip the data URI prefix if present
        base64_data = image_data["base64"]
        if base64_data.startswith(f"data:{media_type};base64,"):
            base64_data = base64_data.split(",", 1)[1]

        return ImageBase64(data=base64_data, media_type=media_type)
    else:
        # If format doesn't match what we have, fall back to what's available
        if has_url:
            return ImageUrl(url=image_data["url"], media_type=media_type)
        elif has_base64:
            base64_data = image_data["base64"]
            if base64_data.startswith(f"data:{media_type};base64,"):
                base64_data = base64_data.split(",", 1)[1]

            return ImageBase64(data=base64_data, media_type=media_type)
        else:
            raise ValueError("No valid image representation found")
