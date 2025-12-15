from mcp.server.fastmcp import FastMCP
from vlc_controller import VLCController

mcp = FastMCP(
    name="vlc-mcp-controller"
)

vlc = VLCController()
vlc_started = False


@mcp.tool()
def play_video(path: str) -> str:
    global vlc_started
    if not path:
        return "ERROR: path is required"
    if not vlc_started:
        vlc.start()
        vlc_started = True
    vlc.play(path)
    return f"Playing video: {path}"


@mcp.tool()
def load_video(path: str) -> str:
    global vlc_started
    if not path:
        return "ERROR: path is required"
    if not vlc_started:
        vlc.start()
        vlc_started = True
    vlc.load(path)
    return f"Loaded video: {path}"


@mcp.tool()
def pause() -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.pause()
    return "Playback toggled"


@mcp.tool()
def stop() -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.stop()
    return "Playback stopped"


@mcp.tool()
def seek(seconds: int) -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.seek(seconds)
    return f"Seeked {seconds} seconds"


@mcp.tool()
def set_volume(level: int) -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_volume(level)
    return f"Volume set to {level}"


@mcp.tool()
def mute() -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.mute()
    return "Muted"


@mcp.tool()
def status() -> str:
    if not vlc_started:
        return "VLC not started yet"
    return str(vlc.status())


@mcp.tool()
def shutdown_vlc() -> str:
    global vlc_started
    if not vlc_started:
        return "VLC not running"
    vlc.shutdown()
    vlc_started = False
    return "VLC shutdown"

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")