from __future__ import annotations

from typing import Any

import toml
import yaml


def yaml_compose(*args, **kwargs):
    raise NotImplementedError("yaml_compose is not implemented")


def yaml_load(stream):
    try:
        return toml.loads(stream).get("tool", {}).get("pre-commit", {})
    except ValueError:
        return yaml.load(stream, Loader=yaml.SafeLoader)


def yaml_dump(o: Any, **kwargs: Any) -> str:
    raise NotImplementedError("yaml_dump is not implemented")
