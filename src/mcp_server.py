from mcp.server import Server
from mcp.types import TextContent
from src.vlc_controller import VLCController


# Initialize VLC
vlc = VLCController()
vlc.start()


# Create MCP server
server = Server(
name="vlc-mcp-controller",
description="MCP server exposing VLC Media Player controls",
)




@server.tool(
    name="play_video",
    description="Play a local video file in VLC",
    input_schema={
    "type": "object",
    "properties": {
    "path": {
    "type": "string",
    "description": "Absolute path to the video file",
    }
    },
    "required": ["path"],
    },
    )
def play_video(path: str):
    vlc.play(path)
    return [TextContent(text=f"Playing video: {path}")]




@server.tool(
    name="pause",
    description="Pause or resume VLC playback",
    )
def pause():
    vlc.pause()
    return [TextContent(text="Playback toggled")]

@server.tool(
    name="seek",
    description="Seek playback by seconds",
    input_schema={
    "type": "object",
    "properties": {
    "seconds": {
    "type": "integer",
    "description": "Seconds to seek (+forward, -backward)",
    }
    },
    "required": ["seconds"],
    },
    )
def seek(seconds: int):
    vlc.seek(seconds)
    return [TextContent(text=f"Seeked {seconds} seconds")]




@server.tool(
    name="status",
    description="Get current VLC playback status",
    )
def status():
    s = vlc.status()
    return [TextContent(text=str(s))]

def run():
    server.run()