"""Validated configuration loading."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ResourceThreshold:
    max_usage_percent: float


@dataclass(frozen=True)
class NetworkConfig:
    target: str
    port: int
    timeout: float


@dataclass(frozen=True)
class AppConfig:
    cpu: ResourceThreshold
    memory: ResourceThreshold
    disk: ResourceThreshold
    disk_path: str
    network: NetworkConfig
    services: tuple[str, ...]


def _threshold(section: dict[str, Any], name: str) -> ResourceThreshold:
    value = float(section.get("max_usage_percent", 90))
    if not 0 < value <= 100:
        raise ValueError(f"{name}.max_usage_percent must be between 0 and 100")
    return ResourceThreshold(value)


def load_config(path: Path | None = None) -> AppConfig:
    """Load project YAML configuration and validate its values."""
    config_path = path or Path(__file__).resolve().parents[1] / "config" / "config.yaml"
    try:
        with config_path.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except OSError as exc:
        raise RuntimeError(f"Cannot read configuration {config_path}: {exc}") from exc

    try:
        network_data = data.get("network", {})
        network = NetworkConfig(
            target=str(network_data.get("target", "127.0.0.1")),
            port=int(network_data.get("port", 0)),
            timeout=float(network_data.get("timeout", 3)),
        )
        if network.timeout <= 0 or not 0 <= network.port <= 65535:
            raise ValueError("network timeout/port is invalid")
        disk_data = data.get("disk", {})
        services = tuple(str(item) for item in data.get("services", []))
        return AppConfig(
            cpu=_threshold(data.get("cpu", {}), "cpu"),
            memory=_threshold(data.get("memory", {}), "memory"),
            disk=_threshold(disk_data, "disk"),
            disk_path=str(disk_data.get("path", "/")),
            network=network,
            services=services,
        )
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f"Invalid configuration {config_path}: {exc}") from exc
