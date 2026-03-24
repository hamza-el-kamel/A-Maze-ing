
def parse_entry(val: str) -> tuple[int, int]:
    try:
        x_str, y_str = val.split(',')
        return int(x_str.strip()), int(y_str.strip())
    except ValueError:
        raise ValueError(f"Invalid coordinate format. Expected x,y but got: {val}")

def parse_bool(val: str) -> bool:
    normalized = val.strip().lower()
    if normalized in ('true', '1', 'yes'):
        return True
    if normalized in ('false', '0', 'no'):
        return False
    raise ValueError(f"Invalid boolean format: {val}")

def parse_config(path: str) -> dict:
    config = {}

    PARSERS = {
        "WIDTH": int,
        "HEIGHT": int,
        "ENTRY": parse_entry,
        "EXIT": parse_entry,
        "OUTPUT_FILE": str,
        "PERFECT": parse_bool,
    }

    required_keys = set(PARSERS.keys())

    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()

                # Ignore empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Validate format
                if "=" not in line:
                    raise ValueError(f"Invalid line format: {line}")

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Check valid key
                if key not in PARSERS:
                    raise ValueError(f"Unknown key: {key}")

                # Parse value
                parser = PARSERS[key]
                config[key] = parser(value)

    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {path}")

    missing = required_keys - config.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    return config