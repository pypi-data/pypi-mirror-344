from typing import Any, Literal, overload, cast
import logging

from anthropic.types import ImageBlockParam, MessageParam, TextBlockParam
from anthropic.types import Message as AnthropicMessage
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionAssistantMessageParam,
    ChatCompletionContentPartParam,
    ChatCompletionContentPartTextParam,
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from moxn.telemetry.utils import unpack_llm_response_content
from moxn_models import core
from moxn import base_models
from moxn.base_models.content import (
    ImageContentBase64,
    Author,
    MessageRole,
    Provider,
    TextContent,
    ImageContentUrl,
    get_image_representation,
    ImageBase64,
    ImageUrl,
)

OPENAI_MESSAGE_CLASSES = {
    MessageRole.SYSTEM: ChatCompletionSystemMessageParam,
    MessageRole.USER: ChatCompletionUserMessageParam,
    MessageRole.ASSISTANT: ChatCompletionAssistantMessageParam,
}


class Message(core.Message):
    @overload
    def _process_block(
        self,
        block: dict[str, Any],
        provider: Literal[Provider.ANTHROPIC],
        variables: dict[str, str | int | float | None | bool | dict],
    ) -> TextBlockParam | ImageBlockParam: ...

    @overload
    def _process_block(
        self,
        block: dict[str, Any],
        provider: Literal[Provider.OPENAI],
        variables: dict[str, str | int | float | None | bool | dict],
    ) -> ChatCompletionContentPartParam: ...

    def _process_block(
        self,
        block: dict[str, Any],
        provider: Provider,
        variables: dict[str, str | int | float | None | bool | dict],
    ) -> TextBlockParam | ImageBlockParam | ChatCompletionContentPartParam:
        """
        Process a single content block

        Handles:
        - Regular text blocks
        - Image blocks
        - Variable blocks (inline and block with complex types)
        """
        block_type = block["metadata"].get("type", "text")

        if block_type == "text":
            if provider == Provider.ANTHROPIC:
                return TextContent(text=block["content"]).to_provider_content_block(
                    Provider.ANTHROPIC,
                )
            elif provider == Provider.OPENAI:
                return TextContent(text=block["content"]).to_provider_content_block(
                    Provider.OPENAI
                )
            else:
                raise ValueError(f"Unsupported provider: {provider}")

        elif block_type == "image" and block["metadata"].get("imageData"):
            # Use the new helper method to get standardized image representation
            try:
                image_repr = get_image_representation(block)

                if provider == Provider.ANTHROPIC:
                    if isinstance(image_repr, ImageBase64):
                        return ImageContentBase64(
                            type="image_base64",
                            media_type=image_repr.media_type,
                            data=image_repr.data,
                        ).to_provider_content_block(Provider.ANTHROPIC)
                    elif isinstance(image_repr, ImageUrl):
                        return ImageContentUrl(
                            image_url=image_repr.url
                        ).to_provider_content_block(Provider.ANTHROPIC)
                    else:
                        raise ValueError(
                            f"Unsupported image representation: {image_repr}"
                        )

                elif provider == Provider.OPENAI:
                    if isinstance(image_repr, ImageBase64):
                        return ImageContentBase64(
                            type="image_base64",
                            media_type=image_repr.media_type,
                            data=image_repr.data,
                        ).to_provider_content_block(Provider.OPENAI)
                    else:  # ImageUrl
                        return ImageContentUrl(
                            image_url=image_repr.url
                        ).to_provider_content_block(Provider.OPENAI)

                else:
                    raise ValueError(f"Unsupported provider: {provider}")

            except ValueError as e:
                logging.warning(
                    f"Converting image to provider content failed: {e}. Falling back to text description if available."
                )

                # Fall back to text description if image processing fails
                if provider == Provider.ANTHROPIC:
                    return TextContent(
                        text=f"[Image: {block.get('content', 'Could not process image')}]"
                    ).to_provider_content_block(Provider.ANTHROPIC)
                elif provider == Provider.OPENAI:
                    return TextContent(
                        text=f"[Image: {block.get('content', 'Could not process image')}]"
                    ).to_provider_content_block(Provider.OPENAI)
                else:
                    raise ValueError(f"Unsupported provider: {provider}")

        elif block_type in ("variable", "variableInline", "variableBlock"):
            var_name = block["metadata"]["conf"]["name"]
            if var_name not in variables:
                raise ValueError(f"Missing required variable: {var_name}")
            var_value = variables[var_name]

            # Check if this is an image variable
            var_type = block["metadata"]["property"].get("type")

            if var_type == "image":
                var_format = (
                    block["metadata"]["property"]
                    .get("constraints", {})
                    .get("format", "")
                )

                # Handle image URL variables
                if var_format == "image-url":
                    if not isinstance(var_value, str):
                        raise ValueError(
                            f"Expected URL string for image variable {var_name}, got {type(var_value)}"
                        )

                    if provider == Provider.ANTHROPIC:
                        return ImageContentUrl(
                            image_url=var_value
                        ).to_provider_content_block(Provider.ANTHROPIC)
                    elif provider == Provider.OPENAI:
                        return ImageContentUrl(
                            image_url=var_value
                        ).to_provider_content_block(Provider.OPENAI)

                # Handle base64 image variables
                elif var_format == "image-base64":
                    if (
                        not isinstance(var_value, dict)
                        or "data" not in var_value
                        or "media_type" not in var_value
                    ):
                        raise ValueError(
                            f"Expected dict with 'data' and 'media_type' for base64 image variable {var_name}"
                        )

                    if provider == Provider.ANTHROPIC:
                        return ImageContentBase64(
                            type="image_base64",
                            media_type=var_value["media_type"],
                            data=var_value["data"],
                        ).to_provider_content_block(Provider.ANTHROPIC)
                    elif provider == Provider.OPENAI:
                        return ImageContentBase64(
                            type="image_base64",
                            media_type=var_value["media_type"],
                            data=var_value["data"],
                        ).to_provider_content_block(Provider.OPENAI)
                else:
                    raise ValueError(f"Unsupported image format: {var_format}")

            # Handle regular text variables (existing behavior)
            text = str(var_value) if var_value is not None else ""

            if provider == Provider.ANTHROPIC:
                return TextContent(text=text).to_provider_content_block(
                    Provider.ANTHROPIC
                )
            elif provider == Provider.OPENAI:
                return TextContent(text=text).to_provider_content_block(Provider.OPENAI)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        elif isinstance(block["content"], str):
            if provider == Provider.ANTHROPIC:
                return TextContent(text=block["content"]).to_provider_content_block(
                    Provider.ANTHROPIC
                )
            elif provider == Provider.OPENAI:
                return TextContent(text=block["content"]).to_provider_content_block(
                    Provider.OPENAI
                )
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    @overload
    def _reduce_blocks(
        self,
        blocks: list[TextBlockParam | ImageBlockParam],
        provider: Literal[Provider.ANTHROPIC],
    ) -> list[TextBlockParam | ImageBlockParam]: ...

    @overload
    def _reduce_blocks(
        self,
        blocks: list[ChatCompletionContentPartParam],
        provider: Literal[Provider.OPENAI],
    ) -> list[ChatCompletionContentPartParam]: ...

    def _reduce_blocks(
        self,
        blocks: (
            list[TextBlockParam | ImageBlockParam]
            | list[ChatCompletionContentPartParam]
        ),
        provider: Literal[Provider.ANTHROPIC, Provider.OPENAI],
    ) -> list[TextBlockParam | ImageBlockParam] | list[ChatCompletionContentPartParam]:
        """Collapse sequential text blocks while preserving non-text block order"""
        if not blocks:
            return blocks

        if provider == Provider.ANTHROPIC:
            anthropic_reduced: list[TextBlockParam | ImageBlockParam] = []
            current_anthropic_text: list[str] = []

            for block in blocks:
                if block["type"] == "text":
                    current_anthropic_text.append(block["text"])
                else:
                    # Non-text block encountered, flush accumulated text
                    if current_anthropic_text:
                        anthropic_reduced.append(
                            TextBlockParam(
                                text="".join(current_anthropic_text),
                                type="text",
                            )
                        )
                        current_anthropic_text = []
                    anthropic_reduced.append(cast(ImageBlockParam, block))

            # Flush any remaining text
            if current_anthropic_text:
                anthropic_reduced.append(
                    TextBlockParam(
                        text="".join(current_anthropic_text),
                        type="text",
                    )
                )

            return anthropic_reduced

        elif provider == Provider.OPENAI:
            openai_reduced: list[ChatCompletionContentPartParam] = []
            current_openai_text: list[str] = []

            for block in blocks:
                if block["type"] == "text":
                    current_openai_text.append(block["text"])
                else:
                    # Non-text block encountered, flush accumulated text
                    if current_openai_text:
                        openai_reduced.append(
                            ChatCompletionContentPartTextParam(
                                type="text", text="".join(current_openai_text)
                            )
                        )
                        current_openai_text = []
                    openai_reduced.append(cast(ChatCompletionContentPartParam, block))

            # Flush any remaining text
            if current_openai_text:
                openai_reduced.append(
                    ChatCompletionContentPartTextParam(
                        type="text", text="".join(current_openai_text)
                    )
                )

            return openai_reduced

        raise ValueError(f"Unsupported provider: {provider}")

    @overload
    def to_provider_content_blocks(
        self, provider: Literal[base_models.Provider.ANTHROPIC], variables: Any
    ) -> list[TextBlockParam | ImageBlockParam]: ...

    @overload
    def to_provider_content_blocks(
        self, provider: Literal[base_models.Provider.OPENAI], variables: Any
    ) -> list[ChatCompletionContentPartParam]: ...

    def to_provider_content_blocks(
        self, provider: Provider, variables: Any
    ) -> list[TextBlockParam | ImageBlockParam] | list[ChatCompletionContentPartParam]:
        """Convert message content to provider-specific content blocks"""

        if provider == Provider.ANTHROPIC:
            anthropic_blocks = [
                self._process_block(block, Provider.ANTHROPIC, variables)
                for block in self.blocks.get("blocks", [])
            ]
            anthropic_reduced_blocks = self._reduce_blocks(
                anthropic_blocks,
                provider=cast(Literal[Provider.ANTHROPIC], Provider.ANTHROPIC),
            )
            return cast(
                list[TextBlockParam | ImageBlockParam], anthropic_reduced_blocks
            )

        elif provider == Provider.OPENAI:
            openai_blocks = [
                self._process_block(block, Provider.OPENAI, variables)
                for block in self.blocks.get("blocks", [])
            ]
            openai_reduced_blocks = self._reduce_blocks(
                openai_blocks,
                provider=cast(Literal[Provider.OPENAI], Provider.OPENAI),
            )
            return cast(list[ChatCompletionContentPartParam], openai_reduced_blocks)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @overload
    def to_provider_message_param(
        self,
        provider: Literal[Provider.ANTHROPIC],
        role: Literal[MessageRole.SYSTEM],
        variables: dict[str, str | int | float | None | bool | dict],
    ) -> TextBlockParam: ...

    @overload
    def to_provider_message_param(
        self,
        provider: Literal[Provider.ANTHROPIC],
        role: Literal[MessageRole.USER, MessageRole.ASSISTANT],
        variables: dict[str, str | int | float | None | bool | dict],
    ) -> MessageParam: ...

    @overload
    def to_provider_message_param(
        self,
        provider: Literal[Provider.OPENAI],
        role: Literal[MessageRole.SYSTEM, MessageRole.USER, MessageRole.ASSISTANT],
        variables: dict[str, str | int | float | None | bool | dict],
    ) -> ChatCompletionMessageParam: ...

    def to_provider_message_param(
        self,
        provider: Provider,
        role: MessageRole | None = None,
        variables: dict[str, str | int | float | None | bool | dict] | None = None,
    ) -> TextBlockParam | MessageParam | ChatCompletionMessageParam:
        """
        Convert message to provider-specific message format

        Args:
            provider: The provider to format for
            role: Optional role override (uses self.role if not provided)
            **variables: Variables to substitute in the message
        """
        # Use provided role or fall back to the message's role
        effective_role = role if role is not None else self.role

        if provider == Provider.ANTHROPIC:
            content_blocks = self.to_provider_content_blocks(
                Provider.ANTHROPIC, variables
            )

            # For system role, we need to ensure we only return TextBlockParam
            if effective_role == MessageRole.SYSTEM:
                # Ensure we only have text blocks for system messages
                if len(content_blocks) != 1 or content_blocks[0]["type"] != "text":
                    # Convert all blocks to a single text block if needed
                    combined_text = "".join(
                        (
                            block["text"]
                            if block["type"] == "text"
                            else "[Image content not supported in system message]"
                        )
                        for block in content_blocks
                    )
                    return TextBlockParam(type="text", text=combined_text)
                return content_blocks[0]  # Return the single TextBlockParam
            elif effective_role in (MessageRole.USER, MessageRole.ASSISTANT):
                return MessageParam(role=effective_role.value, content=content_blocks)
            else:
                raise ValueError(f"Unsupported role for Anthropic: {effective_role}")
        elif provider == Provider.OPENAI:
            openai_content_blocks = self.to_provider_content_blocks(
                Provider.OPENAI, variables
            )
            message_class = OPENAI_MESSAGE_CLASSES.get(effective_role)
            if not message_class:
                raise ValueError(f"Unsupported role for OpenAI: {effective_role}")
            return message_class(
                role=effective_role.value, content=openai_content_blocks
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @classmethod
    def from_provider_response(
        cls,
        content: ChatCompletion | AnthropicMessage,
        provider: Provider,
        name: str,
        description: str,
        author: Author = Author.MACHINE,
        role: MessageRole = MessageRole.ASSISTANT,
    ) -> "Message":
        """Create a Message from a provider response"""

        parsed_response = unpack_llm_response_content(content, provider)
        if not parsed_response.content:
            raise ValueError("Cannot create message from empty response content")

        # Create blocks structure
        blocks = {
            "blocks": [
                {"content": parsed_response.content, "metadata": {"type": "text"}}
            ]
        }

        return cls(
            id=None,
            versionId=None,
            name=name,
            description=description,
            author=author,
            role=role,
            blocks=blocks,
        )
