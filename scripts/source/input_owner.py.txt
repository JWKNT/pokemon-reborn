"""One process family owns normal game controls; inherited children share it."""
import atexit
import fcntl
import json
import os
from pathlib import Path
import time
import uuid

_handle = None
_joined = False


def acquire():
    global _handle, _joined
    if _handle is not None or _joined:
        return
    path = Path(__file__).resolve().parents[1] / 'work/active-input-owner.json'
    path.parent.mkdir(exist_ok=True)
    handle = path.open('a+')
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.seek(0)
        try:
            owner = json.load(handle)
        except (ValueError, OSError):
            owner = {}
        handle.close()
        if owner.get('token') and owner['token'] == os.environ.get('REBORN_INPUT_OWNER'):
            _joined = True
            return
        raise RuntimeError(f"Another UI worker owns game controls: PID {owner.get('pid', 'starting')}")
    token = uuid.uuid4().hex
    handle.seek(0)
    handle.truncate()
    json.dump({'pid': os.getpid(), 'token': token, 'started_epoch': time.time()}, handle)
    handle.flush()
    os.environ['REBORN_INPUT_OWNER'] = token
    _handle = handle
    atexit.register(release)


def release():
    global _handle
    if _handle is not None:
        fcntl.flock(_handle, fcntl.LOCK_UN)
        _handle.close()
        _handle = None
