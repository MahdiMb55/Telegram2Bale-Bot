from pathlib import Path
import json

def load_config():
    path = Path(__file__).parent / "config.json"
    return json.loads(path.read_text(encoding="utf-8"))