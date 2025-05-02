from typing import Sequence
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError
from enum import Enum
from pydantic import BaseModel
import io
import requests
from PIL import Image as PILImage
import json


class DogEyeTools(str, Enum):
    DIAGNOSE = "dog_eye_diagnosis"


class DogEyeDiagnosisInput(BaseModel):
    image_path: str


class DogEyeServer:
    MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1MB

    def diagnose_dog_eye(self, image_path: str) -> dict:
        img = PILImage.open(image_path).convert("RGB")
        img.thumbnail((1024, 1024))

        quality = 90
        step = 10

        while True:
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            size = buffer.tell()

            if size <= self.MAX_SIZE_BYTES or quality <= step:
                buffer.seek(0)
                break

            quality -= step

        files = {'img_file': ('compressed.jpg', buffer, 'image/jpeg')}
        response = requests.post("http://13.124.223.37/v1/prediction/binary", files=files)

        try:
            return response.json()
        except ValueError:
            raise McpError(f"Invalid JSON response: {response.text}")


async def serve() -> None:
    server = Server("dog-eye-diagnosis")
    dog_eye_server = DogEyeServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=DogEyeTools.DIAGNOSE.value,
                description="Analyze a dog's eye image and return diagnosis probabilities for 10 diseases.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "Local filesystem path to the dog's eye image file."
                        }
                    },
                    "required": ["image_path"],
                },
            )
        ]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        try:
            match name:
                case DogEyeTools.DIAGNOSE.value:
                    image_path = arguments.get("image_path")
                    if not image_path:
                        raise ValueError("Missing required argument: image_path")

                    result = dog_eye_server.diagnose_dog_eye(image_path)

                case _:
                    raise ValueError(f"Unknown tool: {name}")

            return [
                TextContent(type="text", text=json.dumps(result, indent=2))
            ]

        except Exception as e:
            raise ValueError(f"Error processing dog-eye-diagnosis query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)
