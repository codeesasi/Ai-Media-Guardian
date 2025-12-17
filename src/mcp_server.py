from mcp.server.fastmcp import FastMCP
from vlc_controller import VLCController

mcp = FastMCP(
    name="vlc-mcp-controller"
)

vlc = VLCController()
vlc_started = False

@mcp.tool()
def launch_vlc() -> str:
    """
    Launches the VLC media player if it is not already running.

    This function checks the status of the VLC player and starts it if it hasn't
    been started yet. It updates the vlc_started flag to reflect the player's status.

    Returns:
        str: A success message indicating that VLC has been launched.
    """
    global vlc_started
    if not vlc_started:
        vlc.start()
        vlc_started = True

    return "VLC Launched successfully"

@mcp.tool()
def load_video(path: str) -> str:
    """
    Loads and plays a video file in VLC.

    This function takes a file path as input, launches VLC if it's not already running,
    and then plays the specified video.

    Args:
        path (str): The path to the video file.

    Returns:
        str: A message indicating the video that was loaded, or an error message if the path is invalid.
    """
    if not path:
        return "ERROR: path is required"
    launch_vlc()
    vlc.play(path)
    return f"Loaded video: {path}"


@mcp.tool()
def pause() -> str:
    """
    Pauses or resumes the current video playback in VLC.

    This function toggles the pause state of the currently playing video.

    Returns:
        str: A message indicating that the playback has been toggled, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.pause()
    return "Playback toggled"


@mcp.tool()
def stop() -> str:
    """
    Stops the current video playback in VLC.

    This function stops the currently playing video and resets the player.

    Returns:
        str: A message indicating that the playback has been stopped, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.stop()
    return "Playback stopped"


@mcp.tool()
def seek(seconds: int) -> str:
    """
    Seeks to a specific position in the current video playback in VLC.

    This function moves the current playback position to the specified number of seconds.

    Args:
        seconds (int): The number of seconds to seek to.

    Returns:
        str: A message indicating the number of seconds the playback was seeked to, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.seek(seconds)
    return f"Seeked {seconds} seconds"


@mcp.tool()
def set_volume(level: int) -> str:
    """
    Sets the volume level of the VLC player.

    This function sets the volume of the VLC player to the specified level.

    Args:
        level (int): The desired volume level (0-100).

    Returns:
        str: A message indicating the volume level that was set, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_volume(level)
    return f"Volume set to {level}"


@mcp.tool()
def mute() -> str:
    """
    Mutes or unmutes the VLC player.

    This function toggles the mute state of the VLC player.

    Returns:
        str: A message indicating that the player has been muted, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.mute()
    return "Muted"


@mcp.tool()
def status() -> str:
    """
    Retrieves the current status information of the VLC player.

    This function gets information about the currently playing media, such as
    the title, artist, and duration.

    Returns:
        str: A string representation of the current media information, or a message indicating that VLC is not running.
    """
    if not vlc_started:
        return "VLC not started yet"
    return str(vlc.current_media_info())


# ---------- Video tools ----------

@mcp.tool()
def aspect_ratio(ratio: str) -> str:
    """
    Sets the aspect ratio of the video output in VLC.

    Args:
        ratio (str): The desired aspect ratio (e.g., "16:9", "4:3").

    Returns:
        str: A message indicating the aspect ratio that was set, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_aspect_ratio(ratio)
    return f"Aspect ratio set to {ratio}"


@mcp.tool()
def crop(ratio: str) -> str:
    """
    Sets the crop ratio of the video output in VLC.

    Args:
        ratio (str): The desired crop ratio (e.g., "16:9", "4:3").

    Returns:
        str: A message indicating the crop ratio that was set, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_crop(ratio)
    return f"Crop set to {ratio}"


@mcp.tool()
def fullscreen() -> str:
    """
    Toggles fullscreen mode in VLC.

    Returns:
        str: A message indicating that fullscreen mode was toggled, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.fullscreen()
    return "Fullscreen toggled"


@mcp.tool()
def take_snapshot() -> str:
    """
    Takes a snapshot of the current video frame in VLC.

    Returns:
        str: A message indicating that a snapshot was taken, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.snapshot()
    return "Snapshot taken"

# ---------- Audio tools ----------

@mcp.tool()
def audio_speed(rate: float) -> str:
    """
    Sets the playback rate (speed) of the audio in VLC.

    Args:
        rate (float): The desired playback rate (e.g., 1.0 for normal speed, 2.0 for double speed).

    Returns:
        str: A message indicating the playback rate that was set, or an error message if VLC is not running.
    """
    if not vlc_started:
        return "ERROR: VLC is not running"
    vlc.set_playback_rate(rate)
    return f"Playback speed set to {rate}"

@mcp.tool()
def list_movies(refresh: bool = False) -> dict:
    """
    List movies from configured folder in JSON format.
    """
    return vlc.list_movies(refresh=refresh)


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")