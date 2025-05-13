import yaml
from pathlib import Path

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)

    def get(self, *keys):
        value = self._config
        for key in keys:
            value = value[key]
        return value

config = Config()
