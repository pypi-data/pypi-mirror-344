import json
import pathlib

path = pathlib.Path(__file__).parent / 'metadata.json'
if path.exists():
    __DEBUG__ = False
else:
    path = pathlib.Path(__file__).parent.parent / 'metadata.json'
    __DEBUG__ = True
with open(path) as f:
    _METADATA = json.load(f)
    __author__ = _METADATA['authors']
    __version__ = _METADATA['version']
    __description__ = _METADATA['description']