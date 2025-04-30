import json
import pathlib

with open(pathlib.Path(__file__).parent.parent.parent / 'metadata.json') as f:
    _METADATA = json.load(f)
    __author__ = _METADATA['author']
    __version__ = _METADATA['version']
    __description__ = _METADATA['description']