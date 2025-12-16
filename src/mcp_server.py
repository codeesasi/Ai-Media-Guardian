from mcp.server.fastmcp import FastMCP
from vlc_controller import VLCController

mcp = FastMCP(
    name="vlc-mcp-controller"
)

vlc = VLCController()
vlc_started = False

@mcp.tool()
def launch_vlc() -> str:
    global vlc_started
    if not vlc_started:
        vlc.start()
        vlc_started = True

    return "VLC Launched successfully"

@mcp.tool()
def load_video(path: str) -> str:
    if not path:
        return "ERROR: path is required"
    launch_vlc()
    vlc.play(path)
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
    return str(vlc.current_media_info())


@mcp.tool()
def shutdown_vlc() -> str:
    global vlc_started
    if not vlc_started:
        return "VLC not running"
    vlc.shutdown()
    vlc_started = False
    return "VLC shutdown"

# ---------- Video tools ----------

@mcp.tool()
def set_brightness(value: float) -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_brightness(value)
    return f"Brightness set to {value}"


@mcp.tool()
def aspect_ratio(ratio: str) -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_aspect_ratio(ratio)
    return f"Aspect ratio set to {ratio}"


@mcp.tool()
def crop(ratio: str) -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_crop(ratio)
    return f"Crop set to {ratio}"


@mcp.tool()
def fullscreen() -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.fullscreen()
    return "Fullscreen toggled"


@mcp.tool()
def take_snapshot() -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.snapshot()
    return "Snapshot taken"


# ---------- Audio tools ----------

@mcp.tool()
def audio_speed(rate: float) -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_playback_rate(rate)
    return f"Playback speed set to {rate}"


@mcp.tool()
def audio_device(device_id: str) -> str:
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_audio_device(device_id)
    return f"Audio device set to {device_id}"

@mcp.tool()
def list_audio_devices() -> list:
    if not vlc_started:
        return ["ERROR: VLC is not running"]
    return vlc.list_audio_devices()

@mcp.tool()
def list_audio_drive() -> list:
    if not vlc_started:
        return ["ERROR: VLC is not running"]
    return vlc.list_audio_outputs()

@mcp.tool()
def list_video_outputs() -> list:
    if not vlc_started:
        return ["ERROR: VLC is not running"]
    return vlc.list_video_outputs()

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")