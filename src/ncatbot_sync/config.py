import yaml
import os
from pathlib import Path

class Config:
    __slots__ = ("url", "token")
    
    def __init__(self, url, token):
        self.url = url
        self.token = token

def load_config(path=os.path.join(os.getcwd(), "config.yaml")):
    config_path = Path(path)
    if not config_path.exists():
        return Config("ws://localhost:3001", "")
    
    with config_path.open() as f:
        config_data = yaml.safe_load(f) or {}
    
    return Config(
        url=config_data.get("url", "ws://localhost:3001"),
        token=config_data.get("token", "")
    )
