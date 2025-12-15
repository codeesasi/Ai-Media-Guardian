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

    def load(self, path: str):
        self._send("in_enqueue", {"input": path})