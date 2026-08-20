import os
import json


################################################################################################################################


_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_INFO_FILE_PATH = os.path.join(_ROOT_DIR, "data", "command_info.json")

with open(_INFO_FILE_PATH, "r", encoding="utf-8") as f:
    CMD_INFO = json.load(f)