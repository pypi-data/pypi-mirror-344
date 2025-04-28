"""InVideo AI MCP - API client module for interacting with the InVideo AI API."""

import importlib.metadata
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel

#######################
# InVideo API Models #
#######################


# Common base response model
class BaseInVideoResponse(BaseModel):
    error: Optional[str] = None


# Topic generation models
class TopicData(BaseModel):
    topic: str
    description: Optional[str] = None


class TopicResponse(BaseInVideoResponse):
    topics: List[TopicData]


# Narrative options models
class NarrativeOption(BaseModel):
    id: str
    title: str
    description: str
    duration: int  # in seconds


class NarrativeOptionsData(BaseModel):
    options: List[NarrativeOption]


class NarrativeOptionsResponse(BaseInVideoResponse):
    data: Optional[NarrativeOptionsData] = None


# Video style models
class VideoStyle(BaseModel):
    style_id: str
    name: str
    description: str
    examples: Optional[List[str]] = None


class VideoStyleData(BaseModel):
    style: VideoStyle


class VideoStyleResponse(BaseInVideoResponse):
    data: Optional[VideoStyleData] = None


# Platform models
class Platform(BaseModel):
    platform_id: str
    name: str
    description: str
    recommended_aspect_ratios: List[str]
    recommended_durations: List[int]  # in seconds


class PlatformsData(BaseModel):
    platforms: List[Platform]


class PlatformsResponse(BaseInVideoResponse):
    data: Optional[PlatformsData] = None


# Video generation models
class VideoGenerateRequest(BaseModel):
    prompt: str
    aspect_ratio: Optional[str] = "16:9"
    callback_url: Optional[str] = None


class VideoGenerateData(BaseModel):
    video_id: str
    status: str
    estimated_time: Optional[int] = None


class VideoGenerateResponse(BaseInVideoResponse):
    data: Optional[VideoGenerateData] = None


# Video status models
class VideoStatusError(BaseModel):
    code: Optional[int] = None
    detail: Optional[str] = None
    message: Optional[str] = None


class VideoStatusData(BaseModel):
    video_id: str
    status: str  # Values: "waiting", "pending", "processing", "completed", "failed"
    progress: Optional[int] = None
    video_url: Optional[str] = None
    created_at: Optional[int] = None
    error: Optional[VideoStatusError] = None


class VideoStatusResponse(BaseInVideoResponse):
    data: Optional[VideoStatusData] = None


class MCPScriptResponse(BaseInVideoResponse):
    script: Optional[str] = None


class MCPVideoGenerateResponse(BaseInVideoResponse):
    video_id: Optional[str] = None
    status: Optional[str] = None
    estimated_time: Optional[int] = None


class MCPVideoStatusResponse(BaseInVideoResponse):
    video_id: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    video_url: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None


class MCPVideoFromScriptResponse(BaseInVideoResponse):
    video_url: Optional[str] = None
    instructions: Optional[str] = None


class MCPTopicResponse(BaseInVideoResponse):
    topic: Optional[str] = None
    description: Optional[str] = None


class MCPNarrativeOptionsResponse(BaseInVideoResponse):
    options: Optional[List[NarrativeOption]] = None


# Update the MCPIdeaResponse model class
class MCPIdeaData(BaseModel):
    topic: str
    description: str
    vibe: str  # e.g., "educational", "entertaining", "professional"
    target_audience: str


class MCPIdeasResponse(BaseInVideoResponse):
    ideas: Optional[List[MCPIdeaData]] = None


# InVideo API Client Class
class InVideoApiClient:
    """Client for interacting with the InVideo API."""

    def __init__(self, api_host: str = "http://localhost:4000"):
        """Initialize the API client with the API key and host.

        Args:
            api_host: The API host URL (defaults to InVideo API)
        """
        self.api_host = api_host

        # Set version for user agent
        try:
            self.version = importlib.metadata.version("invideo-mcp")
        except importlib.metadata.PackageNotFoundError:
            self.version = "unknown"

        self.user_agent = f"invideo-mcp/{self.version}"
        self.base_url = f"{api_host}/api"
        self._client = httpx.AsyncClient()

    async def close(self):
        """Close the underlying HTTP client."""
        await self._client.aclose()

    def _get_headers(self) -> Dict[str, str]:
        """Return the headers needed for API requests."""
        return {
            "Accept": "application/json",
            "User-Agent": self.user_agent,
        }

    async def _make_request(
        self, endpoint: str, method: str = "GET", data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a request to the specified API endpoint.

        Args:
            endpoint: The API endpoint to call (without the base URL)
            method: HTTP method to use (GET or POST)
            data: JSON payload for POST requests

        Returns:
            The JSON response from the API

        Raises:
            httpx.RequestError: If there's a network-related error
            httpx.HTTPStatusError: If the API returns an error status code
            Exception: For any other unexpected errors
        """
        url = f"{self.base_url}/{endpoint}"
        headers = self._get_headers()

        if method.upper() == "GET":
            response = await self._client.get(url, headers=headers, timeout=60.0)
        elif method.upper() == "POST":
            headers["Content-Type"] = "application/json"
            response = await self._client.post(
                url, headers=headers, json=data, timeout=60.0
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()  # Raises if status code is 4xx or 5xx
        return response.json()

    async def _handle_api_request(
        self,
        api_call,
        response_model_class,
        mcp_response_class,
        error_msg: str,
        **kwargs,
    ):
        """Generic handler for API requests to reduce code duplication.

        Args:
            api_call: Async function to call the API
            response_model_class: Pydantic model class for validating the API response
            mcp_response_class: Pydantic model class for the MCP response
            error_msg: Error message to return if the validation fails
            **kwargs: Additional arguments for the response transformation

        Returns:
            An MCP response object
        """
        try:
            # Make the request to the API
            result = await api_call()

            # Validate the response
            validated_response = response_model_class.model_validate(result)

            # Return the appropriate response based on the validation result
            if hasattr(validated_response, "data") and validated_response.data:
                return self._transform_to_mcp_response(
                    validated_response.data, mcp_response_class, **kwargs
                )
            elif validated_response.error:
                return mcp_response_class(error=validated_response.error)
            else:
                return mcp_response_class(error=error_msg)

        except httpx.RequestError as exc:
            return mcp_response_class(error=f"HTTP Request failed: {exc}")
        except httpx.HTTPStatusError as exc:
            return mcp_response_class(
                error=f"HTTP Error: {exc.response.status_code} - {exc.response.text}"
            )
        except Exception as e:
            return mcp_response_class(error=f"An unexpected error occurred: {e}")

    def _transform_to_mcp_response(self, data, mcp_response_class, **kwargs):
        """Transform API response data to MCP response format.

        Args:
            data: The API response data
            mcp_response_class: The MCP response class to instantiate
            **kwargs: Additional parameters for the response

        Returns:
            An instance of the MCP response class
        """
        if "transform_func" in kwargs:
            # Use the provided transform function
            transform_func = kwargs.pop("transform_func")
            return transform_func(data, mcp_response_class)

        # Apply lambda functions to data if provided or use direct values
        processed_kwargs = {}
        for key, value in kwargs.items():
            if callable(value):
                processed_kwargs[key] = value(data)
            else:
                processed_kwargs[key] = value

        return mcp_response_class(**processed_kwargs)

    async def generate_topic(self, category: Optional[str] = None) -> MCPTopicResponse:
        """Generate a video topic idea based on an optional category.

        Args:
            category: Optional category to generate a topic for (e.g., "technology", "education")

        Returns:
            A response containing a topic and description
        """

        async def api_call():
            endpoint = "/mcp-server/topic"
            params = {}
            if category:
                params = {"category": category}
            return await self._make_request(endpoint, method="POST", data=params)

        def transform_data(data, mcp_class):
            return mcp_class(topic=data.topic, description=data.description)

        return await self._handle_api_request(
            api_call=api_call,
            response_model_class=TopicResponse,
            mcp_response_class=MCPTopicResponse,
            error_msg="Failed to generate a topic.",
            transform_func=transform_data,
        )

    async def generate_narrative_options(
        self,
        topic: str,
        platform: str = "youtube_shorts",
        duration_range: str = "30-60",
    ) -> MCPNarrativeOptionsResponse:
        """Generate multiple narrative options for a given topic.

        Args:
            topic: The main topic of the video
            platform: The target platform (defaults to YouTube Shorts)
            duration_range: Desired duration range in seconds (defaults to 30-60 seconds)

        Returns:
            A response containing multiple narrative options with titles, descriptions and durations
        """

        async def api_call():
            endpoint = "/mcp-server/narrative-options"
            data = {
                "topic": topic,
                "platform": platform,
                "duration_range": duration_range,
            }
            return await self._make_request(endpoint, method="POST", data=data)

        def transform_data(data, mcp_class):
            return mcp_class(options=data.options)

        return await self._handle_api_request(
            api_call=api_call,
            response_model_class=NarrativeOptionsResponse,
            mcp_response_class=MCPNarrativeOptionsResponse,
            error_msg="Failed to generate narrative options.",
            transform_func=transform_data,
        )

    async def generate_content_ideas(
        self, platform_conversation_starter: str
    ) -> MCPIdeasResponse:
        """Generate content ideas for a specific platform with topic, vibe, and target audience suggestions.

        Args:
            platform_conversation_starter: A conversation starter that includes the intended video platform
                (e.g., YouTube, Instagram, TikTok) and the initial context or intent for video creation.

        Returns:
            A response containing multiple content ideas with topics, vibes, and target audiences
        """

        async def api_call():
            endpoint = "/mcp-server/generate/content-ideas"
            data = {
                "conversation_starter": platform_conversation_starter,
            }
            return await self._make_request(endpoint, method="POST", data=data)

        try:
            # Make the API request
            result = await api_call()

            # Create the response with the ideas
            # Note: We're assuming the API returns ideas in the expected format
            return MCPIdeasResponse(ideas=result.get("content_ideas", []))

        except httpx.RequestError as exc:
            return MCPIdeasResponse(error=f"HTTP Request failed: {exc}")
        except httpx.HTTPStatusError as exc:
            return MCPIdeasResponse(
                error=f"HTTP Error: {exc.response.status_code} - {exc.response.text}"
            )
        except Exception as e:
            return MCPIdeasResponse(error=f"An unexpected error occurred: {e}")

    async def generate_script(
        self, topic: str, vibe: str, target_audience: str
    ) -> MCPScriptResponse:
        """Generate a video script based on topic, vibe, and target audience.

        Args:
            topic: The main topic of the video
            vibe: The vibe/tone of the video (e.g., "educational", "entertaining", "professional")
            target_audience: The target audience for the video

        Returns:
            A response containing the generated script and prompt
        """

        async def api_call():
            endpoint = "/mcp-server/generate/script"
            data = {
                "topic": topic,
                "vibe": vibe,
                "target_audience": target_audience,
            }
            return await self._make_request(endpoint, method="POST", data=data)

        try:
            # Make the API request
            result = await api_call()

            # Create the response with the script
            return MCPScriptResponse(script=result.get("script"))

        except httpx.RequestError as exc:
            return MCPScriptResponse(error=f"HTTP Request failed: {exc}")
        except httpx.HTTPStatusError as exc:
            return MCPScriptResponse(
                error=f"HTTP Error: {exc.response.status_code} - {exc.response.text}"
            )
        except Exception as e:
            return MCPScriptResponse(error=f"An unexpected error occurred: {e}")

    async def generate_video_from_script(
        self, script: str, topic: str, vibe: str, target_audience: str, platform: str
    ) -> MCPVideoFromScriptResponse:
        """Generate a video from a script with the given topic, vibe, and target audience.

        Args:
            script: The video script content
            topic: The main topic of the video
            vibe: The vibe/tone of the video (e.g., "educational", "entertaining", "professional")
            target_audience: The target audience for the video

        Returns:
            A response containing the video ID, status, estimated time, and instructions
        """

        async def api_call():
            endpoint = "/copilot/request/mcp-server/new-from-script"
            data = {
                "script": script,
                "title": topic,
                "vibe": vibe,
                "target_audience": target_audience,
                "platform": platform,
            }
            return await self._make_request(endpoint, method="POST", data=data)

        try:
            # Make the API request
            result = await api_call()

            # Create the response with the video information
            return MCPVideoFromScriptResponse(
                video_url=result.get("video_url"),
                instructions=result.get("instructions"),
            )

        except httpx.RequestError as exc:
            return MCPVideoFromScriptResponse(error=f"HTTP Request failed: {exc}")
        except httpx.HTTPStatusError as exc:
            return MCPVideoFromScriptResponse(
                error=f"HTTP Error: {exc.response.status_code} - {exc.response.text}"
            )
        except Exception as e:
            return MCPVideoFromScriptResponse(
                error=f"An unexpected error occurred: {e}"
            )
