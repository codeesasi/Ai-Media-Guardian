from mcp.server import Server
from mcp.types import Tool, TextContext
from src.vlc_controller import VLCController

vlc = VLCController()
vlc.start()

server = Server(name="vlc-controller",
                description="Control VLC Media Player Via MCP")

# --- Tool: Play video ----
@server.tool(
    name="play_video",
    description = "play a local video file in VLC",
    input_schema={
                  "type":"object",
                  "properties":{
                      "path":{
                          "type":"string",
                          "description":"Absolute path to video file"
                          }
                    },
                    "required":["path"]
                }
                          
)

def play_video(path:str):
    vlc.play(path)
    return [TextContext(text=f"Playing video:{path}")]

# --- TOOL: Pause ---
@server.tool(
    name="pause",
    description="pause or resume VLC player"
)

def pause():
    vlc.pause()
    return [TextContext(text="Toggled pause")]

# ---TOOL: SEEEK ----

@server.tool(name="seek",
             description="Seek video by seconds (+/_)",
             input_schema={
                 "type":"object",
                 "properties":{
                     "seconds":{"type":"integer","description":"Seconds to seek (+Forward, -Backword)"}
                 },
                 "required":["seconds"]
             }
            )

def seek(seconds: int):
    vlc.seek(seconds)
    return [TextContext(text="fSeeked {seconds} seconds")]

def run():
    server.run()

    