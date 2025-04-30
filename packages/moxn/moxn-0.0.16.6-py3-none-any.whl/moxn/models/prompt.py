from typing import (
    Literal,
    ClassVar,
    overload,
    Any,
    cast,
    Sequence,
    Optional,
    runtime_checkable,
    Protocol,
)
from uuid import UUID

from anthropic.types import Message as AnthropicMessage
from openai.types.chat import ChatCompletion
from pydantic import BaseModel, Field

from moxn import base_models
from moxn.models import message as msg
from moxn_models.content import MessageRole
from moxn.telemetry.utils import unpack_llm_response_content
from moxn.base_models.content import AnthropicMessagesParam, OpenAIMessagesParam
from moxn_models.telemetry import LLMEvent
from moxn_models import core


@runtime_checkable
class RenderableModel(Protocol):
    model_version_config: ClassVar[dict[str, Any]]

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: Any = None,
        exclude: Any = None,
        context: dict[str, Any] | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        serialize_as_any: bool = False,
    ) -> Any: ...

    def render(self, **kwargs: Any) -> Any: ...


# Add these Pydantic models for image handling
class ImageProviderOptions(BaseModel):
    mime: str
    key: str | None = None


class ImageData(BaseModel):
    format: str
    base64: str
    url: str | None = None
    providerOptions: ImageProviderOptions


class ImageMetadata(BaseModel):
    type: str
    mime: str
    key: Optional[str] = None
    src: Optional[str] = None
    imageData: ImageData


class ContentBlock(BaseModel):
    content: str
    metadata: ImageMetadata


class Prompt(core.Prompt):
    """Immutable representation of a stored prompt configuration."""

    messages: Sequence[msg.Message] = Field(default_factory=list)

    # Keep only the core data access methods
    def get_message_by_role(self, role: str | MessageRole) -> msg.Message | None:
        """Get the first message with the specified role."""
        _role = MessageRole(role) if isinstance(role, str) else role

        messages = [p for p in self.messages if p.role == role]
        if len(messages) == 1:
            return messages[0]
        elif len(messages) == 0:
            return None
        else:
            raise ValueError(
                f"get message is not deterministic, there are {len(messages)} {_role.value} messages in the prompt"
            )

    def get_messages_by_role(
        self, role: str | base_models.MessageRole
    ) -> list[msg.Message]:
        """Get all messages with the specified role."""
        role = base_models.MessageRole(role) if isinstance(role, str) else role
        return [p for p in self.messages if p.role == role]

    def get_message_by_name(self, name: str) -> msg.Message:
        """Helper to get message by name"""
        matching = [p for p in self.messages if p.name == name]
        if not matching:
            raise ValueError(f"No message found with name: {name}")
        if len(matching) > 1:
            raise ValueError(f"Multiple messages found with name: {name}")
        return matching[0]

    def _get_selected_messages(
        self,
        message_names: list[str] | None = None,
        messages: list[msg.Message] | None = None,
    ) -> list[msg.Message]:
        """Internal method to get selected messages based on various criteria."""
        if message_names:
            return [self.get_message_by_name(name) for name in message_names]
        elif messages:
            return messages
        else:
            # Use message_order if available, otherwise fall back to default role ordering
            if self.message_order:
                message_map = {str(p.id): p for p in self.messages}
                return [
                    message_map[str(pid)]
                    for pid in self.message_order
                    if str(pid) in message_map
                ]
            else:
                # Fall back to default role ordering
                selected_messages = []
                for role in [
                    base_models.MessageRole.SYSTEM,
                    base_models.MessageRole.USER,
                    base_models.MessageRole.ASSISTANT,
                ]:
                    message = self.get_message_by_role(role)
                    if message:
                        selected_messages.append(message)
                return selected_messages

    def create_instance(
        self,
        message_names: list[str] | None = None,
        messages: list[msg.Message] | None = None,
        **variables,
    ) -> "PromptInstance":
        """Create a new PromptInstance for managing runtime state."""
        return PromptInstance.from_prompt(
            self, message_names=message_names, messages=messages, **variables
        )


class PromptInstance:
    """Manages the runtime state and operations for a prompt execution."""

    def __init__(
        self,
        base_prompt: Prompt,
        selected_messages: list[msg.Message],
        input_schema: RenderableModel | None = None,
        render_kwargs: dict[str, Any] | None = None,
    ):
        self.base_prompt = base_prompt
        self.messages = selected_messages
        self.input_schema = input_schema
        self.render_kwargs = render_kwargs or {}
        self.conversation_history: list[msg.Message] = []

    @property
    def prompt_id(self) -> UUID:
        return self.base_prompt.id

    @property
    def prompt_version_id(self) -> UUID:
        return self.base_prompt.version_id

    @classmethod
    def from_prompt(
        cls,
        prompt: Prompt,
        input_schema: RenderableModel | None = None,
        render_kwargs: dict[str, Any] | None = None,
        message_names: list[str] | None = None,
        messages: list[msg.Message] | None = None,
    ) -> "PromptInstance":
        """Create a PromptInstance from a base Prompt."""
        if message_names and messages:
            raise ValueError("Cannot specify both message_names and messages")

        selected_messages = prompt._get_selected_messages(message_names, messages)
        return cls(
            base_prompt=prompt,
            input_schema=input_schema,
            render_kwargs=render_kwargs,
            selected_messages=selected_messages,
        )

    @overload
    def append_message(
        self,
        content: AnthropicMessage,
        provider: Literal[base_models.Provider.ANTHROPIC],
        name: str = "",
        description: str = "",
        author=base_models.Author.MACHINE,
        role=base_models.MessageRole.ASSISTANT,
    ) -> None: ...

    @overload
    def append_message(
        self,
        content: ChatCompletion,
        provider: Literal[base_models.Provider.OPENAI],
        name: str = "",
        description: str = "",
        author=base_models.Author.MACHINE,
        role=base_models.MessageRole.ASSISTANT,
    ) -> None: ...

    def append_message(
        self,
        content: ChatCompletion | AnthropicMessage,
        provider: base_models.Provider,
        name: str = "",
        description: str = "",
        author=base_models.Author.MACHINE,
        role=base_models.MessageRole.ASSISTANT,
    ) -> None:
        """Append a message to the conversation history."""
        new_message = msg.Message.from_provider_response(
            content=content,
            provider=provider,
            name=name,
            description=description,
            author=author,
            role=role,
        )
        self.conversation_history.append(new_message)

    def append_text(
        self,
        text: str,
        name: str = "",
        description: str = "",
        author=base_models.Author.HUMAN,
        role=base_models.MessageRole.USER,
    ) -> None:
        """
        Append a text message to the conversation history.

        Args:
            text: The text content to add
            name: Optional name for the message
            description: Optional description for the message
            author: Who created this content (default: HUMAN)
            role: The role of this content (default: USER)
        """
        # Create blocks structure for text content
        blocks = {
            "blocks": [
                {
                    "content": text,
                    "metadata": {
                        "type": "text",
                    },
                }
            ]
        }

        new_message = msg.Message(
            id=None,
            versionId=None,
            name=name,
            description=description,
            author=author,
            role=role,
            blocks=blocks,
        )
        self.conversation_history.append(new_message)

    def append_image(
        self,
        image_data: str,
        media_type: Literal["image/png", "image/jpeg"],
        image_url: str | None = None,
        key: str | None = None,
        name: str = "",
        description: str = "",
        author=base_models.Author.HUMAN,
        role=base_models.MessageRole.USER,
    ) -> None:
        """
        Append an image to the conversation history.

        Args:
            image_data: Base64-encoded image data (without the "data:image/..." prefix)
            media_type: The MIME type of the image ("image/png" or "image/jpeg")
            image_url: Optional URL to the image
            key: Optional unique identifier for the image
            name: Optional name for the message
            description: Optional description for the message
            author: Who created this content (default: HUMAN)
            role: The role of this content (default: USER)
        """
        # Format the image content as markdown
        image_markdown = "![]("
        if image_url:
            image_markdown += image_url
        image_markdown += ")\n\n"

        provider_options = ImageProviderOptions(
            mime=media_type, key=key if key else None
        )

        image_data_obj = ImageData(
            format="base64",
            base64=f"data:{media_type};base64,{image_data}",
            url=image_url,
            providerOptions=provider_options,
        )

        metadata = ImageMetadata(
            type="image",
            mime=media_type,
            key=key,
            src=image_url,
            imageData=image_data_obj,
        )

        content_block = ContentBlock(content=image_markdown, metadata=metadata)

        # Convert to dictionary for the blocks structure
        blocks = {"blocks": [content_block.model_dump(exclude_none=True)]}

        new_message = msg.Message(
            id=None,
            versionId=None,
            name=name,
            description=description,
            author=author,
            role=role,
            blocks=blocks,
        )
        self.conversation_history.append(new_message)

    def append_content(
        self,
        blocks: list[dict],
        name: str = "",
        description: str = "",
        author=base_models.Author.HUMAN,
        role=base_models.MessageRole.USER,
    ) -> None:
        """
        Append mixed content (text and/or images) to the conversation history.

        This method accepts pre-formatted blocks that match the internal block structure.
        For simpler use cases, consider using append_text() or append_image().

        Args:
            blocks: List of properly formatted content blocks
            name: Optional name for the message
            description: Optional description for the message
            author: Who created this content (default: HUMAN)
            role: The role of this content (default: USER)
        """
        # Create blocks structure
        blocks_data = {"blocks": blocks}

        new_message = msg.Message(
            id=None,
            versionId=None,
            name=name,
            description=description,
            author=author,
            role=role,
            blocks=blocks_data,
        )
        self.conversation_history.append(new_message)

    def to_openai_provider_messages(self) -> OpenAIMessagesParam:
        all_messages = self.messages + self.conversation_history
        messages = []
        for _msg in all_messages:
            if (
                _msg.role == base_models.MessageRole.SYSTEM
                or _msg.role == base_models.MessageRole.USER
                or _msg.role == base_models.MessageRole.ASSISTANT
            ):
                messages.append(
                    _msg.to_provider_message_param(
                        base_models.Provider.OPENAI,
                        role=_msg.role,
                        variables=(
                            self.input_schema.render(**self.render_kwargs)
                            if self.input_schema
                            else {}
                        ),
                    )
                )
            else:
                raise ValueError(f"Unsupported message role: {_msg.role}")

        # Create properly typed OpenAIMessagesParam
        return OpenAIMessagesParam(messages=messages)

    def to_anthropic_provider_messages(self) -> AnthropicMessagesParam:
        all_messages = self.messages + self.conversation_history

        system = []
        messages = []
        for _msg in all_messages:
            if _msg.role == base_models.MessageRole.SYSTEM:
                system.append(
                    _msg.to_provider_message_param(
                        base_models.Provider.ANTHROPIC,
                        role=_msg.role,
                        variables=(
                            self.input_schema.render(**self.render_kwargs)
                            if self.input_schema
                            else {}
                        ),
                    )
                )
            elif (
                _msg.role == base_models.MessageRole.USER
                or _msg.role == base_models.MessageRole.ASSISTANT
            ):
                messages.append(
                    _msg.to_provider_message_param(
                        base_models.Provider.ANTHROPIC,
                        role=_msg.role,
                        variables=(
                            self.input_schema.render(**self.render_kwargs)
                            if self.input_schema
                            else {}
                        ),
                    )
                )
            else:
                raise ValueError(f"Unsupported message role: {_msg.role}")
        return AnthropicMessagesParam(system=system, messages=messages)

    @overload
    def to_provider_messages(
        self,
        provider: Literal[base_models.Provider.ANTHROPIC],
    ) -> AnthropicMessagesParam: ...

    @overload
    def to_provider_messages(
        self,
        provider: Literal[base_models.Provider.OPENAI],
    ) -> OpenAIMessagesParam: ...

    def to_provider_messages(
        self,
        provider: base_models.Provider,
    ) -> AnthropicMessagesParam | OpenAIMessagesParam:
        """Convert current state to provider-specific messages."""

        if provider == base_models.Provider.ANTHROPIC:
            return self.to_anthropic_provider_messages()

        elif provider == base_models.Provider.OPENAI:
            return self.to_openai_provider_messages()

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def to_provider_payload(
        self,
        provider: base_models.Provider,
    ) -> dict[str, Any]:
        """Convert current state to provider-specific payload"""
        if provider == base_models.Provider.ANTHROPIC:
            return cast(
                dict[str, Any],
                self.to_provider_messages(base_models.Provider.ANTHROPIC).model_dump(
                    by_alias=True, mode="json"
                ),
            )
        elif provider == base_models.Provider.OPENAI:
            return cast(
                dict[str, Any],
                self.to_provider_messages(base_models.Provider.OPENAI).model_dump(
                    by_alias=True, mode="json"
                ),
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @overload
    async def _create_llm_event(
        self,
        response: AnthropicMessage,
        provider: Literal[base_models.Provider.ANTHROPIC],
        attributes: dict | None = None,
    ) -> LLMEvent: ...

    @overload
    async def _create_llm_event(
        self,
        response: ChatCompletion,
        provider: Literal[base_models.Provider.OPENAI],
        attributes: dict | None = None,
    ) -> LLMEvent: ...

    async def _create_llm_event(
        self,
        response: ChatCompletion | AnthropicMessage,
        provider: base_models.Provider,
        attributes: dict | None = None,
    ) -> LLMEvent:
        """Creates an LLM event from the current state."""
        parsed_response = unpack_llm_response_content(response, provider)
        return LLMEvent(
            messages=[
                (
                    {"id": p.id, "version_id": p.version_id}
                    if p.id
                    else p.model_dump(mode="json", by_alias=True)
                )
                for p in self.messages + self.conversation_history
            ],
            provider=provider,
            llm_response_content=parsed_response.content,
            llm_response_tool_calls=[
                tool_call.model_dump(by_alias=True)
                for tool_call in parsed_response.tool_calls
            ],
            raw_input=(
                self.input_schema.model_dump(by_alias=True)
                if self.input_schema
                else None
            ),
            rendered_input=(
                self.input_schema.render(**self.render_kwargs)
                if self.input_schema
                else None
            ),
            attributes=attributes,
        )

    async def create_llm_event(
        self,
        response: ChatCompletion | AnthropicMessage | Any,
        provider: base_models.Provider,
        attributes: dict | None = None,
    ) -> LLMEvent:
        """Creates an LLM event from the current state."""
        if not isinstance(response, (ChatCompletion, AnthropicMessage)):
            try:
                response = ChatCompletion.model_validate(response.model_dump())
            except Exception as _:
                raise ValueError(f"Unsupported response type: {type(response)}")
        if provider == base_models.Provider.OPENAI:
            assert isinstance(response, ChatCompletion)
            return await self._create_llm_event(
                response, base_models.Provider.OPENAI, attributes
            )
        elif provider == base_models.Provider.ANTHROPIC:
            assert isinstance(response, AnthropicMessage)
            return await self._create_llm_event(
                response, base_models.Provider.ANTHROPIC, attributes
            )
        else:
            raise ValueError(f"Unsupported response type: {type(response)}")
