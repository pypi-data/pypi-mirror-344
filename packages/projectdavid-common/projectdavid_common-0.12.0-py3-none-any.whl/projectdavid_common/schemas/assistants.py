from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from projectdavid_common.schemas.vectors import VectorStoreRead


# ------------------------------------------------------------------ #
#  ASSISTANT CREATE
# ------------------------------------------------------------------ #
class AssistantCreate(BaseModel):
    id: Optional[str] = Field(
        None,
        description="Unique identifier for the assistant. Optional on creation.",
    )
    name: str = Field(..., description="Name of the assistant")
    description: str = Field("", description="A brief description of the assistant")
    model: str = Field(..., description="Model used by the assistant")
    instructions: str = Field(
        "", description="Special instructions or guidelines for the assistant"
    )

    # ─── Tool definitions ───────────────────────────────────────────
    tools: Optional[List[dict]] = Field(
        None,
        description="OpenAI-style tool configs (name, description, parameters, etc.)",
    )
    platform_tools: Optional[List[Dict[str, Any]]] = Field(
        None,
        description=(
            "Inline platform tool specs, "
            "e.g. [{'type': 'file_search', 'vector_store_ids': ['vs_123']}]"
        ),
    )
    tool_resources: Optional[Dict[str, Dict[str, Any]]] = Field(  # NEW ⬅
        None,
        description=(
            "Per-tool resource map.  Example:\n"
            "{\n"
            "  'code_interpreter': { 'file_ids': ['f_abc', 'f_def'] },\n"
            "  'file_search':     { 'vector_store_ids': ['vs_123'] }\n"
            "}"
        ),
    )

    # ─── Misc settings ──────────────────────────────────────────────
    meta_data: Optional[dict] = Field(None, description="Additional metadata")
    top_p: float = Field(1.0, description="Top-p sampling parameter")
    temperature: float = Field(1.0, description="Temperature parameter")
    response_format: str = Field("auto", description="Response format")

    # ─── Webhook config ─────────────────────────────────────────────
    webhook_url: Optional[HttpUrl] = Field(
        None,
        description="URL to send 'run.action_required' webhooks to.",
        examples=["https://myapp.com/webhooks/projectdavid/actions"],
    )
    webhook_secret: Optional[str] = Field(
        None,
        min_length=16,
        description="Secret used to sign outgoing webhooks (min 16 chars).",
        examples=["whsec_MySecureS3cr3tValueF0rHMAC"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Webhook Enabled Assistant",
                "description": "Assistant configured for webhooks",
                "model": "gpt-4-turbo",
                "instructions": "Use tools when needed and await webhook callback.",
                "tools": [{"name": "get_flight_times"}],
                "platform_tools": [{"type": "file_search", "vector_store_ids": ["vs_demo_store"]}],
                "tool_resources": {
                    "code_interpreter": {"file_ids": ["f_readme_md"]},
                    "file_search": {"vector_store_ids": ["vs_demo_store"]},
                },
                "meta_data": {"project": "webhook-test"},
                "top_p": 0.9,
                "temperature": 0.7,
                "response_format": "auto",
                "webhook_url": "https://api.example.com/my-webhook-receiver",
                "webhook_secret": "whsec_ReplaceWithARealSecureSecretKey123",
            }
        }
    )


# ------------------------------------------------------------------ #
#  ASSISTANT READ
# ------------------------------------------------------------------ #
class AssistantRead(BaseModel):
    id: str = Field(..., description="Assistant ID")
    user_id: Optional[str] = Field(None, description="Owning user ID")
    object: str = Field(..., description="Object type (always 'assistant')")
    created_at: int = Field(..., description="Unix timestamp of creation")
    name: str = Field(..., description="Name")
    description: Optional[str] = Field(None, description="Description")
    model: str = Field(..., description="Model")
    instructions: Optional[str] = Field(None, description="Instructions")

    tools: Optional[List[dict]] = Field(None, description="Tool configs")
    platform_tools: Optional[List[Dict[str, Any]]] = Field(
        None, description="Inline platform tool specs"
    )
    tool_resources: Optional[Dict[str, Dict[str, Any]]] = Field(  # NEW ⬅
        None, description="Resolved resource map per tool"
    )

    meta_data: Optional[Dict[str, Any]] = Field(None, description="Metadata")
    top_p: float = Field(..., description="Top-p")
    temperature: float = Field(..., description="Temperature")
    response_format: str = Field(..., description="Response format")

    vector_stores: Optional[List[VectorStoreRead]] = Field(
        default_factory=list, description="Linked vector stores"
    )
    webhook_url: Optional[HttpUrl] = Field(None, description="Configured webhook URL (if any)")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "asst_abc123",
                "user_id": "user_xyz",
                "object": "assistant",
                "created_at": 1710000000,
                "name": "Webhook Enabled Assistant",
                "description": "Assistant configured for webhooks",
                "model": "gpt-4-turbo",
                "instructions": "Use tools when needed and await webhook callback.",
                "tools": [{"name": "get_flight_times"}],
                "platform_tools": [{"type": "file_search", "vector_store_ids": ["vs_demo_store"]}],
                "tool_resources": {
                    "code_interpreter": {"file_ids": ["f_readme_md"]},
                    "file_search": {"vector_store_ids": ["vs_demo_store"]},
                },
                "meta_data": {"department": "automation"},
                "top_p": 1.0,
                "temperature": 0.7,
                "response_format": "auto",
                "vector_stores": [],
                "webhook_url": "https://api.example.com/my-webhook-receiver",
            }
        },
    )


# ------------------------------------------------------------------ #
#  ASSISTANT UPDATE
# ------------------------------------------------------------------ #
class AssistantUpdate(BaseModel):
    name: Optional[str] = Field(None, description="New name")
    description: Optional[str] = Field(None, description="New description")
    model: Optional[str] = Field(None, description="New model")
    instructions: Optional[str] = Field(None, description="New instructions")

    tools: Optional[List[Any]] = Field(None, description="Replace tool configs")
    platform_tools: Optional[List[Dict[str, Any]]] = Field(
        None, description="Replace inline platform tool specs"
    )
    tool_resources: Optional[Dict[str, Dict[str, Any]]] = Field(  # NEW ⬅
        None, description="Replace resource map"
    )

    meta_data: Optional[Dict[str, Any]] = Field(None, description="Replace metadata")
    top_p: Optional[float] = Field(None, description="New top-p")
    temperature: Optional[float] = Field(None, description="New temperature")
    response_format: Optional[str] = Field(None, description="New response format")

    webhook_url: Optional[HttpUrl] = Field(
        None,
        description="Updated webhook URL (null to remove)",
        examples=["https://myapp.com/webhooks/new_endpoint", None],
    )
    webhook_secret: Optional[str] = Field(
        None,
        min_length=16,
        description="Updated webhook secret (provide only if changing)",
        examples=["whsec_AnotherSecureSecretKeyABC"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Assistant Name",
                "instructions": "New instructions here.",
                "tool_resources": {"code_interpreter": {"file_ids": ["f_new_readme_md"]}},
                "platform_tools": [{"type": "calculator"}],
                "webhook_url": "https://api.example.com/my-new-webhook-endpoint",
            }
        }
    )
