import logging

from mcp.server.fastmcp import FastMCP

from invideo_ai_mcp.api_client import (
    InVideoApiClient,
    MCPIdeasResponse,
    MCPScriptResponse,
    MCPVideoFromScriptResponse,
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("invideo-ai")
logger.info("Initialized FastMCP server with name 'invideo-ai'")

# Constants
API_HOST = "https://pro-api.invideo.io"

# Global API client
api_client = None


async def get_api_client() -> InVideoApiClient:
    """Get or create the API client instance."""
    global api_client

    if api_client is not None:
        return api_client

    # Create and store client
    api_client = InVideoApiClient(api_host=API_HOST)
    return api_client


@mcp.tool(
    name="generate_content_ideas",
    description="Generate content ideas for a specific platform with topic, vibe, and target audience suggestions.",
)
async def generate_content_ideas(
    platform_conversation_starter: str,
) -> MCPIdeasResponse:
    """Generate content ideas for a specific platform.

    Args:
        platform_conversation_starter: A conversation starter that includes the intended video platform
            (e.g., YouTube, Instagram, TikTok) and the initial context or intent for video creation.
    """
    try:
        logger.info(f"Generating content ideas for: {platform_conversation_starter}")
        client = await get_api_client()
        return await client.generate_content_ideas(platform_conversation_starter)
    except Exception as e:
        logger.error(f"Failed to generate content ideas: {str(e)}")
        return MCPIdeasResponse(error=str(e))


@mcp.tool(
    name="generate_script",
    description="Generate a video script based on topic, vibe, and target audience. "
    "Returns a response containing the generated script text and the prompt used to generate it.",
)
async def generate_script(topic: str, vibe: str, target_audience: str) -> MCPScriptResponse:
    """Generate a video script.

    Args:
        topic: The main topic of the video
        vibe: The vibe/tone of the video (e.g., "educational", "entertaining", "professional")
        target_audience: The target audience for the video

    Returns:
        MCPScriptResponse object with fields:
        - script: The generated video script
        - prompt: The prompt used to generate the script
        - error: Error message if any occurred during generation
    """
    try:
        logger.info(f"Generating script for topic: {topic}, vibe: {vibe}, target audience: {target_audience}")
        client = await get_api_client()
        return await client.generate_script(topic, vibe, target_audience)
    except Exception as e:
        logger.error(f"Failed to generate script: {str(e)}")
        return MCPScriptResponse(error=str(e))


@mcp.tool(
    name="generate_video_from_script",
    description="Generate a video using a script and additional context (topic, vibe, target audience). "
    "Returns video ID and instructions for checking status.",
)
async def generate_video_from_script(
    script: str, topic: str, vibe: str, target_audience: str, platform: str
) -> MCPVideoFromScriptResponse:
    """Generate a video from a script with additional context.

    Args:
        script: The video script content
        topic: The main topic of the video
        vibe: The vibe/tone of the video (e.g., "educational", "entertaining", "professional")
        target_audience: The target audience for the video
        platform: The platform to generate the video for (e.g., "youtube", "instagram", "tiktok")

    Returns:
        MCPVideoFromScriptResponse object with fields:
        - video_id: Unique identifier for the generated video
        - status: Current status of the video generation process
        - estimated_time: Estimated time to complete generation (in seconds)
        - instructions: Instructions for checking video status
        - error: Error message if any occurred during generation
    """
    try:
        logger.info(
            f"Generating video from script with topic: {topic}, "
            f"vibe: {vibe}, target audience: {target_audience}, "
            f"platform: {platform}"
        )
        client = await get_api_client()
        return await client.generate_video_from_script(script, topic, vibe, target_audience, platform)
    except Exception as e:
        logger.error(f"Failed to generate video from script: {str(e)}")
        return MCPVideoFromScriptResponse(error=str(e))


def main():
    """Main entry point for the MCP server."""
    # Initialize and run the server
    logger.info("Starting MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
