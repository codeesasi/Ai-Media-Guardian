import subprocess
import time
import requests
import urllib.parse
from requests.auth import HTTPBasicAuth
from settings import (
    VLC_PATH,
    VLC_HOST,
    VLC_PORT,
    VLC_PASSWORD,
    VLC_STARTUP_WAIT,
)


class VLCController:
    """Low-level VLC HTTP controller (NO AI, NO MCP logic here)"""

    def __init__(self):
        self.base_url = f"{VLC_HOST}/requests/status.json"

    def start(self):
        subprocess.Popen([
            VLC_PATH,
            "--extraintf", "http",
            "--http-password", VLC_PASSWORD,
            "--http-port", VLC_PORT,
        ])
        time.sleep(VLC_STARTUP_WAIT)

    def _send(self, command=None, params=None):
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
        url_path = urllib.parse.quote(
            file_path.replace("\\", "/"), safe=":/"
        )
        return self._send(
            "in_play",
            {"input": f"file:///{url_path}"},
        )

    def pause(self):
        return self._send("pl_pause")

    def seek(self, seconds: int):
        val = f"+{seconds}s" if seconds >= 0 else f"{seconds}s"
        return self._send("seek", {"val": val})

    def status(self):
        return self._send()
    
    def stop(self):
        self._send("pl_stop")

    def set_volume(self, level: int):
        self._send("volume", {"val": level})

    def mute(self):
        self._send("volume", {"val": 0})

    def shutdown(self):
        self._send("quit")

    def set_brightness(self, value: float):
        # value: 0.0 – 2.0 (1.0 = normal)
        self._send("brightness", {"val": value})

    def set_aspect_ratio(self, ratio: str):
        # examples: "16:9", "4:3", "1:1", "21:9"
        self._send("aspect-ratio", {"val": ratio})

    def set_crop(self, crop: str):
        # examples: "16:9", "4:3", "1:1"
        self._send("crop", {"val": crop})

    def fullscreen(self):
        self._send("fullscreen")

    def snapshot(self):
        self._send("snapshot")

    def set_playback_rate(self, rate: float):
        # examples: 0.5, 1.0, 1.25, 1.5, 2.0
        self._send("rate", {"val": rate})

    def set_audio_device(self, device_id: str):
        # device_id from VLC audio-device list
        self._send("adev", {"val": device_id})