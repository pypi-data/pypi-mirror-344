from __future__ import annotations

from typing import Any

import toml


def yaml_compose(*args, **kwargs):
    raise NotImplementedError("yaml_compose is not implemented")


def yaml_load(stream):
    return toml.load(stream).get("tool", {}).get("pre-commit", {})


def yaml_dump(o: Any, **kwargs: Any) -> str:
    raise NotImplementedError("yaml_dump is not implemented")
