import subprocess, os, time
import time,socket,requests
import urllib.parse
from requests.auth import HTTPBasicAuth
from settings import (
    VLC_PATH,
    VLC_HOST,
    VLC_PORT,
    VLC_PASSWORD,
    VLC_STARTUP_WAIT,
    MOVIES_DIR, VIDEO_EXTENSIONS
)

class VLCController:
    """Low-level VLC HTTP controller (NO AI, NO MCP logic here)"""
    _movie_cache = None

    def __init__(self):
        self.base_url = f"{VLC_HOST}/requests/status.json"

    def start(self):
        """
        Starts the VLC media player as a subprocess.
        """
        subprocess.Popen([
            VLC_PATH,
            "--extraintf", "http",
            "--http-password", VLC_PASSWORD,
            "--http-port", VLC_PORT,
        ])
        time.sleep(VLC_STARTUP_WAIT)

    def _send(self, command=None, params=None):
        """
            Send a GET request to the VLC HTTP interface.\n
            Parameters
                command : str, optional
                    The VLC command to execute (e.g., ``'pl_play'``). If provided, it is added
                    to the query parameters as ``command``.\n

                params : dict, optional
                    Additional query‑string parameters to include in the request. If ``None``,
                    an empty dict is created.
        """
        params = params or {}
        if command:
            params["command"] = command

        r = requests.get(
            self.base_url,
            params=params,
            auth=HTTPBasicAuth("", VLC_PASSWORD),
            timeout=5,
        )
        r.raise_for_status()
        return r.json()

    def play(self, file_path: str):
        """
        Plays a media file.

        Args:
            file_path (str): The path to the file to play.

        Returns:
            dict: The JSON response from the VLC server.
        """
        url_path = urllib.parse.quote(
            file_path.replace("\\", "/"), safe=":/"
        )
        return self._send(
            "in_play",
            {"input": f"file:///{url_path}"},
        )

    def pause(self):
        """
        Pauses or resumes playback.

        Returns:
            dict: The JSON response from the VLC server.
        """
        return self._send("pl_pause")

    def seek(self, seconds: int):
        """
        Seeks to a specific position in the media.

        Args:
            seconds (int): The number of seconds to seek. Positive values seek forward, negative values seek backward.

        Returns:
            dict: The JSON response from the VLC server.
        """
        val = f"+{seconds}s" if seconds >= 0 else f"{seconds}s"
        return self._send("seek", {"val": val})

    def status(self):
        """
        Gets the current status of VLC.

        Returns:
            dict: The JSON response from the VLC server.
        """
        return self._send()

    def stop(self):
        """
        Stops playback.
        """
        self._send("pl_stop")

    def set_volume(self, level: int):
        """
        Sets the volume level.

        Args:
            level (int): The volume level (0-100).
        """
        self._send("volume", {"val": level})

    def mute(self):
        """
        Mutes the audio.
        """
        self._send("volume", {"val": 0})

    def set_aspect_ratio(self, ratio: str):
        """
        Sets the aspect ratio of the video output.

        Args:
            ratio (str): The aspect ratio (e.g., "16:9", "4:3").
        """
        # examples: "16:9", "4:3", "1:1", "21:9"
        self._send("aspect-ratio", {"val": ratio})

    def set_crop(self, crop: str):
        """
        Sets the crop ratio of the video output.

        Args:
            crop (str): The crop ratio (e.g., "16:9", "4:3").
        """
        # Examples: "16:9", "4:3", "1:1"
        self._send("crop", {"val": crop})

    def fullscreen(self):
        """
        Toggles fullscreen mode.
        """
        self._send("fullscreen")

    def snapshot(self):
        """
        Takes a snapshot of the current video frame.
        """
        self._send("snapshot")

    def set_playback_rate(self, rate: float):
        """
        Sets the playback rate.

        Args:
            rate (float): The playback rate (e.g., 0.5, 1.0, 1.25, 1.5, 2.0).
        """
        # examples: 0.5, 1.0, 1.25, 1.5, 2.0
        self._send("rate", {"val": rate})

    def current_media_info(self) -> dict:
        """
        Retrieves the current media information.

        Returns:
            dict: A dictionary containing the title, artist, album, duration, position, state, volume, and rate of the currently playing media.
        """
        status = self.status()

        info = {}
        meta = status.get("information", {}).get("category", {}).get("meta", {})

        info["title"] = meta.get("title")
        info["artist"] = meta.get("artist")
        info["album"] = meta.get("album")

        info["duration"] = status.get("length")
        info["position"] = status.get("time")
        info["state"] = status.get("state")
        info["rate"] = status.get("rate")
        info["volume"] = status.get("volume")

        return info
    
    def list_movies(self, refresh: bool = False) -> dict:
        """
        Returns movies in structured JSON format.
        - Supports movie files
        - Supports movie folders with internal video files
        - One-level scan only (optimized)
        """
        if self._movie_cache is not None and not refresh:
            return self._movie_cache

        movies = []

        try:
            with os.scandir(MOVIES_DIR) as entries:
                for entry in entries:

                    # -------- Case 1: Movie file directly --------
                    if entry.is_file():
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext in VIDEO_EXTENSIONS:
                            movies.append({
                                "name": os.path.splitext(entry.name)[0],
                                "type": "file",
                                "files": [
                                    {
                                        "filename": entry.name,
                                        "path": entry.path
                                    }
                                ]
                            })

                    # -------- Case 2: Movie folder --------
                    elif entry.is_dir():
                        video_files = []

                        try:
                            with os.scandir(entry.path) as sub_entries:
                                for sub in sub_entries:
                                    if sub.is_file():
                                        ext = os.path.splitext(sub.name)[1].lower()
                                        if ext in VIDEO_EXTENSIONS:
                                            video_files.append({
                                                "filename": sub.name,
                                                "path": sub.path
                                            })
                        except PermissionError:
                            pass

                        movies.append({
                            "name": entry.name,
                            "type": "folder",
                            "files": video_files
                        })

        except FileNotFoundError:
            return {
                "root": MOVIES_DIR,
                "count": 0,
                "movies": [],
                "error": "MOVIES_DIR not found"
            }

        result = {
            "source": "folder_scan",
            "root": MOVIES_DIR,
            "count": len(movies),
            "movies": sorted(movies, key=lambda x: x["name"].lower())
        }

        self._movie_cache = result
        return result

