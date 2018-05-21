import sys
import os
from os.path import basename, splitext
from typing import Any, Optional, Text, Tuple

current_dir = os.path.dirname(os.path.abspath(__file__))

def import_module_from_source(path: Text, name: Optional[Text]=None) -> Any:
    if not name:
        name = splitext(basename(path))[0]

    # importlib.util.module_from_spec is supported from Python3.5
    py_version = sys.version_info
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 5):
        import imp
        module = imp.load_source(name, path)
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        loader = spec.loader
        if loader is None:
            return None
        loader.exec_module(module)

    return module

def resolve_bot_path(name: Text) -> Tuple[Text, Text]:
    if os.path.isfile(name) or os.path.isfile(name + '.py'):
        bot_path = os.path.abspath(name) if os.path.isfile(name) else os.path.abspath(name + '.py')
        bot_name = splitext(basename(bot_path))[0]
    else:
        bot_path = os.path.abspath(os.path.join(current_dir, 'bots', name, name + '.py'))
        bot_name = name
    sys.path.insert(0, os.path.dirname(bot_path))

    return (bot_path, bot_name)
