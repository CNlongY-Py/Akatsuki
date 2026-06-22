import json
import os
from typing import Optional

from libs import logger

log = logger.get_logger("Session")

_CFG_FOLDER = "config/sessions/"
SESSIONS_DIR = os.path.join(_CFG_FOLDER, "sessions") + "/"
SESSIONS_JSON = os.path.join(_CFG_FOLDER, "sessions.json")


class Account:
    def __init__(self, name: str, token: str, auth_type: str = "token"):
        self.name = name
        self.token = token
        self.auth_type = auth_type


_accounts: dict[str, Account] = {}
_bindings: dict[str, list[str]] = {}
_initialized = False


def _resolve_paths(cfg_folder: str) -> None:
    global _CFG_FOLDER, SESSIONS_DIR, SESSIONS_JSON
    _CFG_FOLDER = cfg_folder.rstrip("/\\") + "/"
    SESSIONS_DIR = os.path.join(_CFG_FOLDER, "sessions") + "/"
    SESSIONS_JSON = os.path.join(_CFG_FOLDER, "sessions.json")


def init(cfg_folder: str | None = None) -> None:
    global _initialized
    if cfg_folder:
        _resolve_paths(cfg_folder)
    os.makedirs(SESSIONS_DIR, exist_ok=True)

    if os.path.isdir(SESSIONS_DIR):
        for fname in os.listdir(SESSIONS_DIR):
            if fname.endswith(".token"):
                name = fname[:-6]
                try:
                    with open(os.path.join(SESSIONS_DIR, fname)) as f:
                        token = f.read().strip()
                    if token:
                        _accounts[name] = Account(name, token)
                except OSError:
                    log.warning(f"failed to read {fname}")

    if os.path.isfile(SESSIONS_JSON):
        try:
            with open(SESSIONS_JSON) as f:
                data = json.load(f)
            raw = data.get("bindings")
            if raw is None:
                raw = data.get("listeners", {})
            for pid, val in raw.items():
                if isinstance(val, list):
                    _bindings[pid] = list(val)
                else:
                    _bindings[pid] = [val]
            for name, meta in data.get("accounts", {}).items():
                if name in _accounts:
                    _accounts[name].auth_type = meta.get("auth_type", "token")
        except (json.JSONDecodeError, OSError):
            log.warning("failed to load sessions.json")

    _initialized = True
    log.debug(f"loaded {len(_accounts)} accounts, {len(_bindings)} plugin bindings")


def _save_metadata() -> None:
    data = {
        "bindings": {pid: list(accs) for pid, accs in _bindings.items()},
        "accounts": {name: {"auth_type": acc.auth_type} for name, acc in _accounts.items()},
    }
    with open(SESSIONS_JSON, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _write_token_file(name: str, token: str) -> None:
    path = os.path.join(SESSIONS_DIR, f"{name}.token")
    with open(path, "w") as f:
        f.write(token)


def get_account(name: str) -> Optional[Account]:
    return _accounts.get(name)


def list_accounts() -> dict[str, Account]:
    return dict(_accounts)


def add_token_account(name: str, token: str) -> Account:
    _accounts[name] = Account(name, token, auth_type="token")
    _write_token_file(name, token)
    _save_metadata()
    log.debug(f"added token account '{name}'")
    return _accounts[name]


def add_official_account(name: str, token: str) -> Account:
    _accounts[name] = Account(name, token, auth_type="official")
    _write_token_file(name, token)
    _save_metadata()
    return _accounts[name]


def remove_account(name: str) -> None:
    _accounts.pop(name, None)
    token_path = os.path.join(SESSIONS_DIR, f"{name}.token")
    if os.path.isfile(token_path):
        os.remove(token_path)
    for pid in list(_bindings):
        _bindings[pid] = [a for a in _bindings[pid] if a != name]
        if not _bindings[pid]:
            _bindings.pop(pid, None)
    _save_metadata()
    log.debug(f"removed account '{name}'")


def get_current_account(data: dict) -> Optional[Account]:
    name = data.get("name")
    if not name:
        return None
    return _accounts.get(name)


def add_binding(plugin_id: str, account_name: str) -> None:
    _bindings.setdefault(plugin_id, []).append(account_name)
    _save_metadata()


def remove_binding(plugin_id: str, account_name: str) -> None:
    accs = _bindings.get(plugin_id)
    if not accs:
        return
    accs = [a for a in accs if a != account_name]
    if accs:
        _bindings[plugin_id] = accs
    else:
        _bindings.pop(plugin_id, None)
    _save_metadata()


def remove_plugin(plugin_id: str) -> None:
    _bindings.pop(plugin_id, None)
    _save_metadata()


def get_bindings(plugin_id: str) -> list[str] | None:
    return _bindings.get(plugin_id)


def list_bindings() -> dict[str, list[str]]:
    return dict(_bindings)
