from collections.abc import Callable
from typing import Any


def parse_entry(val: str) -> tuple[int, int]:
    try:
        x_str, y_str = val.split(",")
        return int(x_str.strip()), int(y_str.strip())
    except ValueError:
        raise ValueError(
            f"Invalid coordinate format. Expected x,y but got: {val}"
        )


def parse_bool(val: str) -> bool:
    normalized = val.strip().lower()
    if normalized in ("true", "1", "yes"):
        return True
    if normalized in ("false", "0", "no"):
        return False
    raise ValueError(f"Invalid boolean format: {val}")


def parse_config(path: str) -> dict[str, Any]:
    config: dict[str, Any] = {}

    required_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
        }

    PARSERS: dict[str, Callable[[str], Any]] = {
        "WIDTH": int,
        "HEIGHT": int,
        "ENTRY": parse_entry,
        "EXIT": parse_entry,
        "OUTPUT_FILE": str,
        "PERFECT": parse_bool,
        "SEED": int,
    }

    try:
        with open(path, "r") as file:
            for line in file:
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid line format: {line}")

                key, value = line.split("=", 1)
                key = key.strip().upper()
                value = value.strip()

                if key not in PARSERS:
                    raise ValueError(f"Unknown key: {key}")

                parser = PARSERS[key]
                config[key] = parser(value)

    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {path}")
    except PermissionError:
        raise PermissionError(
            f"Permission denied when reading config file: {path}"
            )

    missing = required_keys - config.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    return config
