import json
import os

_DEFAULT_BASE_URL = "http://127.0.0.1:8000"
_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "api_config.json")


def _load_base_url():
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            value = json.load(f).get("api_url")
        if value:
            return str(value).rstrip("/")
    except FileNotFoundError:
        pass
    except (ValueError, OSError) as e:
        print(f"config: ignoring bad {_CONFIG_PATH}: {e}")
    return _DEFAULT_BASE_URL


BASE_URL = _load_base_url()
