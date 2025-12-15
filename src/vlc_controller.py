import subprocess
import time
import requests
import urllib.parse
from requests.auth import HTTPBasicAuth
from config.settings import (VLC_Host, VLC_Password, VLC_Path, VLC_Port,VLC_Strat_timeout)

class VLCController:
    def __init__(self):
        self.base_url = f"{VLC_Host}/requests/status.json"

    def start(self):
        subprocess.Popen([
            VLC_Path,"--extraintf","http",
            "--http-password",VLC_Password,
            "--http-port",VLC_Port
        ])
        time.sleep(VLC_Strat_timeout)

    def _send(self, command, params=None):
        params = params or {}
        params["command"] = command

        req = requests.get(self.base_url,
                           params=params,
                           auth=HTTPBasicAuth("",VLC_Password),
                           timeout=VLC_Strat_timeout)

        req.raise_for_status()
        return req.json()
    
    def play(self, filepath):
        url_path = urllib.parse.quote(filepath.replace("\\",'/'), safe=":/")
        return self._send("in_play",{"input":f"file:///{url_path}"})
    
    def pause(self):
        return self._send("pl_pause")
    
    def seek(self, second):
        val = f"{second}s" if second < 0 else f"+{second}s"
        return self._send("seek", {"val":val})
    
    def status(self):
        return self._send("")
    